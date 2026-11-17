/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * membership-liability-check.js —— 会员卡预收与履约负债核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**月末结账 / 门店盘点 / 会员卡专项审计之前**，
 * 财务要把会员卡的预收负债（卡里还没消费掉的余额）与履约进度（已经核销掉的次数）核一遍：
 * 卖卡收到的钱先记成负债，会员每核销一次才把一部分负债结转为收入。
 * 这张表错一处会同时错三处 —— 预收负债错、收入错、门店业绩错；
 * 而会员卡预收**恰好是最容易被拿去调节收入与业绩的科目**，审计必查。
 *
 * 自包含：只用 Node.js 标准库；不 require 本包以外的任何文件；
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）；不写盘；不读环境变量。
 *
 * 核心可算关系（都能用同一份输入手算复现）：
 *   本期核销金额 = 核销次数 × 单次确认价
 *   期末负债     = 期初负债 + 本期销售 − 本期核销 − 过期作废
 *   本期核销金额 ≤ 期初负债 + 本期销售（不能核销掉卡里没有的钱）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。
 * 材料不足时**绝不给结论**：不认定"一致"，也不认定"不一致"，更不输出"未发现问题"。
 * ⚠️ 本工具**不判断会员章程/卡政策本身是否合规**（有效期多长、作废比例上限由你的章程决定），
 *    只核这张台账的内部勾稽与政策口径一致性。
 */

const CHECKS_GIVEN = [
  '本期核销金额逐行复算（核销金额 = 核销次数 × 单次确认价）',
  '期末负债勾稽（期初负债 + 本期销售 − 本期核销 − 过期作废 = 期末负债，逐行 + 合计行）',
  '核销金额超过卡内可用余额检测',
  '同一会员卡号重复销售检测',
  '过期作废金额与政策一致性检测（不得为负、不得超过可用余额）',
  '关键字段缺失/占位符与负数检测',
];

const CHECKS_WITHHELD = [
  '跨门店/跨卡种汇总台账（门店负债合计与卡种核销率）',
  '负债差异归因（核销口径 / 作废政策 / 跨期归属 / 重复销售）',
  '按负债差异金额排序的处理清单',
  '跨期归属：期初有余额但本期无任何变动检测',
  '卡种归集完整性（卡种缺失时无法按卡种汇总）',
];

const OUT_OF_SCOPE = [
  '判断会员章程/卡政策本身是否合规（有效期多长、过期作废比例上限由你的章程决定）',
  '判断收入确认时点与履约进度（那属于会计准则判断，请咨询会计师）',
  '处理含税/不含税口径、赠送卡与折扣卡的金额拆分',
  '读取会员系统或 ERP 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '会员卡号\t会员姓名\t卡种\t门店\t期初负债\t本期销售金额\t核销次数\t单次确认价\t本期核销金额\t过期作废金额\t期末负债',
  'MC2025001\t张伟\t年卡\t郑州中原店\t1200.00\t600.00\t5\t100.00\t500.00\t0.00\t1300.00',
  'MC2025002\t李娜\t季卡\t郑州金水店\t300.00\t200.00\t4\t50.00\t200.00\t0.00\t300.00',
  'MC2025003\t王强\t年卡\t洛阳涧西店\t800.00\t400.00\t6\t100.00\t600.00\t100.00\t500.00',
  'MC2025004\t赵敏\t月卡\t郑州金水店\t150.00\t150.00\t6\t25.00\t150.00\t0.00\t150.00',
  '合计\t—\t—\t—\t2450.00\t1350.00\t—\t—\t1450.00\t100.00\t2250.00',
].join('\n');

const TOL = 0.01;
const TOTAL_WORDS = /^(合计|总计|小计|共计)$/;

/* ⚠️ ROLES 的键顺序就是匹配优先级：更具体的别名必须排在更宽泛的前面
   （否则「期末负债」会被「负债」抢走 —— 这类错不会报缺列，只会静默算错）。 */
