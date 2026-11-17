'use strict';
/**
 * progress-output-check.js —— 工程进度款与产值确认核对（免费档 / 完整档共用源码）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），不写盘、不读环境变量。
 *
 * 真实痛点：施工/工程类企业每月报进度款，先由项目部报「本期申请产值」，再由监理/业主做
 * 「产值确认」把申请核成「本期确认产值」，然后才按合同支付比例算钱：
 *   ① 本期应付进度款 = 本期**确认**产值 × 支付比例（常见 80%；基数用申请产值就会多付）
 *   ② 累计确认产值   = 上期累计确认产值 + 本期确认产值（滚动栏最常忘了跟着改）
 *   ③ 本期实付       = 本期应付进度款 − 本期扣质保金
 * 单笔动辄几十上百万，把申请产值当确认产值去乘比例、或累计栏没更新，都是"表算错了但没人看得出来"
 * 的典型错法；这些全是纯算术，几十个标段人眼核不动。每一步都带原文行号，第三方可按同口径复算。
 *
 * 与已有能力的区别：`progress-payment-check` 核「进度款与质保金」的三种比例算法；
 * 本能力核的是**产值确认口径**：申请 vs 确认、累计确认滚动、确认值 × 比例、合计勾稽与空缺。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不判工程实体是否真的完成、不给造价/法律意见；材料不足不给结论。
 *
 * ⚠️ 完整档（付费）的实现集中在下面那一行 MARKER 与 `function run(` 之间，
 *    免费包会**整块**摘掉它；免费包只保留免费检查项。
 */

const CHECKS_GIVEN = [
  '本期确认产值与本期申请产值不符（核减/核增未说明）',
  '本期应付进度款勾稽（本期确认产值 × 支付比例）',
  '累计确认产值勾稽（上期累计确认产值 + 本期确认产值）',
  '本期实付勾稽（本期应付进度款 − 本期扣质保金）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复标段/合同行与关键字段空缺检测',
];

const CHECKS_WITHHELD = [
  '跨标段汇总台账（逐标段汇总合同、确认产值、应付与实付，按影响金额排序）',
  '核减/核增差异归因（把申请与确认的差额按金额排序，指出先问哪几笔）',
  '累计确认产值超过合同金额检测（超合同/超付风险）',
  '支付比例越界（0~100%）与本期实付为负检测',
];

const OUT_OF_SCOPE = [
  '判断现场是否真的完成了这些产值（那是监理计量、现场签证与验收资料的事）',
  '判断产值确认单上的签字/盖章/审批流程是否真实有效（那是业主与监理的审批流程）',
  '处理甲供材、暂列金额、变更签证、索赔、罚款、水电费代扣等口径差异（请先算进本期申请产值或另行列示）',
  '处理多级分包、总包代扣税与农民工工资专户扣款（口径按合同与当地规定，需逐项确认）',
  '判断合同金额、支付比例与质保金比例本身是否合理或合法（那是合同与招投标文件的事）',
  '读取 .xlsx/.pdf 原文件（需要你先导出成文本贴进来）',
];

/** 干净样例：一张算得对的进度款申请与产值确认表（两档都必须 0 条问题） */
const SAMPLE_TEXT = [
  '标段\t合同金额\t上期累计确认产值\t本期申请产值\t本期确认产值\t累计确认产值\t支付比例\t本期应付进度款\t本期扣质保金\t本期实付',
  'A标段\t5000000.00\t2400000.00\t800000.00\t800000.00\t3200000.00\t80%\t640000.00\t19200.00\t620800.00',
  'B标段\t3000000.00\t1600000.00\t400000.00\t400000.00\t2000000.00\t80%\t320000.00\t16000.00\t304000.00',
  '合计\t8000000.00\t4000000.00\t1200000.00\t1200000.00\t5200000.00\t\t960000.00\t35200.00\t924800.00',
].join('\n');

/** 金额容差：0.01 元（表里都是两位小数，四舍五入到分以后要能对齐） */
const TOL = 0.01;

/**
 * 表头 → 角色的关键词表。
 * ⚠️ **顺序即优先级**：更具体的角色必须排在更宽泛的角色前面，否则宽泛词会把具体列抢走
 *    （例如「累计确认产值」「上期累计确认产值」都会被「确认产值」抢走 ⇒ 列被覆盖、静默算错）。
 */
