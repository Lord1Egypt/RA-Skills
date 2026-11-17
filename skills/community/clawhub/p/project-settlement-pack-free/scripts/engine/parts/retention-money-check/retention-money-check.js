/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * retention-money-check.js —— 工程质量保证金（质保金/保修金）扣留与退还核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**施工方与发包方在每个月结算、竣工结算、以及保修期满退还质保金时**
 * 都必须把质保金台账核一遍。质保金是按结算金额的一定比例扣留下来的钱（工程常见不高于 3%）：
 * 扣多了占用施工方资金、到期不退要扯皮、保修期内扣减没有依据更会被投诉；
 * 而"扣留比例用错一档、保修期届满日算错一个月"这类错人眼看不出来，钱却实实在在。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * 不发起任何网络请求（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   本期扣留金额 = 本期结算金额 × 扣留比例
 *   保修期届满日 = 保修期起 + 保修期（月） − 1 日     ← 含首日口径
 *   应退金额     = 累计扣留金额 − 保修期内扣减
 *
 * 口径（必须写清楚，否则算出来是错的）：
 *   · 扣留比例可写 3 / 3% / 0.03，均按 3% 理解；
 *   · 日期可写 2024-05-01 / 2024/5/1 / 20240501 / 2024年5月1日；
 *   · 保修期届满日按**含首日**口径：2024-05-01 起 24 个月 ⇒ 2026-04-30；
 *   · 「保修期内扣减」为空按 0 理解（没扣减），并在结论里写明这一假定。
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD），并把"应退未退"做成排期与催办清单。
 * 材料不足时**绝不给结论**。
 *
 * 调用契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 */

const CHECKS_GIVEN = [
  '本期扣留金额勾稽（本期结算金额 × 扣留比例）',
  '保修期届满日勾稽（保修期起 + 保修期月数 − 1 日，含首日口径）',
  '退还金额勾稽（累计扣留金额 − 保修期内扣减）',
  '日期倒挂检测（届满日早于保修期起 / 退还日期早于保修期起）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复结算单号检测',
  '空白、占位符与无法识别的日期检测',
];

const CHECKS_WITHHELD = [
  '扣留比例超出合同上限（默认 3%，可用 payload.max_rate 覆盖）检测',
  '保修期内扣减的合理性判定（无依据扣减 / 扣减超过累计扣留 / 扣减为负）',
  '质保金应退未退的排期与逾期天数计算',
  '质保金应退未退的可执行催办清单（含合同依据行号与建议动作）',
  '保修期未满即已退还（提前退还）检测',
];

const OUT_OF_SCOPE = [
  '判断扣留比例是否合法（合同/结算单约定优先；建设工程质量保证金管理办法的 3% 是上限口径，不是唯一口径）',
  '计算逾期退还的资金占用费或利息（需要合同约定的利率与起算口径）',
  '处理银行保函、保险保单、第三方担保形式的质保金（本表只核现金扣留与退还）',
  '判断维修扣款本身该不该扣、金额是否合理（那是现场验收与维修计价的事）',
  '读取 .xlsx 或财务/ERP 系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '项目名称\t结算单号\t结算日期\t本期结算金额\t扣留比例\t本期扣留金额\t累计扣留金额\t保修期起\t保修期（月）\t保修期止\t实际退还日期\t退还金额\t保修期内扣减\t扣减依据',
  '市政道路工程A标段\tJS-2024-001\t2024-04-20\t1286400.00\t3%\t38592.00\t38592.00\t2024-05-01\t24\t2026-04-30\t2026-05-08\t38592.00\t0.00\t',
  '中岳路桥市政工程\tJS-2024-002\t2024-06-15\t950000.00\t3%\t28500.00\t28500.00\t2024-07-01\t24\t2026-06-30\t2026-07-05\t28500.00\t0.00\t',
  '豫通管网改造工程\tJS-2024-003\t2024-08-20\t5200000.00\t3%\t156000.00\t156000.00\t2024-09-01\t12\t2025-08-31\t2025-09-10\t156000.00\t0.00\t',
  '合计\t\t\t7436400.00\t\t223092.00\t223092.00\t\t\t\t\t223092.00\t0.00\t',
].join('\n');