const ROLES = {
  memberCard: ['会员卡号', '会员卡编号', '卡号'],
  memberName: ['会员姓名', '会员名称', '持卡人', '姓名'],
  cardType: ['卡类型', '会员卡类型', '卡种'],
  store: ['门店名称', '所属门店', '门店'],
  openLiability: ['期初负债', '期初余额', '期初预收'],
  soldAmount: ['本期销售金额', '本期售卡金额', '本期销售', '销售金额'],
  redeemedTimes: ['本期核销次数', '核销次数', '核销笔数'],
  unitPrice: ['单次确认价', '单次核销价', '单次确认金额', '核销单价'],
  redeemedAmount: ['本期核销金额', '本期核销额', '核销金额'],
  expiredAmount: ['过期作废金额', '本期作废金额', '作废金额', '过期金额'],
  closeLiability: ['期末负债', '期末余额', '期末预收'],
};

const LABELS = {
  memberCard: '会员卡号', memberName: '会员姓名', cardType: '卡种', store: '门店',
  openLiability: '期初负债', soldAmount: '本期销售金额', redeemedTimes: '核销次数',
  unitPrice: '单次确认价', redeemedAmount: '本期核销金额', expiredAmount: '过期作废金额',
  closeLiability: '期末负债',
};

const REQUIRED = ['memberCard', 'openLiability', 'soldAmount', 'redeemedTimes',
  'unitPrice', 'redeemedAmount', 'expiredAmount', 'closeLiability'];
const SUM_ROLES = ['openLiability', 'soldAmount', 'redeemedAmount', 'expiredAmount', 'closeLiability'];
const NON_NEGATIVE = ['soldAmount', 'redeemedTimes', 'unitPrice', 'redeemedAmount'];

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请把会员卡销售与核销明细表（**含表头**）补全再跑：本工具在材料不足时不做任何认定，也不套用默认值。',
  };
}

function splitRow(line) {
  if (String(line).indexOf('\t') >= 0) return String(line).split('\t').map((s) => s.trim());
  return String(line).split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()【】\[\]]/g, '');
  if (!h) return null;
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '').replace(/%$/, '');
  if (!/^-?\d+(\.\d+)?$/.test(t)) return null;
  const n = Number(t);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round((Number(n) + Number.EPSILON) * 100) / 100;

function parseTable(text) {
  const raw = String(text === undefined || text === null ? '' : text)
    .split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { items: [], totals: {}, missingColumns: null, header: [] };
  const header = splitRow(raw[0]);
  const roles = header.map((h) => roleOf(h));
  const missingColumns = REQUIRED.filter((r) => roles.indexOf(r) < 0).map((r) => LABELS[r]);
  const items = [];
  const totals = {};
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1 };
    let isTotal = false;
    for (let c = 0; c < roles.length; c++) {
      const role = roles[c];
      if (!role) continue;
      const v = cells[c] === undefined ? '' : cells[c];
      row[role] = v;
      if (TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    }
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns, header };
}

