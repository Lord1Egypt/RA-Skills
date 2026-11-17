'use strict';
/**
 * insurance-agency-fee-check.js —— 保险代理手续费与佣金结算核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**每月结算期**。保险中介 / 代理公司每个月都要把各家保司
 * 结算的手续费（首期佣金 / 续期佣金 / 附加佣金）与保单明细逐笔勾稽：
 * 应收多少、退保追回多少、代扣税费多少、实收净额多少，一条都不能含糊。
 * 这张表对不上，方向只有两个 —— **少结（白干）** 或 **多结 / 重复计佣**（要被保司追回），
 * 两个都会传导到开票与增值税申报上。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   应收手续费 = 保费金额 × 手续费率
 *   实收净额   = 应收手续费 − 退保追回 − 代扣税费
 *   合计行各列 = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**手续费率该定多少、是否符合监管对佣金上限的规定，也不判断退保追回
 *    该怎么跨期分摊（那属于代理协议、监管口径与会计判断）：表里给的保费金额、本期费率、
 *    协议费率、退保追回、代扣税费一律**以你填的为准**，本工具只核表内勾稽，
 *    并把可疑处按原文行号列出来。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约（所有引擎一致，别改名字）：
 *   run(payload) -> {status:'success', result} | {status:'insufficient_input', missing, advice}
 *   CHECKS_GIVEN / CHECKS_WITHHELD     免费版执行 / 不执行的检查项（免费包据此**如实列出未执行项**）
 *   OUT_OF_SCOPE                       本能力**根本不做**的判断（边界诚实）
 *   SAMPLE_TEXT                        样例输入（免费包 --sample 用它自检）
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的完整档开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出那个开关的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '应收手续费复算（保费金额 × 手续费率 = 应收手续费）',
  '实收净额复算（应收手续费 − 退保追回 − 代扣税费 = 实收净额）',
  '合计行逐列复核',
  '同一保单号同一期间重复行检测',
  '空白与占位符检测',
  '金额或费率为负检测',
];

const CHECKS_WITHHELD = [
  '手续费率与代理协议不一致提示',
  '退保追回超过已结手续费提示',
  '实收净额为负提示',
  '同一保单重复结算同一期间提示',
  '首期/续期标识与保单年度不一致提示',
];

const OUT_OF_SCOPE = [
  '判断手续费率 / 佣金比例该定多少、是否符合监管对保险中介佣金上限的规定（那属于代理协议与合规口径，请找合规负责人）',
  '核对开票金额、发票税率与发票信息是否正确，也不做增值税申报（本工具只核结算表内的算术勾稽）',
  '判断退保追回该不该跨期分摊、该冲减哪一期的手续费收入（那属于收入确认的会计判断，请咨询会计师）',
  '判断手续费是否已经到账（以银行流水与保司结算单为准，需要你先导出成文本贴进来）',
  '校验保单本身的承保信息（投保人、险种、保额、生效日与佣金结算的对应关系，一律以保司结算单为准）',
];

/* 干净样例：4 行明细 + 合计行，两档都必须 0 命中。
   第 1 行 中国人寿 100000 × 15% = 15000，净额 15000 − 0 − 900 = 14100
   第 2 行 平安财险  50000 × 12% =  6000，净额 6000 − 0 − 360 = 5640
   第 3 行 中国人寿 100000 ×  5% =  5000，净额 5000 − 0 − 300 = 4700（续期，保单年度 2）
   第 4 行 太平洋    80000 × 10% =  8000，净额 8000 − 1500 − 480 = 6020（续期，保单年度 2）
   合计行 = 各列之和：保费 330000 / 应收 34000 / 追回 1500 / 代扣 2040 / 净额 30460 */
const SAMPLE_TEXT = [
  '所属期间\t保险公司\t销售渠道\t保单号\t手续费类型\t保单年度\t保费金额\t手续费率\t协议手续费率\t应收手续费\t退保追回\t代扣税费\t实收净额',
  '2026-01\t中国人寿\t直营\tP2026001\t首期佣金\t1\t100000.00\t15.00%\t15.00%\t15000.00\t0.00\t900.00\t14100.00',
  '2026-01\t平安财险\t经纪\tP2026002\t首期佣金\t1\t50000.00\t12.00%\t12.00%\t6000.00\t0.00\t360.00\t5640.00',
  '2026-02\t中国人寿\t直营\tP2026001\t续期佣金\t2\t100000.00\t5.00%\t5.00%\t5000.00\t0.00\t300.00\t4700.00',
  '2026-02\t太平洋保险\t网销\tP2026003\t续期佣金\t2\t80000.00\t10.00%\t10.00%\t8000.00\t1500.00\t480.00\t6020.00',
  '合计\t\t\t\t\t\t330000.00\t\t\t34000.00\t1500.00\t2040.00\t30460.00',
].join('\n');