const TOL = 0.01;
const RATE_CAP = 0.03;   // 工程质保金常见上限：不高于工程价款结算总额的 3%

const ROLES = {
  // ⚠️ 顺序即优先级，更具体的别名在前 —— 不能让「累计扣留金额」被「扣留金额」抢走、
  //    也不能让「扣减依据」被「扣减」抢走（这两个坑本仓库都踩过，见 tools/header_map_check.py）。
  project: ['项目名称', '工程名称', '单位工程', '标段名称', '项目'],
  bill: ['结算单号', '结算书编号', '结算编号', '单号'],
  settleDate: ['结算日期', '结算日', '开单日期'],
  settle: ['本期结算金额', '结算金额', '本期结算', '结算额'],
  rate: ['扣留比例', '质保金比例', '保证金比例', '预留比例', '质保金率', '扣留率', '比例'],
  cum: ['累计扣留金额', '累计质保金', '累计预留', '累计扣留'],
  withheld: ['本期扣留金额', '本期扣留质保金', '质保金扣留', '本期扣留', '扣留金额', '扣留额'],
  wStart: ['保修期起', '保修期起始', '质保期起', '保修开始', '起算日'],
  wMonths: ['保修期月', '保修期月数', '质保期月数', '保修月数', '保修期个数'],
  wEnd: ['保修期止', '保修期届满', '保修期结束', '质保期止', '保修期至', '到期日'],
  refundDate: ['实际退还日期', '退还日期', '退款日期', '退还日'],
  refundAmt: ['退还金额', '已退还金额', '退款金额', '退还额'],
  basis: ['扣减依据', '扣减事由', '扣款依据', '依据说明', '依据'],
  deduct: ['保修期内扣减', '扣减金额', '维修扣款', '扣款金额', '保修扣减', '扣减'],
};

const LABELS = {
  project: '项目名称', bill: '结算单号', settleDate: '结算日期', settle: '本期结算金额',
  rate: '扣留比例', cum: '累计扣留金额', withheld: '本期扣留金额',
  wStart: '保修期起', wMonths: '保修期（月）', wEnd: '保修期止',
  refundDate: '实际退还日期', refundAmt: '退还金额', basis: '扣减依据', deduct: '保修期内扣减',
};

const REQUIRED = ['project', 'bill', 'settle', 'rate', 'withheld', 'cum', 'wStart', 'wMonths', 'wEnd'];
const SUM_ROLES = ['settle', 'withheld', 'cum', 'refundAmt', 'deduct'];
const DATE_ROLES = ['settleDate', 'wStart', 'wEnd', 'refundDate'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|total)/i;
const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a|无|略)$/i;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim().replace(/[,，\s¥￥$]/g, '').replace(/%$/, '');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

/** 比例归一化成小数：`3` / `3%` ⇒ 0.03；`0.03` ⇒ 0.03 */
function rateRatio(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return n > 0.1 ? n / 100 : n;
}

const pad2 = (n) => String(n).padStart(2, '0');

function daysInMonth(y, m) {         // m 为 1~12
  return new Date(Date.UTC(y, m, 0)).getUTCDate();
}

/** 日期归一化成 YYYY-MM-DD；认不出返回 null（**不猜**，由「日期无法识别」检查项报出来） */
function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  let m = /^(\d{4})[-/.年](\d{1,2})[-/.月](\d{1,2})日?$/.exec(s);
  if (!m) m = /^(\d{4})(\d{2})(\d{2})$/.exec(s);
  if (!m) return null;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  if (y < 1900 || y > 2999) return null;
  if (mo < 1 || mo > 12) return null;
  if (d < 1 || d > daysInMonth(y, mo)) return null;
  return `${y}-${pad2(mo)}-${pad2(d)}`;
}

function dayNum(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || ''));
  if (!m) return null;
  return Math.round(Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3])) / 86400000);
}

function fromDayNum(n) {
  const d = new Date(n * 86400000);
  return `${d.getUTCFullYear()}-${pad2(d.getUTCMonth() + 1)}-${pad2(d.getUTCDate())}`;
}