const who = (it) => {
  const card = it && it.memberCard ? String(it.memberCard).trim() : '';
  const name = it && it.memberName ? String(it.memberName).trim() : '';
  const tag = [card, name].filter((x) => x && !isBlank(x)).join(' ');
  return tag ? `${tag}（第 ${it.line} 行）` : `第 ${it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */

function checkRedeemRecompute(it) {
  const times = normNumber(it.redeemedTimes);
  const price = normNumber(it.unitPrice);
  const amt = normNumber(it.redeemedAmount);
  if (times === null || price === null || amt === null) return null;
  const expect = round2(times * price);
  if (Math.abs(expect - amt) <= TOL) return null;
  return {
    level: 'P0',
    category: '核销金额与核销次数×单次确认价不符',
    line: it.line,
    message: `${who(it)}：核销 ${times} 次 × 单次确认价 ${price.toFixed(2)} 应为 ${expect.toFixed(2)}，`
      + `表里核销金额写的是 ${amt.toFixed(2)}，相差 ${round2(amt - expect).toFixed(2)} —— `
      + '要么次数抄错，要么单次确认价被改过，要么核销金额本身不是按次数算的。',
  };
}

function checkLiabilityIdentity(it) {
  const open = normNumber(it.openLiability);
  const sold = normNumber(it.soldAmount);
  const rede = normNumber(it.redeemedAmount);
  const exp = normNumber(it.expiredAmount);
  const close = normNumber(it.closeLiability);
  if ([open, sold, rede, exp, close].some((v) => v === null)) return null;
  const expect = round2(open + sold - rede - exp);
  if (Math.abs(expect - close) <= TOL) return null;
  return {
    level: 'P0',
    category: '期末负债勾稽不符',
    line: it.line,
    message: `${who(it)}：期初负债 ${open.toFixed(2)} + 本期销售 ${sold.toFixed(2)} − 本期核销 ${rede.toFixed(2)}`
      + ` − 过期作废 ${exp.toFixed(2)} 应为 ${expect.toFixed(2)}，表里期末负债写的是 ${close.toFixed(2)}，`
      + `相差 ${round2(close - expect).toFixed(2)}。`,
  };
}

function checkRedeemOverBalance(it) {
  const open = normNumber(it.openLiability);
  const sold = normNumber(it.soldAmount);
  const rede = normNumber(it.redeemedAmount);
  if (open === null || sold === null || rede === null) return null;
  const available = round2(open + sold);
  if (rede <= available + TOL) return null;
  return {
    level: 'P0',
    category: '核销金额超过卡内可用余额',
    line: it.line,
    message: `${who(it)}：本期核销 ${rede.toFixed(2)} 超过卡内可用余额（期初 ${open.toFixed(2)} + 本期销售 ${sold.toFixed(2)}`
      + ` = ${available.toFixed(2)}），超出 ${round2(rede - available).toFixed(2)} —— 卡里没有的钱不可能被核销掉，`
      + '要么期初负债少记了，要么核销串到了别的卡。',
  };
}

function checkExpiredPolicy(it) {
  const exp = normNumber(it.expiredAmount);
  if (exp === null) return null;
  if (exp < -TOL) {
    return {
      level: 'P0',
      category: '过期作废金额为负',
      line: it.line,
      message: `${who(it)}的过期作废金额是 ${exp.toFixed(2)}（负数）—— 作废只会让负债减少，`
        + '负数通常意味着把冲回/退款记成了作废，请单独列示并写明依据的卡政策条款。',
    };
  }
  const open = normNumber(it.openLiability);
  const sold = normNumber(it.soldAmount);
  const rede = normNumber(it.redeemedAmount);
  if ([open, sold, rede].some((v) => v === null)) return null;
  const available = round2(open + sold - rede);
  // ⚠️ 作废金额为 0 不算「超过可用余额」：核销已经超余额时可用余额是负数，
  //    不能让「作废 0」跟着误报一条（那一条该由「核销金额超过卡内可用余额」单独负责 —— 单因隔离）。
  if (exp <= TOL) return null;
  if (exp <= available + TOL) return null;
  return {
    level: 'P0',
    category: '过期作废金额超过可用余额',
    line: it.line,
    message: `${who(it)}：过期作废 ${exp.toFixed(2)} 超过作废前可用余额（期初 ${open.toFixed(2)} + 本期销售 ${sold.toFixed(2)}`
      + ` − 本期核销 ${rede.toFixed(2)} = ${available.toFixed(2)}），超出 ${round2(exp - available).toFixed(2)} —— `
      + '作废金额必须与会员章程里的有效期与作废条款对得上，请附上条款出处。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) sum += v;
  }
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0',
    category: '合计行与明细之和不符',
    line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} —— 合计行不是明细加出来的，整表勾稽都会被带偏。`,
  });
  return out;
}

