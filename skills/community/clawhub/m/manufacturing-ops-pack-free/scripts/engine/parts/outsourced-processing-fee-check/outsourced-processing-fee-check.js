/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * outsourced-processing-fee-check.js —— 委外加工费与损耗核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**制造业每月与委外加工厂对账的时候**。料件发出去（委外发出）、
 * 成品收回来（委外收回）、车间/对方仓库还结存多少、损耗掉多少、加工费按"单价 × 数量"该付多少 ——
 * 这几件事必须三方勾稽清楚：
 *
 *   委外发出数量 = 收回数量 + 结存数量 + 损耗量     （料件到底去哪了）
 *   损耗率       = 损耗量 ÷ 发出数量                （损耗有没有超过约定上限）
 *   加工费       = 加工数量 × 加工费单价             （一分钱都不该多算）
 *
 * 算错的后果是实打实的钱：加工费多付（数量或单价填错、同一张加工单重复计费），
 * 或者料件丢失无人认账（损耗量与结存对不上、收回数比发出数还多）。
 * 这张表的每一格都能手算复现，所以"对不对"是完全可以机械核出来的。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 核心可算关系（都能手算复现）：
 *   加工费 = 加工数量 × 加工费单价
 *   损耗量 = 发出数量 − 收回数量 − 结存数量
 *   合计行 = 各明细行逐列相加
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**委外加工费该按哪个单价结算、超损耗部分该不该扣款（那属于合同条款与
 *    商务判断）：单价、数量与损耗上限一律以表里给的、双方签认的为准；
 *    "3%" 只是**参考上限**，用于提示"这笔损耗明显偏高，值得先问一句"。
 */

const CHECKS_GIVEN = [
  '加工费复算（加工数量 × 加工费单价 = 加工费）',
  '损耗量复算（发出数量 − 收回数量 − 结存数量 = 损耗量）',
  '合计行逐列复核',
  '同一加工单重复行检测（加工单号 + 物料名称相同）',
  '空白与占位符检测',
  '数量或金额为负检测',
];

const CHECKS_WITHHELD = [
  '损耗率超过约定上限（参考 3%）提示',
  '加工费与合同单价不一致提示',
  '收回数量大于发出数量检测',
  '结存数量与期末盘点不一致提示',
  '加工数量为零却有加工费提示',
];

const OUT_OF_SCOPE = [
  '判断委外加工费该按哪个单价、哪段期间结算（以合同条款与双方签认的结算单为准）',
  '判断超出约定损耗上限的部分该不该扣款、扣多少（属于合同与商务判断）',
  '核对料件实物出入库单据与仓库台账、盘点表（需要仓库单据与盘点结果）',
  '读取 ERP / 委外加工系统导出文件（需要你先导出成文本贴进来）',
];

/** 参考上限：仅供"明显偏高"时提示，不是行业标准，也不替代合同约定的损耗上限 */
const LOSS_RATE_REF = 0.03;

const SAMPLE_TEXT = [
  '期间\t加工单号\t物料名称\t发出数量\t收回数量\t结存数量\t损耗量\t损耗率\t加工数量\t加工费单价\t加工费\t合同单价\t期末盘点数量',
  '2026-01\tWW2026-001\t铝壳\t10000\t9600\t280\t120\t1.2%\t9600\t1.50\t14400.00\t1.50\t280',
  '2026-01\tWW2026-002\t铜片\t8000\t7840\t80\t80\t1.0%\t7840\t0.80\t6272.00\t0.80\t80',
  '2026-02\tWW2026-003\t塑胶件\t5000\t4900\t50\t50\t1.0%\t4900\t0.60\t2940.00\t0.60\t50',
  '合计\t\t\t23000.00\t22340.00\t410.00\t250.00\t\t22340.00\t\t23612.00\t\t410.00',
].join('\n');

const TOL = 0.01;
const RATE_TOL = 0.0005;                    // 比率容差：0.05 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名必须排在更宽泛的词前面，否则宽泛词会把整列抢走。
  //    · 「损耗率」必须在「损耗量/损耗」之前，否则损耗率那列被当成损耗量（算错但不报错）；
  //    · 「合同单价」必须在「加工费单价/单价」之前，否则合同单价被当成计费单价；
  //    · 「加工费单价」必须在「加工费」之前，否则计费单价被当成加工费金额。
  period: ['期间', '结算期间', '对账期间', '所属期', '加工月份', '月份'],
  orderNo: ['委外加工单号', '加工单号', '委外单号', '加工单编号', '委外加工单', '工单号'],
  item: ['物料名称', '料件名称', '物料规格', '物料', '料件', '品名'],
  issuedQty: ['委外发出数量', '发出数量', '发出料件数量', '发出'],
  returnedQty: ['委外收回数量', '收回数量', '收回成品数量', '收回'],
  balanceQty: ['结存数量', '未收回数量', '结存'],
  lossRate: ['损耗率', '料件损耗率'],
  lossQty: ['损耗量', '损耗数量', '损耗'],
  processQty: ['加工数量', '加工完成数量', '加工量'],
  contractPrice: ['合同单价', '合同加工单价', '约定单价'],
  unitPrice: ['加工费单价', '加工单价', '计费单价', '单价'],
  processFee: ['加工费', '加工费金额', '加工费合计', '加工费小计'],
  stockQty: ['期末盘点数量', '期末盘点', '盘点数量'],
};

const LABELS = {
  period: '期间', orderNo: '加工单号', item: '物料名称', issuedQty: '发出数量',
  returnedQty: '收回数量', balanceQty: '结存数量', lossQty: '损耗量', lossRate: '损耗率',
  processQty: '加工数量', unitPrice: '加工费单价', processFee: '加工费',
  contractPrice: '合同单价', stockQty: '期末盘点数量',
};