/** 起算日 + 月数（日对齐，月末夹取），不减 1 天 */
function addMonths(iso, months) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso || ''));
  if (!m) return null;
  const total = Number(m[1]) * 12 + (Number(m[2]) - 1) + months;
  const ny = Math.floor(total / 12);
  const nm = (total % 12) + 1;
  const nd = Math.min(Number(m[3]), daysInMonth(ny, nm));
  return `${ny}-${pad2(nm)}-${pad2(nd)}`;
}

/** 保修期届满日 = 保修期起 + 保修期（月） − 1 日（含首日口径）；认不出返回 null */
function maturityOf(it) {
  const start = normDate(it.wStart);
  const months = normNumber(it.wMonths);
  if (start === null || months === null) return null;
  const added = addMonths(start, Math.trunc(months));
  const n = dayNum(added);
  if (n === null) return null;
  return fromDayNum(n - 1);
}

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: [], missingColumns: [], cols: [] };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i] };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      if (row[role] === undefined) row[role] = v;
      if (role === 'project' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) totals.push(row);
    else items.push(row);
  }
  return { items, totals, missingColumns, cols: headers };
}

const who = (it) => {
  const p = String(it.project === undefined ? '' : it.project).trim();
  const b = String(it.bill === undefined ? '' : it.bill).trim();
  if (p && b) return `项目「${p}」的结算单 ${b}`;
  if (p) return `项目「${p}」`;
  if (b) return `结算单 ${b}`;
  return `第 ${it.line} 行`;
};

const numOf = (it, role) => normNumber(it[role]);

/* ================================ 免费档检查项 ================================ */