const TOL = 0.01;             // 金额容差：1 分
const RATE_TOL = 0.0005;      // 费率容差：0.05 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前（roleOf 按这个顺序取第一个命中的别名）。
  //    · 「协议手续费率」必须排在「手续费率」前，否则协议那一列会被本期费率列整列抢走；
  //    · 「续期佣金 / 首期佣金 / 附加佣金」（手续费类型这一列的写法）必须排在「佣金」（应收金额列的兜底别名）前；
  //    · 「保费金额」必须排在所有带「金额」的列（应收手续费金额 / 追回金额 / 实收金额）前；
  //    · 「手续费类型」必须排在「手续费 / 佣金」前，否则整列类型会被当成应收金额。
  period: ['所属期间', '结算期间', '会计期间', '结算月份', '所属期', '期间', '月份'],
  insurer: ['保险公司名称', '保险公司', '承保公司', '保司'],
  channel: ['销售渠道', '业务渠道', '来源渠道', '出单渠道', '渠道'],
  policyNo: ['保单编号', '保单号码', '保单号', '投保单号'],
  feeType: ['手续费类型', '佣金类型', '费用类型', '手续费项目', '佣金项目', '手续费科目', '佣金科目',
    '续期佣金', '首期佣金', '附加佣金', '费用名称', '类型'],
  policyYear: ['保单年度', '保险年度', '承保年度', '年度'],
  premium: ['保费金额', '保费收入', '承保保费', '规模保费', '投保金额', '保费'],
  agreementRate: ['协议手续费率', '协议佣金率', '约定手续费率', '合同手续费率', '代理协议费率', '协议费率'],
  feeRate: ['手续费率', '佣金率', '手续费比例', '佣金比例', '费率'],
  feeDue: ['应收手续费金额', '应收手续费', '应收佣金', '应结手续费', '手续费金额', '佣金金额', '佣金', '手续费'],
  clawback: ['退保追回', '退保追偿', '退保扣回', '退保冲回', '追回金额', '扣回金额', '扣回'],
  taxWithheld: ['代扣税费', '代扣税金', '代扣增值税', '代扣税', '扣税金额', '税费', '税金'],
  feeNet: ['实收净额', '实收手续费', '结算净额', '净结算额', '实收金额', '实收', '净额'],
};

const LABELS = {
  period: '所属期间', insurer: '保险公司', channel: '销售渠道', policyNo: '保单号',
  feeType: '手续费类型', policyYear: '保单年度', premium: '保费金额', feeRate: '手续费率',
  agreementRate: '协议手续费率', feeDue: '应收手续费', clawback: '退保追回',
  taxWithheld: '代扣税费', feeNet: '实收净额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数）。销售渠道是选填。 */
const REQUIRED = ['period', 'insurer', 'policyNo', 'feeType', 'policyYear', 'premium',
  'feeRate', 'agreementRate', 'feeDue', 'clawback', 'taxWithheld', 'feeNet'];
/** 合计行逐列复核的列（这几列都可以按明细行相加） */
const SUM_ROLES = ['premium', 'feeDue', 'clawback', 'taxWithheld', 'feeNet'];
/**
 * 免费档负值检测覆盖的列：**保费与费率**这一侧。
 * ⚠️ 刻意**不含**退保追回、代扣税费、实收净额：
 *    · 退保追回为负是"冲回"、代扣税费为负是"多扣退税"，都属于红字调整的正常写法，
 *      该不该这么记是会计判断（见 OUT_OF_SCOPE），不由本工具下结论；
 *    · 实收净额为负是**完整档**的独立检查项（见 CHECKS_WITHHELD）——
 *      免费档提前把它报出来，就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['premium', 'feeDue', 'feeRate', 'agreementRate'];
/** 首期 / 续期标识（手续费类型列的取值写法） */
const FIRST_WORDS = /首期|首年|首次|新单/;
const RENEW_WORDS = /续期|续年|续保|续收/;
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|合计：)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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