const REQUIRED = ['period', 'orderNo', 'issuedQty', 'returnedQty', 'balanceQty',
  'lossQty', 'processQty', 'unitPrice', 'processFee'];
/** 合计行逐列复核的列（单价/比率不是可加列，逐列复核不覆盖它们） */
const SUM_ROLES = ['issuedQty', 'returnedQty', 'balanceQty', 'lossQty',
  'processQty', 'processFee', 'stockQty'];
/** 负值检测覆盖的列（lossRate 另按比率解析） */
const NEGATIVE_ROLES = ['issuedQty', 'returnedQty', 'balanceQty', 'lossQty', 'processQty',
  'unitPrice', 'processFee', 'contractPrice', 'stockQty', 'lossRate'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合 计)$/;

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

/** 比率归一化成小数：`1.2%` ⇒ 0.012；`0.012` ⇒ 0.012；`1.2` ⇒ 0.012 */
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
    ? String(it.period).trim() : '';
  const o = it && it.orderNo !== undefined && String(it.orderNo).trim() !== ''
    ? String(it.orderNo).trim() : '';
  const n = it && it.item !== undefined && String(it.item).trim() !== ''
    ? String(it.item).trim() : '';
  const head = [p, o].filter(Boolean).join(' ') || `第 ${it && it.line} 行`;
  return n ? `${head}「${n}」` : head;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkProcessFeeRecompute(it) {
  const out = [];
  const qty = normNumber(it.processQty);
  const price = normNumber(it.unitPrice);
  const stated = normNumber(it.processFee);
  if (qty === null || price === null || stated === null) return out;
  if (Math.abs(qty) <= TOL) return out;      // 加工数量为零：复算无从算起（完整档单独提示）
  const expect = round2(qty * price);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '加工费复算不符', line: it.line,
    message: `${who(it)}：加工数量 ${qty.toFixed(2)} × 加工费单价 ${price.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「加工费」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)} —— `
      + '加工费就是这两个数相乘，不该有第三种算法；多算就是多付，少算对方会要求补。',
  });
  return out;
}

function checkLossQtyRecompute(it) {
  const out = [];
  const issued = normNumber(it.issuedQty);
  const returned = normNumber(it.returnedQty);
  const balance = normNumber(it.balanceQty);
  const stated = normNumber(it.lossQty);
  if (issued === null || returned === null || balance === null || stated === null) return out;
  const expect = round2(issued - returned - balance);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '损耗量复算不符', line: it.line,
    message: `${who(it)}：发出数量 ${issued.toFixed(2)} − 收回数量 ${returned.toFixed(2)} − 结存数量 ${balance.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「损耗量」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)} —— `
      + '发出去的料件只有"收回 + 结存 + 损耗"三个去处，损耗量对不上就是这三笔里至少有一笔填错。',
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
    sum = round2(sum);
    if (Math.abs(stated - sum) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 条明细行逐行相加是 ${sum.toFixed(2)}，`
        + `相差 ${round2(stated - sum).toFixed(2)} —— 合计行必须等于各明细行之和。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const o = it.orderNo !== undefined ? String(it.orderNo).trim() : '';
    const n = it.item !== undefined ? String(it.item).trim() : '';
    if (!o) continue;
    const key = `${o}|${n}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一加工单重复行', line: it.line,
        message: `${who(it)}与第 ${seen.get(key)} 行是同一张加工单的同一物料，却列了两行 —— `
          + '发出/收回数量与加工费会被重复汇总，等于按同一笔加工付两次钱。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）—— `
            + '这一格会静默地不参与任何检查，先把原始单据上的数补上再核。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = role === 'lossRate' ? rateValue(it[role]) : normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    const shown = role === 'lossRate' ? `${(v * 100).toFixed(3)}%` : v.toFixed(2);
    out.push({
      level: 'P0', category: '数量或金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${shown}（负数）—— 发出/收回/结存/损耗与加工费都不该为负；`
        + '退料、冲回或红字调整请单独列示，不要用负数混在正常行里。',
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
    return insufficient('没有收到委外加工结算核对表正文（text）—— 请把「期间 / 加工单号 / 物料名称 / 发出数量 / 收回数量 / 结存数量 / 损耗量 / 加工数量 / 加工费单价 / 加工费」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `委外加工结算核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何委外加工明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkProcessFeeRecompute(it));
    findings.push(...checkLossQtyRecompute(it));
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

  let issuedTotal = 0;
  let returnedTotal = 0;
  let lossTotal = 0;
  let feeTotal = 0;
  for (const it of t.items) {
    const a = normNumber(it.issuedQty); if (a !== null) issuedTotal += a;
    const b = normNumber(it.returnedQty); if (b !== null) returnedTotal += b;
    const c = normNumber(it.lossQty); if (c !== null) lossTotal += c;
    const d = normNumber(it.processFee); if (d !== null) feeTotal += d;
  }

  const result = {
    status: 'success',
    service_type: 'OUTSOURCED_PROCESSING_FEE_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      issued_qty_total: round2(issuedTotal),
      returned_qty_total: round2(returnedTotal),
      loss_qty_total: round2(lossTotal),
      process_fee_total: round2(feeTotal),
      loss_rate_ref: LOSS_RATE_REF,
      tolerance: TOL,
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
    disclaimer: '只核「加工数量 × 加工费单价 = 加工费」「发出数量 − 收回数量 − 结存数量 = 损耗量」'
      + '与合计行这类**表内勾稽**，以及"明显偏高"的档位提示；'
      + '**不判断**该按哪个单价结算、超损耗部分该不该扣款（以合同条款与双方签认的结算单为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
