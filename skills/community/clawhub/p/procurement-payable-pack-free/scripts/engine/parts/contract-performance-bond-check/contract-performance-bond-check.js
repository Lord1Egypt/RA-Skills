/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * contract-performance-bond-check.js —— 履约保证金与保函台账核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**建筑/工程企业每个项目在缴纳、退还、到期、保函释放这几个节点上**，
 * 财务都要把「履约保证金 / 质量保证金 / 银行保函」这张台账逐笔勾一遍 ——
 * 应退多少、退了没有、保函还剩多少额度、保函到期日跟项目结束日对不对得上。
 * 漏退一笔就是一笔钱长期占在别人账上（占资金），完全能算出来对错。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   应退金额 = 已缴金额 − 已退金额
 *   保函余额 = 保函金额 − 已释放金额
 *   合计行各列 = 各明细行之和
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不规定**保证金比例上限与保函费用标准（业主、地方与银行口径不同）：
 *    只对"明显超出常见区间"做**提示**并明确标注是参考。
 */

const CHECKS_GIVEN = [
  '应退金额复算（已缴金额 − 已退金额 = 应退金额）',
  '保函余额复算（保函金额 − 已释放金额 = 保函余额）',
  '合计行逐列复核',
  '同一项目同一类型重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '已退金额超过已缴金额检测',
  '保函到期日早于项目结束日提示',
  '保函余额为负检测',
  '保证金超过合同金额比例上限（10%）提示（参考口径）',
  '已缴金额为零却有保函费用检测',
];

const OUT_OF_SCOPE = [
  '判断保证金比例上限、保函费用率与保函条款是否合规（各业主、各地与各银行口径不同，请以招标文件、合同与银行条款为准）',
  '判断保函真伪、银行授信与保函索赔（需要向出具银行核验）',
  '处理保证金退还的诉讼时效、违约扣罚与利息主张',
  '读取财务系统或银行流水导出文件（需要你先导出成文本贴进来）',
];

/* 参考比例：履约 + 质量保证金一般不超过合同金额的 10%（仅供"明显超出"时提示，不是规定） */
const DEPOSIT_RATIO_CAP = 0.10;

const SAMPLE_TEXT = [
  '项目名称\t保证金类型\t合同金额\t已缴金额\t已退金额\t应退金额\t保函金额\t已释放金额\t保函余额\t保函费用\t保函到期日\t项目结束日',
  '中环广场项目\t履约保证金\t12000000.00\t1200000.00\t300000.00\t900000.00\t600000.00\t200000.00\t400000.00\t6000.00\t2026-12-31\t2026-09-30',
  '临港物流园项目\t质量保证金\t8000000.00\t400000.00\t0.00\t400000.00\t0.00\t0.00\t0.00\t0.00\t2027-03-31\t2026-12-31',
  '城西医院项目\t履约保证金\t5000000.00\t250000.00\t250000.00\t0.00\t1500000.00\t0.00\t1500000.00\t15000.00\t2027-06-30\t2027-03-31',
  '合计\t\t25000000.00\t1850000.00\t550000.00\t1300000.00\t2100000.00\t200000.00\t1900000.00\t21000.00\t\t',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的前面。
  //    `项目结束日` 若排在 `项目名称` 之后，就会被更宽泛的「项目」抢走 ⇒ 日期列静默为空、永不提示。
  projectEndDate: ['项目结束日', '合同结束日', '工程结束日', '项目竣工日'],
  guaranteeDueDate: ['保函到期日', '保函有效期至', '保函截止日'],
  project: ['项目名称', '工程名称', '项目编号', '项目'],
  bondType: ['保证金类型', '保函类型', '款项类型', '类型'],
  contractAmount: ['合同金额', '合同总额', '合同额', '合同总价'],
  paidAmount: ['已缴金额', '已缴纳金额', '已交金额', '缴纳金额'],
  refundedAmount: ['已退金额', '已退还金额', '退还金额', '已退'],
  refundableAmount: ['应退金额', '应退还金额', '应退未退', '应退'],
  guaranteeAmount: ['保函金额', '保函开具金额', '保函额度'],
  releasedAmount: ['已释放金额', '保函已释放', '已释放'],
  guaranteeBalance: ['保函余额', '保函剩余额度', '保函剩余'],
  guaranteeFee: ['保函费用', '保函手续费', '保函费', '保费'],
};

const LABELS = {
  project: '项目名称', bondType: '保证金类型', contractAmount: '合同金额',
  paidAmount: '已缴金额', refundedAmount: '已退金额', refundableAmount: '应退金额',
  guaranteeAmount: '保函金额', releasedAmount: '已释放金额', guaranteeBalance: '保函余额',
  guaranteeFee: '保函费用', guaranteeDueDate: '保函到期日', projectEndDate: '项目结束日',
};

const REQUIRED = ['project', 'bondType', 'contractAmount', 'paidAmount', 'refundedAmount', 'refundableAmount'];
const SUM_ROLES = ['contractAmount', 'paidAmount', 'refundedAmount', 'refundableAmount',
  'guaranteeAmount', 'releasedAmount', 'guaranteeBalance', 'guaranteeFee'];
/* 金额为负检测只管**存量/发生额**列：`应退金额`「保函余额」是倒挤出来的派生列，
   已退超过已缴时应退本来就是负的 —— 那属于完整档的判定，免费档不许抢答。 */