function checkWithheld(it) {
  const settle = numOf(it, 'settle');
  const rate = rateRatio(it.rate);
  const stated = numOf(it, 'withheld');
  if (settle === null || rate === null || stated === null) return null;
  const expect = round2(settle * rate);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期扣留金额与复算不符', line: it.line,
    message: `${who(it)}的本期扣留金额是 ${stated.toFixed(2)}，`
      + `按 本期结算金额 ${settle.toFixed(2)} × 扣留比例 ${(rate * 100).toFixed(2)}% 应为 ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '扣留比例要按合同/结算单约定的那一档填（可写 3 / 3% / 0.03）；比例填错一档，整张台账的扣留额都会跟着错。',
  };
}

function checkMaturity(it) {
  const start = normDate(it.wStart);
  const months = normNumber(it.wMonths);
  const stated = normDate(it.wEnd);
  if (start === null || months === null || stated === null) return null;
  const expect = maturityOf(it);
  if (expect === null) return null;
  if (stated === expect) return null;
  return {
    level: 'P0', category: '保修期届满日与复算不符', line: it.line,
    message: `${who(it)}的保修期止是 ${stated}，按 保修期起 ${start} + ${Math.trunc(months)} 个月 − 1 日`
      + `（含首日口径）应为 ${expect}。`,
    advice: '届满日早算一个月会提前退款、晚算一个月会到期不退；把口径写进台账（含首日还是不包含首日）。',
  };
}

function checkRefund(it) {
  const cum = numOf(it, 'cum');
  const stated = numOf(it, 'refundAmt');
  if (cum === null || stated === null) return null;
  const deductRaw = numOf(it, 'deduct');
  const deduct = deductRaw === null ? 0 : deductRaw;
  const expect = round2(cum - deduct);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '退还金额与应退不符', line: it.line,
    message: `${who(it)}的退还金额是 ${stated.toFixed(2)}，按 累计扣留金额 ${cum.toFixed(2)} − `
      + `保修期内扣减 ${deduct.toFixed(2)}${deductRaw === null ? '（该列为空，按 0 计）' : ''} 应为 ${expect.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`,
    advice: '退还时必须"累计扣留 − 保修期内扣减 = 实退"三处对得上；扣减有依据就在台账上写明，别只在备注里说。',
  };
}

function checkDateOrder(it) {
  const out = [];
  const start = normDate(it.wStart);
  const end = normDate(it.wEnd);
  const back = normDate(it.refundDate);
  if (start !== null && end !== null && end < start) {
    out.push({
      level: 'P0', category: '日期倒挂：届满日早于保修期起', line: it.line,
      message: `${who(it)}的保修期止（${end}）早于保修期起（${start}），这个顺序不成立。`,
      advice: '保修期起与届满日填反了，或者保修期月数填成了负数；到期判定会全错。',
    });
  }
  if (start !== null && back !== null && back < start) {
    out.push({
      level: 'P1', category: '日期倒挂：退还日期早于保修期起', line: it.line,
      message: `${who(it)}的实际退还日期（${back}）早于保修期起（${start}）。`,
      advice: '退还日期不可能早于保修期起算日；先确认这一行是不是串了别的项目。',
    });
  }
  return out;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = numOf(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = numOf(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: t.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
        + `相差 ${round2(stated - sum).toFixed(2)}。`,
      advice: '要么明细行漏了结算单，要么合计行没跟着更新；合计行对不上时别急着往下签字。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.bill === undefined ? '' : it.bill).trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '重复结算单号', line: it.line,
        message: `结算单号「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一结算单号出现两次会把扣留额与退还额一起翻倍；多标段请按结算单号分行而不是重复贴。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格这笔质保金就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
    for (const role of DATE_ROLES) {
      const s = String(it[role] === undefined ? '' : it[role]).trim();
      if (s === '' || isBlank(s)) continue;
      if (normDate(s) === null) {
        out.push({
          level: 'P0', category: '日期无法识别', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是「${s}」，认不出是哪一天。`,
          advice: '日期请写成 2024-05-01 / 2024/5/1 / 20240501 / 2024年5月1日 这几种之一；认不出的日期本工具不做猜测。',
        });
      }
    }
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到台账正文（text）—— 请把含表头的质保金台账贴进来');
  }
  const t = parseTable(text);
  // ⚠️ 空数组在 JS 里是**真值**：`if ([])` 会成立 —— 必须判长度，否则「没缺列」也会被当成缺列。
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账表头缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(String(text).split(/\r?\n/)[0]).join(' / ')}`,
      '从结算单/竣工结算书导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何结算单明细行');
  }

  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const a = checkWithheld(it); if (a) findings.push(a);
    const b = checkMaturity(it); if (b) findings.push(b);
    const c = checkRefund(it); if (c) findings.push(c);
    for (const d of checkDateOrder(it)) findings.push(d);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  

  const byLine = (x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category));
  findings.sort(byLine);
  const summarize = (list) => {
    const q0 = list.filter((f) => f.level === 'P0').length;
    const q1 = list.filter((f) => f.level === 'P1').length;
    const q2 = list.filter((f) => f.level === 'P2').length;
    return {
      rows: t.items.length,
      total: list.length,
      p0: q0,
      p1: q1,
      p2: q2,
      verdict: q0 > 0 ? 'ERROR_FOUND' : (list.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    };
  };

  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = numOf(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const cumTotal = sumOf('cum');
  let refundedTotal = 0;
  for (const it of t.items) {
    const r = numOf(it, 'refundAmt');
    if (r !== null) refundedTotal += r;
  }
  refundedTotal = round2(refundedTotal);

  let noteText = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`;


  const result = {
    status: 'success',
    service_type: 'RETENTION_MONEY_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_executed: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      settle_total: sumOf('settle'),
      withheld_total: sumOf('withheld'),
      paid_in_total: cumTotal,
      refunded_total: refundedTotal,
      deducted_total: sumOf('deduct'),
      outstanding_total: round2(cumTotal - refundedTotal),
      rate_convention: '扣留比例可写 3 / 3% / 0.03，均按 3% 理解',
      date_convention: '保修期届满日 = 保修期起 + 保修期（月） − 1 日（含首日口径）；日期可写 2024-05-01 / 2024/5/1 / 20240501 / 2024年5月1日',
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: summarize(findings),
    checks_out_of_scope: OUT_OF_SCOPE,
    note: noteText,
    disclaimer: '只核对台账内部的算术与勾稽，不判断扣留比例是否合法、不算逾期资金占用费、不评价维修扣款本身是否该扣；'
      + '每条结论都带原文行号，可由第三方用同一份输入复算。',
  };



  if (findings.length === 0) {
      result.verdict_note = '本次实际执行的免费检查项都通过了。这只说明这张台账按免费口径算得对；'
        + '扣留比例上限、保修期内扣减合理性、应退未退排期与催办清单这几类检查本次没有执行，'
        + '见 scope.checks_not_run。';
    
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, rateRatio, round2, isBlank, normDate, dayNum, addMonths, maturityOf, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, RATE_CAP, TOL,
};