const ROLES = {
  party: ['标段', '项目名称', '工程名称', '合同名称', '单位名称'],
  contract: ['合同金额', '合同价', '签约合同价'],
  priorCum: ['上期累计确认产值', '上期累计确认', '期初累计确认产值', '上期累计'],
  cumApproved: ['累计确认产值', '累计核定产值', '累计确认'],
  applied: ['本期申请产值', '本期申请', '申请产值', '本期报量'],
  approved: ['本期确认产值', '本期核定产值', '本期确认', '确认产值'],
  rate: ['支付比例', '进度款比例', '付款比例', '支付率'],
  payable: ['本期应付进度款', '本期应付', '应付进度款'],
  retention: ['本期扣质保金', '本期质保金', '扣质保金', '质保金'],
  paid: ['本期实付', '本期支付金额', '实付金额'],
};

const LABELS = {
  party: '标段', contract: '合同金额', priorCum: '上期累计确认产值', cumApproved: '累计确认产值',
  applied: '本期申请产值', approved: '本期确认产值', rate: '支付比例',
  payable: '本期应付进度款', retention: '本期扣质保金', paid: '本期实付',
};

/** 必需列：缺一个就**不给结论**（宁可说"材料不足"，也不套默认值） */
const REQUIRED = ['party', 'applied', 'approved', 'priorCum', 'cumApproved', 'rate', 'payable', 'retention', 'paid'];

/** 可以逐列复核合计的金额列（比例列不参与求和） */
const SUM_ROLES = ['contract', 'priorCum', 'applied', 'approved', 'cumApproved', 'payable', 'retention', 'paid'];

const BASIS = '本期应付进度款 = 本期确认产值 × 支付比例；累计确认产值 = 上期累计确认产值 + 本期确认产值；'
  + '本期实付 = 本期应付进度款 − 本期扣质保金；合计行逐列复核。';

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: advice || '请补上这些再跑；材料不足时本工具不做任何认定，也不会套用 0 或默认值替你填。',
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

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥$,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  const n = Number(t);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

const money = (n) => Number(n).toFixed(2);

function roleOf(header) {
  const h = String(header === undefined || header === null ? '' : header).replace(/[\s（）()：:]/g, '');
  if (!h) return null;
  for (const role of Object.keys(ROLES)) {
    if (ROLES[role].some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

/**
 * 解析：把整段文本当成"第一张非空行是表头、其余是数据行"的表。
 * 返回 { header, cols, items, totals, missingColumns, missingRoles } 或 { error }。
 * `line` 是**原文行号**（1 起，跳过空行时也保留真实行号），结论据此可回查原文。
 */
function parseTable(text) {
  const all = String(text === undefined || text === null ? '' : text).split(/\r?\n/);
  const idx = [];
  for (let i = 0; i < all.length; i++) if (all[i].trim() !== '') idx.push(i);
  if (!idx.length) {
    return { error: 'empty', header: [], cols: [], items: [], totals: [], missingColumns: [], missingRoles: [] };
  }
  const header = splitRow(all[idx[0]]);
  const cols = header.map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return {
      error: 'no_header', header, cols, items: [], totals: [],
      missingColumns: missingRoles.map((r) => LABELS[r]), missingRoles,
    };
  }
  const items = [];
  const totals = [];
  for (let k = 1; k < idx.length; k++) {
    const i = idx[k];
    const cells = splitRow(all[i]);
    const byRole = {};
    cols.forEach((c, ci) => {
      if (c.role && byRole[c.role] === undefined) {
        byRole[c.role] = cells[ci] === undefined ? '' : cells[ci];
      }
    });
    const row = { line: i + 1, raw: all[i], byRole };
    const first = String(cells[0] === undefined ? '' : cells[0]).trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { header, cols, items, totals, missingColumns: [], missingRoles: [] };
}

const num = (it, role) => normNumber(it.byRole[role]);
const who = (it) => {
  const p = String(it.byRole.party === undefined || it.byRole.party === null ? '' : it.byRole.party).trim();
  return `标段「${p || '(未命名)'}」`;
};

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

/* =========================== 免费档：逐行检查 =========================== */

/** ① 申请 vs 确认：产值确认就是"核"这一步，核减/核增必须在表里有依据 */
function checkAppliedVsApproved(it, ev) {
  const applied = num(it, 'applied');
  const approved = num(it, 'approved');
  if (applied === null || approved === null) return null;
  const diff = round2(applied - approved);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P1', category: '本期确认产值与本期申请产值不符', line: it.line, amount: Math.abs(diff),
    message: `${who(it)}本期申请产值 ${money(applied)}，本期确认产值 ${money(approved)}，`
      + `${diff > 0 ? '核减' : '核增'} ${money(Math.abs(diff))}；进度款只能按确认产值算。`,
    evidence: ev(it.line),
    advice: '核减/核增要有监理计量或业主审批依据；把依据写进本表备注列，或按确认口径重算应付进度款。',
  };
}

/** ② 本期应付进度款 = 本期确认产值 × 支付比例 */
function checkPayable(it, ev) {
  const approved = num(it, 'approved');
  const rate = num(it, 'rate');
  const stated = num(it, 'payable');
  if (approved === null || rate === null || stated === null) return null;
  const expect = round2(approved * rate / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期应付进度款与复算不符', line: it.line, amount: Math.abs(round2(stated - expect)),
    message: `${who(it)}本期应付进度款填 ${money(stated)}，按 本期确认产值 ${money(approved)} × ${rate}% 复算应为 ${money(expect)}，`
      + `相差 ${money(round2(stated - expect))}。`,
    evidence: ev(it.line),
    advice: '基数是**本期确认产值**（不是申请产值）；比例按合同约定（常见 80%），两者任一录错都会直接变成钱。',
  };
}

/** ③ 累计确认产值 = 上期累计确认产值 + 本期确认产值（滚动栏最常忘了改） */
function checkCumApproved(it, ev) {
  const prior = num(it, 'priorCum');
  const approved = num(it, 'approved');
  const stated = num(it, 'cumApproved');
  if (prior === null || approved === null || stated === null) return null;
  const expect = round2(prior + approved);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '累计确认产值与复算不符', line: it.line, amount: Math.abs(round2(stated - expect)),
    message: `${who(it)}累计确认产值填 ${money(stated)}，按 上期累计确认 ${money(prior)} + 本期确认 ${money(approved)} 复算应为 ${money(expect)}，`
      + `相差 ${money(round2(stated - expect))}。`,
    evidence: ev(it.line),
    advice: '累计栏要跟着本期确认值滚动更新；累计值错会一路污染后续月份的超合同判断。',
  };
}

/** ④ 本期实付 = 本期应付进度款 − 本期扣质保金 */
function checkPaidAmount(it, ev) {
  const payable = num(it, 'payable');
  const retention = num(it, 'retention');
  const stated = num(it, 'paid');
  if (payable === null || retention === null || stated === null) return null;
  const expect = round2(payable - retention);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期实付与复算不符', line: it.line, amount: Math.abs(round2(stated - expect)),
    message: `${who(it)}本期实付填 ${money(stated)}，按 本期应付 ${money(payable)} − 本期扣质保金 ${money(retention)} 复算应为 ${money(expect)}，`
      + `相差 ${money(round2(stated - expect))}。`,
    evidence: ev(it.line),
    advice: '实付 = 应付 − 质保金；若还有代扣税、水电费、罚款，先在本表里显式列出来再算，别只在实付栏里"抹平"。',
  };
}