const NEG_ROLES = ['paidAmount', 'refundedAmount', 'guaranteeAmount', 'releasedAmount', 'guaranteeFee'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|全年合计)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|待核|不详)$/i.test(s);
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

/** 日期归一化成 `YYYY-MM-DD`：`2026/9/30`、`2026年9月30日`、`2026.9.30` 都能认；认不出返回 null */
function normDate(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim()
    .replace(/[年月]/g, '-').replace(/日/g, '')
    .replace(/[/.]/g, '-');
  const m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
  if (!m) return null;
  const y = Number(m[1]); const mo = Number(m[2]); const d = Number(m[3]);
  if (!y || mo < 1 || mo > 12 || d < 1 || d > 31) return null;
  const pad = (n) => (n < 10 ? '0' + n : String(n));
  return `${y}-${pad(mo)}-${pad(d)}`;
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
      if (role === 'project' && TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => (it && it.project && String(it.project).trim()
  ? `${String(it.project).trim()}（第 ${it.line} 行）`
  : `第 ${it && it.line} 行`);

/* ================================ 免费档检查项 ================================ */

function checkRefundable(it) {
  const out = [];
  const depositPaid = normNumber(it.paidAmount);
  const refunded = normNumber(it.refundedAmount);
  const stated = normNumber(it.refundableAmount);
  if (depositPaid === null || refunded === null || stated === null) return out;
  const expect = round2(depositPaid - refunded);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应退金额复算不符', line: it.line,
    message: `${who(it)}：已缴金额 ${depositPaid.toFixed(2)} − 已退金额 ${refunded.toFixed(2)} 应为 ${expect.toFixed(2)}，`
      + `表里应退金额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  });
  return out;
}

function checkGuaranteeBalance(it) {
  const out = [];
  const amount = normNumber(it.guaranteeAmount);
  const released = normNumber(it.releasedAmount);
  const stated = normNumber(it.guaranteeBalance);
  if (amount === null || released === null || stated === null) return out;
  const expect = round2(amount - released);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '保函余额复算不符', line: it.line,
    message: `${who(it)}：保函金额 ${amount.toFixed(2)} − 已释放金额 ${released.toFixed(2)} 应为 ${expect.toFixed(2)}，`
      + `表里保函余额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  });
  return out;
}

function checkTotalRow(totals, items, role) {
  const out = [];
  if (!totals || !totals.row) return out;
  const stated = normNumber(totals.row[role]);
  if (stated === null) return out;
  let sum = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { sum += v; n += 1; }
  }
  if (!n) return out;
  sum = round2(sum);
  if (Math.abs(stated - sum) <= TOL) return out;
  out.push({
    level: 'P0', category: '合计行与明细之和不符', line: totals.line,
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)}。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const name = String(it.project === undefined ? '' : it.project).trim();
    const type = String(it.bondType === undefined ? '' : it.bondType).trim();
    if (!name || !type) continue;
    const key = `${name}|${type}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一项目同一类型重复行', line: it.line,
        message: `${who(it)}（${name} / ${type}）在第 ${seen.get(key)} 行已经出现，第 ${it.line} 行又出现一次`
          + ' —— 保证金或保函会被重复统计（也就可能重复申请退款）。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
        });
      }
    }
  }
  return out;
}

function checkNegativeAmounts(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 冲回请单独列示，不要用负数列在缴纳台账里。`,
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
    return insufficient('没有收到台账正文（text）—— 请把「项目名称 / 保证金类型 / 合同金额 / 已缴 / 已退 / 应退 / '
      + '保函金额 / 已释放 / 保函余额 / 保函费用 / 保函到期日 / 项目结束日」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头（或只有合计行），没有任何保证金/保函明细行');
  }

  const findings = [];
  for (const it of t.items) {
    for (const f of checkRefundable(it)) findings.push(f);
    for (const f of checkGuaranteeBalance(it)) findings.push(f);
    for (const f of checkNegativeAmounts(it)) findings.push(f);

  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  let depositTotal = 0; let refundableTotal = 0; let guaranteeTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.paidAmount); if (a !== null) depositTotal += a;
    const b = normNumber(it.refundableAmount); if (b !== null) refundableTotal += b;
    const c = normNumber(it.guaranteeBalance); if (c !== null) guaranteeTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'CONTRACT_PERFORMANCE_BOND_CHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: notRun,
      rows: t.items.length,
      periods: t.items.length,
      deposit_paid_total: round2(depositTotal),
      refundable_total: round2(refundableTotal),
      guarantee_balance_total: round2(guaranteeTotal),
      deposit_ratio_cap: DEPOSIT_RATIO_CAP,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: t.items.length,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核台账内部的算术勾稽（应退金额 = 已缴金额 − 已退金额、保函余额 = 保函金额 − 已释放金额、'
      + '合计行 = 各明细行之和）与明显的口径异常；**不规定保证金比例上限与保函费用标准**'
      + '（以招标文件、合同与银行条款为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

/* ⚠️ 不导出 `normDate`：它只被完整档的「保函到期日」检查用到，
   剥离付费实现后会被删掉 —— 仍写在 exports 里会当场 `ReferenceError`
   （strip_free_engine 的 always 白名单里恰好有 normDate，不会替你摘掉这个键）。 */
module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
