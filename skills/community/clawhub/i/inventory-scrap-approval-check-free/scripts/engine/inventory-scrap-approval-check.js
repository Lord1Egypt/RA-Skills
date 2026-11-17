/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * inventory-scrap-approval-check.js —— 存货报废与审批核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**制造 / 零售企业每月月末**都要处理存货报废 ——
 * 车间或仓库报损 → 填报废单 → 审批人签字 → 财务做账务处理（待处理财产损溢 / 管理费用等）
 * → 申报时按税法规定作为**资产损失税前扣除**。这里有两层硬约束：
 *   ① **算术必须对**：报废金额 = 报废数量 × 单位成本；报废后库存 = 期初 + 入库 − 领用 − 报废；
 *      同一物料同一批次不能被重复报废（重复即重复计入损失）。
 *   ② **审批必须齐**：**没有审批人（或审批金额为零）的报废不能作为税前扣除依据** ——
 *      这是"缺审批的报废不能税前扣除"这条规则在台账上的机械体现。
 * 这两件事都**完全能算出来对错**，所以交给本引擎逐行复算。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   报废金额       = 报废数量 × 单位成本
 *   报废后库存     = 期初数量 + 本期入库数量 − 本期领用数量 − 报废数量
 *   同一批次报废率 = 报废数量 ÷（期初数量 + 本期入库数量）
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不确定**任何税务或会计口径：单位成本区间与报废率上限只做"明显偏离"的**提示**，
 *    不构成税前扣除的认定，也不替代主管税务机关与本单位审批制度的要求。
 */

const CHECKS_GIVEN = [
  '报废金额复算（报废数量 × 单位成本 = 报废金额）',
  '报废后库存复算（期初数量 + 本期入库数量 − 本期领用数量 − 报废数量 = 报废后库存）',
  '合计行逐列复核',
  '同一物料同一批次重复报废检测',
  '空白与占位符检测',
  '数量或金额为负检测（报废数量 / 单位成本 / 报废金额 / 期初、入库、领用数量）',
];

const CHECKS_WITHHELD = [
  '报废金额超过审批金额提示',
  '无审批人或审批金额为零的报废提示（缺审批不能税前扣除）',
  '报废后库存为负检测',
  '单位成本偏离参考区间（0.01~100000 元/单位）提示（参考口径）',
  '同一批次报废率超过参考上限（5%）提示（参考口径）',
];

const OUT_OF_SCOPE = [
  '判断报废能不能税前扣除、要准备哪些证据资料（以税法与主管税务机关口径为准）',
  '判断某批次存货是否**真的**该报废（能否使用、降价出售、退供应商或返工）',
  '核对报废的账务处理科目与凭证（待处理财产损溢 / 管理费用 / 营业外支出 等）',
  '处理报废物资的变卖收入、进项税额转出与残值回收',
  '读取 ERP / 存货系统导出文件（需要你先导出成文本贴进来）',
];

/* 参考区间：仅供"明显偏离"时提示，**不是规定**，也不构成定价或税务认定 */
const UNIT_COST_REF = [0.01, 100000];   // 单位成本宽区间（元/单位）
const SCRAP_RATE_REF = 0.05;            // 同一批次报废率参考上限 5%

const SAMPLE_TEXT = [
  '期间\t物料编码\t物料名称\t批次号\t期初数量\t本期入库数量\t本期领用数量\t报废数量\t单位成本\t报废金额\t报废后库存\t审批人\t审批金额',
  '2026-01\tCL-001\t瓦楞纸箱\tB2401\t1000\t500\t300\t50\t2.50\t125.00\t1150\t张伟\t125.00',
  '2026-01\tCL-002\t塑料托盘\tB2402\t800\t200\t150\t40\t12.00\t480.00\t810\t李娜\t480.00',
  '2026-01\tCL-003\t缠绕膜\tB2403\t600\t400\t250\t30\t8.00\t240.00\t720\t王强\t300.00',
  '合计\t—\t—\t—\t2400\t1100\t700\t120\t—\t845.00\t2680\t—\t905.00',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  //    （「审批金额」必须排在「审批」前面，否则审批人那一列会把审批金额列抢走；
  //      「报废金额」「报废后库存」也必须排在更宽泛的"报废"类词前面 —— 列被抢走=静默算错）
  period: ['期间', '月份', '所属期', '会计期间', '年度'],
  materialCode: ['物料编码', '物料编号', '存货编码', '存货编号', '物料号', '存货号'],
  materialName: ['物料名称', '存货名称', '物料描述', '品名'],
  batch: ['批次号', '批次', '批号'],
  beginQty: ['期初数量', '期初结存', '期初库存', '期初'],
  inQty: ['本期入库数量', '入库数量', '本期入库', '入库'],
  issueQty: ['本期领用数量', '领用数量', '本期领用', '出库数量', '领用', '出库'],
  scrapQty: ['报废数量', '报废件数'],
  unitCost: ['单位成本', '单位成本价', '单位单价', '单价'],
  scrapAmount: ['报废金额', '报废损失金额', '报废成本金额'],
  approvalAmount: ['审批金额', '批准金额', '核准金额'],
  approver: ['审批人', '批准人', '核准人', '审批签字', '审批'],
  endingQty: ['报废后库存', '报废后结存', '报废后数量', '期末数量', '期末结存', '结存数量', '库存数量'],
};