/** ⑤ 合计行逐列复核 */
function checkTotalRow(totals, items, role, ev) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: t.line, amount: Math.abs(round2(stated - sum)),
      message: `合计行「${LABELS[role]}」填 ${money(stated)}，${items.length} 个明细行相加是 ${money(sum)}，`
        + `相差 ${money(round2(stated - sum))}。`,
      evidence: ev(t.line),
      advice: '要么明细行漏了一个标段，要么合计行没跟着更新；改完合计行再往下走。',
    });
  }
  return out;
}

/** ⑥a 同一标段/合同出现多行 */
function checkDuplicates(items, ev) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.party === undefined || it.byRole.party === null ? '' : it.byRole.party).trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一标段出现多行', line: it.line, amount: 0,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        evidence: ev(it.line),
        advice: '同一标段分次报量是正常的；但若本表按标段汇总，重复行会让应付与实付一起翻倍——先确认是不是合并表。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

/** ⑥b 关键字段空缺或占位符 */
function checkBlanks(items, ev) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      const raw = it.byRole[role];
      const s = String(raw === undefined || raw === null ? '' : raw).trim();
      if (isBlank(raw) || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line, amount: 0,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          evidence: ev(it.line),
          advice: '缺这一格这笔进度款就算不出来；补齐前本工具不会用 0 或默认值替你填，也不会给结论。',
        });
      }
    }
  }
  return out;
}

function countLevels(findings) {
  const lv = { p0: 0, p1: 0, p2: 0 };
  for (const f of findings) {
    if (f.level === 'P0') lv.p0 += 1;
    else if (f.level === 'P1') lv.p1 += 1;
    else lv.p2 += 1;
  }
  return lv;
}

const byPosition = (a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category));