function checkDuplicateSale(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const key = String(it.memberCard === undefined || it.memberCard === null ? '' : it.memberCard).trim();
    if (!key) continue;
    const sold = normNumber(it.soldAmount);
    const selling = sold !== null && sold > TOL;
    if (seen.has(key)) {
      const prev = seen.get(key);
      if (selling || prev.selling) {
        out.push({
          level: 'P0',
          category: '同一会员卡号重复销售',
          line: it.line,
          message: `${key} 已在第 ${prev.line} 行出现过（本次第 ${it.line} 行又有一笔），两行都带销售金额时，`
            + '这张卡的预收负债会被重复确认 —— 请先合并成一张卡再算负债。',
        });
      }
    } else {
      seen.set(key, { line: it.line, selling: selling });
    }
  }
  return out;
}

function checkBlanksAndSigns(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
        out.push({
          level: 'P0',
          category: '关键字段缺失或为占位符',
          line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— 这一列不补上，`
            + '相关的复算与勾稽只能跳过，结论就不完整。',
        });
      }
    }
    for (const role of NON_NEGATIVE) {
      const v = normNumber(it[role]);
      if (v !== null && v < -TOL) {
        out.push({
          level: 'P0',
          category: '金额或次数为负',
          line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 退货/冲回请单独列示，`
            + '不要用负数混在发生额里，否则负债与核销率都会被算错。',
        });
      }
    }
  }
  return out;
}

function run(payload) {
  const p = payload;
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到会员卡销售与核销明细表的正文（text）—— 请把**含表头**的那张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `明细表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${(t.header || []).join(' / ') || '(认不出任何表头)'}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头或合计行，没有任何一张会员卡的明细行');
  }

  let ctx = null;


  const findings = [];
  for (const it of t.items) {
    const a = checkRedeemRecompute(it); if (a) findings.push(a);
    const b = checkLiabilityIdentity(it); if (b) findings.push(b);
    const c = checkRedeemOverBalance(it); if (c) findings.push(c);
    const d = checkExpiredPolicy(it); if (d) findings.push(d);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicateSale(t.items)) findings.push(f);
  for (const f of checkBlanksAndSigns(t.items)) findings.push(f);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));

  const notRun = CHECKS_WITHHELD.slice();
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let openTotal = 0;
  let soldTotal = 0;
  let redeemedTotal = 0;
  let closeTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.openLiability); if (a !== null) openTotal += a;
    const b = normNumber(it.soldAmount); if (b !== null) soldTotal += b;
    const c = normNumber(it.redeemedAmount); if (c !== null) redeemedTotal += c;
    const d = normNumber(it.closeLiability); if (d !== null) closeTotal += d;
  }

  const scope = {
    checks: CHECKS_GIVEN,
    checks_not_run: notRun,
    cards: t.items.length,
    open_liability_total: round2(openTotal),
    sold_total: round2(soldTotal),
    redeemed_total: round2(redeemedTotal),
    close_liability_total: round2(closeTotal),
    tolerance: TOL,
    executed_locally: true,
    network_used: false,
  };

  let note = `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`;


  const summary = {
    cards: t.items.length,
    total: findings.length,
    p0: p0,
    p1: p1,
    p2: p2,
    verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
    omitted: 0,
  };

  const result = {
    status: 'success',
    service_type: 'MEMBERSHIP_LIABILITY_CHECK',
    scope: scope,
    findings: findings,
    summary: summary,
    checks_out_of_scope: OUT_OF_SCOPE,
    note: note,
    disclaimer: '只核会员卡销售与核销台账的内部勾稽（核销复算、负债滚存、重复与作废口径），'
      + '**不判断卡政策本身是否合规，也不判断收入确认时点**；结论可由第三方用同一份输入复算。',
  };



  return { status: 'success', result: result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