/** 费率归一化成小数：`15%` ⇒ 0.15；`0.15` ⇒ 0.15；`15` ⇒ 0.15 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null };
  const headers = splitRow(raw[0]);
  const roles = headers.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    roles.forEach((role, c) => {
      if (!role) return;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (role === 'period' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.insurer, it && it.channel, it && it.policyNo]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const policyKeyOf = (it) => {
  const p = it && it.policyNo !== undefined ? String(it.policyNo).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const feeTypeKeyOf = (it) => {
  const t = it && it.feeType !== undefined ? String(it.feeType).trim() : '';
  return t || '（未填手续费类型）';
};

/** 金额展示：认不出的值照原样说"空"，绝不显示成 0.00 */
function amountText(raw) {
  const v = normNumber(raw);
  return v === null ? '（空）' : v.toFixed(2);
}

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkFeeDueRecompute(it) {
  const out = [];
  const premium = normNumber(it.premium);
  const rate = rateValue(it.feeRate);
  const stated = normNumber(it.feeDue);
  if (premium === null || rate === null || stated === null) return out;
  const expect = round2(premium * rate);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应收手续费复算不符', line: it.line,
    message: `${who(it)}：保费金额 ${premium.toFixed(2)} × 手续费率 ${(rate * 100).toFixed(4)}% = ${expect.toFixed(2)}，`
      + `表里「应收手续费」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '应收手续费就是"保费 × 费率"：算少了是白干，算多了保司结算时会追回，两头都是钱。',
  });
  return out;
}

function checkNetRecompute(it) {
  const out = [];
  const due = normNumber(it.feeDue);
  const clawback = normNumber(it.clawback);
  const tax = normNumber(it.taxWithheld);
  const stated = normNumber(it.feeNet);
  if (due === null || clawback === null || tax === null || stated === null) return out;
  const expect = round2(due - clawback - tax);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '实收净额复算不符', line: it.line,
    message: `${who(it)}：应收手续费 ${due.toFixed(2)} − 退保追回 ${clawback.toFixed(2)} − 代扣税费 ${tax.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「实收净额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '实收净额是打款与开票的口径：差一分，账上的收入与增值税都会跟着差。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v !== null) { sum += v; n += 1; }
    }
    if (!n) continue;
    const expect = round2(sum);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行是开票与保司对账的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const no = it.policyNo !== undefined ? String(it.policyNo).trim() : '';
    if (!p || !no) continue;
    const key = `${p}|${no}|${feeTypeKeyOf(it)}|${amountText(it.premium)}|${amountText(it.feeDue)}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一保单号同一期间重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过（同一保单号、同一所属期间、同一手续费类型，金额也一样），`
          + `第 ${it.line} 行又出现一次 —— 多半是复制粘贴带重了。重复行会把应收与实收都重复计一遍。`,
      });
    } else seen.set(key, it.line);
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪列就补哪列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const isRate = role === 'feeRate' || role === 'agreementRate';
    const v = isRate ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = isRate ? `${(v * 100).toFixed(4)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '金额或费率为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 保费金额与手续费率都不该为负；`
        + '红字冲回应单独列示并在备注里说明，别混在结算行里。',
    });
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
    return insufficient('没有收到保险代理手续费与佣金结算核对表正文（text）—— 请把「所属期间 / 保险公司 / 销售渠道 / 保单号 / 手续费类型 / 保单年度 / 保费金额 / 手续费率 / 协议手续费率 / 应收手续费 / 退保追回 / 代扣税费 / 实收净额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `保险代理手续费与佣金结算核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何手续费结算明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkFeeDueRecompute(it));
    findings.push(...checkNetRecompute(it));
    findings.push(...checkNegative(it));

  }

  findings.push(...checkTotalRow(t.totals, t.items));
  findings.push(...checkDuplicates(t.items));
  findings.push(...checkBlanks(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const totalsOf = (role) => {
    let s = 0;
    for (const it of t.items) {
      const v = normNumber(it[role]);
      if (v !== null) s += v;
    }
    return round2(s);
  };

  const result = {
    status: 'success',
    service_type: 'INSURANCE_AGENCY_FEE_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      premium_total: totalsOf('premium'),
      fee_due_total: totalsOf('feeDue'),
      clawback_total: totalsOf('clawback'),
      tax_withheld_total: totalsOf('taxWithheld'),
      fee_net_total: totalsOf('feeNet'),
      tolerance: TOL,
      rate_tolerance: RATE_TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: groups.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"保费金额 × 手续费率 = 应收手续费"与"应收手续费 − 退保追回 − 代扣税费 = 实收净额"这类**表内勾稽**与档位提示，'
      + '**不判断手续费率该定多少、是否符合监管上限，也不判断退保追回该跨哪一期**（以代理协议、保司结算单与会计师口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