const LABELS = {
  period: '期间', materialCode: '物料编码', materialName: '物料名称', batch: '批次号',
  beginQty: '期初数量', inQty: '本期入库数量', issueQty: '本期领用数量', scrapQty: '报废数量',
  unitCost: '单位成本', scrapAmount: '报废金额', approvalAmount: '审批金额',
  approver: '审批人', endingQty: '报废后库存',
};

const REQUIRED = ['period', 'materialCode', 'batch', 'scrapQty', 'unitCost', 'scrapAmount'];
const SUM_ROLES = ['beginQty', 'inQty', 'issueQty', 'scrapQty', 'scrapAmount', 'endingQty', 'approvalAmount'];
const NEG_ROLES = ['scrapQty', 'unitCost', 'scrapAmount', 'beginQty', 'inQty', 'issueQty'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|汇总|全年合计)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值，更不会输出"未发现问题"。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|暂无)$/i.test(s);
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
      if (TOTAL_WORDS.test(String(v).trim())) isTotal = true;
    });
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

function who(it) {
  const p = it && it.period ? String(it.period).trim() : '';
  const m = it && it.materialCode ? String(it.materialCode).trim() : '';
  const b = it && it.batch ? String(it.batch).trim() : '';
  const tag = [m, b].filter((x) => x).join('/');
  if (p && tag) return `${p} 的 ${tag}`;
  if (tag) return tag;
  if (p) return `${p} 期`;
  return `第 ${it && it.line} 行`;
}

/* ⚠️ 本文件所有 check* 函数**一律返回数组**，调用处一律 for...of 展开 ——
   两种形态混用时，返回空数组的那条会被当成"一条发现"，是静默算错的来源。 */

/* ================================ 免费档检查项 ================================ */

function checkScrapAmount(it) {
  const out = [];
  const qty = normNumber(it.scrapQty);
  const cost = normNumber(it.unitCost);
  const stated = normNumber(it.scrapAmount);
  if (qty === null || cost === null || stated === null) return out;
  const expect = round2(qty * cost);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '报废金额与复算不符', line: it.line,
    message: `${who(it)}：报废数量 ${qty} × 单位成本 ${cost.toFixed(2)} 应为 ${expect.toFixed(2)}，表里报废金额是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`,
  });
  return out;
}

function checkEndingQty(it) {
  const out = [];
  const begin = normNumber(it.beginQty);
  const add = normNumber(it.inQty);
  const issue = normNumber(it.issueQty);
  const scrap = normNumber(it.scrapQty);
  const stated = normNumber(it.endingQty);
  if (begin === null || add === null || issue === null || scrap === null || stated === null) return out;
  const expect = round2(begin + add - issue - scrap);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '报废后库存与勾稽不符', line: it.line,
    message: `${who(it)}：期初 ${begin} + 入库 ${add} − 领用 ${issue} − 报废 ${scrap} = ${expect}，表里报废后库存是 ${stated}，相差 ${round2(stated - expect)}。`,
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
    message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)} —— 合计行必须逐列等于明细之和。`,
  });
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const code = String(it.materialCode || '').trim();
    const batch = String(it.batch || '').trim();
    if (!code && !batch) continue;
    const key = `${code}\u0000${batch}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一物料同一批次重复报废', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经报废过一次，第 ${it.line} 行又出现同一物料同一批次 —— 同一批次的报废会被重复计入损失，请确认是分次报废还是重复录入。`,
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

function checkNegatives(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null || v >= -TOL) continue;
    out.push({
      level: 'P0', category: '数量或金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v}（负数）—— 冲回或红字请单独列示，不要直接抵减本期报废。`,
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
    return insufficient('没有收到报废台账正文（text）—— 请把「期间 / 物料编码 / 批次号 / 报废数量 / 单位成本 / 报废金额 / 审批人」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `报废台账缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何物料明细行');
  }

  const findings = [];
  for (const it of t.items) {
    for (const f of checkScrapAmount(it)) findings.push(f);
    for (const f of checkEndingQty(it)) findings.push(f);
    for (const f of checkNegatives(it)) findings.push(f);

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

  let scrapTotal = 0;
  const periods = new Set();
  for (const it of t.items) {
    const a = normNumber(it.scrapAmount); if (a !== null) scrapTotal += a;
    const p = String(it.period === undefined ? '' : it.period).trim();
    if (p) periods.add(p);
  }

  const result = {
    status: 'success',
    service_type: 'INVENTORY_SCRAP_APPROVAL_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: periods.size,
      scrap_amount_total: round2(scrapTotal),
      unit_cost_ref: UNIT_COST_REF,
      scrap_rate_ref: SCRAP_RATE_REF,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings,
    summary: {
      rows: t.items.length,
      periods: periods.size,
      total: findings.length,
      p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: `本版本只执行：${CHECKS_GIVEN.join('、')}；未执行的检查项见 scope.checks_not_run。`,
    disclaimer: '只核"报废数量 × 单位成本 = 报废金额""期初 + 入库 − 领用 − 报废 = 报废后库存"这类台账内部勾稽，'
      + '**不判断报废能不能税前扣除、也不规定单位成本与报废率的标准**（审批制度与税务口径请以本单位规定和主管税务机关为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