function buildSummary(t, findings, ledger) {
  const lv = countLevels(findings);
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));
  const s = {
    sections: t.items.length,
    total: findings.length,
    p0: lv.p0,
    p1: lv.p1,
    p2: lv.p2,
    omitted: 0,
    applied_total: sumOf('applied'),
    approved_total: sumOf('approved'),
    variance_total: round2(sumOf('applied') - sumOf('approved')),
    payable_total: sumOf('payable'),
    retention_total: sumOf('retention'),
    paid_total: sumOf('paid'),
    verdict: lv.p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
    basis: BASIS,
  };
  if (ledger) {
    s.ledger_rows = ledger.rows.length;
    s.action_items = ledger.action_items.length;
  }
  return s;
}

function run(payload) {
  const p = payload;
  if (p !== undefined && p !== null && typeof p !== 'object') {
    return insufficient([`入参不是对象（收到的是 ${typeof p}）`], '用法：{"text":"（把表头和数据行一起复制进来，Tab 分隔最稳）"}');
  }
  if (!p) {
    return insufficient(['原文（text）', '进度款申请与产值确认表的表头与数据行'],
      '用 {"text":"…"} 传材料；或先用 --sample 看看需要什么格式。');
  }
  const raw = p.text !== undefined ? p.text : p.content;
  const text = Array.isArray(raw) ? raw.join('\n') : raw;
  if (!String(text === undefined || text === null ? '' : text).trim()) {
    return insufficient(['原文（text）', '进度款申请与产值确认表的表头与数据行（Tab 分隔最稳）'],
      '把表头和你关心的数据行一起复制成文本贴进来，别只贴合计行。');
  }
  const srcName = String(p.file || p.name || p.filename || '进度款申请与产值确认表').trim() || '进度款申请与产值确认表';
  const ev = (line) => `${srcName}:${line}`;

  const t = parseTable(text);
  if (t.error === 'empty') {
    return insufficient(['原文（text）', '至少一行表头'], '贴进来的内容全是空白。');
  }
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的进度款申请与产值确认表（要能认出「本期申请产值」「本期确认产值」「上期累计确认产值」'
      + '「累计确认产值」「支付比例」「本期应付进度款」「本期扣质保金」「本期实付」）',
      `本次没认出来的列：${t.missingColumns.join('、')}`,
      '从计量支付台账导出后**连同表头**一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) {
    return insufficient(['至少一个标段的明细行（表头下面至少一行数据）'],
      '只给了表头（或只有合计行）无法核对；把明细行一起贴进来。');
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkAppliedVsApproved(it, ev); if (a) findings.push(a);
    const b = checkPayable(it, ev); if (b) findings.push(b);
    const c = checkCumApproved(it, ev); if (c) findings.push(c);
    const d = checkPaidAmount(it, ev); if (d) findings.push(d);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role, ev)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items, ev)) findings.push(f);
  for (const f of checkBlanks(t.items, ev)) findings.push(f);
  findings.sort(byPosition);

  const result = {
    status: 'success',
    service_type: 'PROGRESS_OUTPUT_CHECK',
    source: srcName,
    columns: t.cols.map((c) => c.header),
    findings,
    summary: buildSummary(t, findings),
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: CHECKS_WITHHELD.slice(),
      sections: t.items.length,
      total_rows: t.totals.length,
      executed_locally: true,
      network_used: false,
    },
    checks_given: CHECKS_GIVEN.slice(),
    checks_withheld: CHECKS_WITHHELD.slice(),
    checks_executed: CHECKS_GIVEN.slice(),
    checks_not_run: CHECKS_WITHHELD.slice(),
    checks_out_of_scope: OUT_OF_SCOPE,
    basis: BASIS,
    disclaimer: '只核这张表内部的算术与勾稽：结论都带**原文行号**、可由第三方用同一口径复算；'
      + '不代替监理计量与业主确认，不做造价或法律意见，也不判断合同条款本身。',
  };

  if (findings.length === 0) {
    result.note = '本次执行的检查项都没有报出问题 —— 这只说明**这张表按上面写明的口径算得对**，'
      + '不代表产值计量真实、也不代表合同约定本身合理，那些不在本工具范围内。';
  } else {
    result.note = `本次共报出 ${findings.length} 条需要复核的问题（P0 ${result.summary.p0} 条 / P1 ${result.summary.p1} 条），`
      + '每条都带原文行号与出处，可以按同一口径复算。';
  }

  // 完整档开关：只在这一行判断档位（免费包里这一行会被整行摘掉）
    result.scope.tier = 'free';
  

  return { status: 'success', result };
}

// ⛔ 第 286 轮：骨架原来只导出 4 个名字 ⇒ 新包从一开始就不满足引擎契约
//    （各守卫都要 parseTable/roleOf/OUT_OF_SCOPE），每个子代理都得自己补。这里一次给全。
module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
