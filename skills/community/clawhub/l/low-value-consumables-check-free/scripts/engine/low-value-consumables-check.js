/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * low-value-consumables-check.js —— 低值易耗品与周转材料摊销核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**有低值易耗品 / 包装物 / 劳保用品 / 周转材料（工具、模具、钢模板等）
 * 台账的企业**，在**每月月末计提摊销并结转、以及年度盘点与审计提供底稿之前**。
 * 仓管与会计各维护一份表，摊销方法又分一次转销法、五五摊销法、分次摊销法三种口径，
 * 最容易出错的正是"数量与金额两条滚存线对不对得上"和"有没有摊销超过可摊销基础"。
 *
 * 核心可算关系（都能手算复现）：
 *   期末数量 = 期初数量 + 本期入库数量 − 本期领用数量
 *   期末金额 = 期初金额 + 本期入库金额 − 本期摊销金额
 *   本期摊销金额 ≤ 期初金额 + 本期入库金额（不能摊销超过可摊销基础）
 *   累计已摊销金额 ≤ 期初金额 + 本期入库金额（累计也不能超）
 *   合计行 = 明细逐行相加（两处必须一致）
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该用哪种摊销方法、该摊销多少（那属于会计政策与职业判断）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**带限定语的列必须排在裸词前面**（本仓库反复踩过的坑）。
   `累计已摊销金额` 里含 `摊销金额`，`本期入库金额` 里含 `金额`，`期初数量` 里含 `数量`
   ⇒ 若把 `摊销金额` 这类更宽泛的键排在 `累计已摊销金额` 前面，累计摊销那一列会被**抢走**，
   `amortCum` 永远认不出来 ⇒ 累计超摊检查静默不跑（`header_map_check.py` 会拦下来）。
   所以：`amortCum` 必须排在 `amortAmount` 之前，并且**不使用裸 `金额` / 裸 `摊销` / 裸 `数量` 做键**。 */
const ROLES = {
  category: ['物品类别', '物料类别', '类别'],
  name: ['物品名称', '物料名称', '品名', '名称'],
  unit: ['计量单位', '单位'],
  beginQty: ['期初数量', '期初结存数量'],
  beginAmount: ['期初金额', '期初余额'],
  inQty: ['本期入库数量', '入库数量'],
  inAmount: ['本期入库金额', '入库金额'],
  outQty: ['本期领用数量', '领用数量'],
  amortCum: ['累计已摊销金额', '累计摊销金额', '累计摊销'],
  amortAmount: ['本期摊销金额', '摊销金额'],
  endQty: ['期末数量', '期末结存数量'],
  endAmount: ['期末金额'],
  method: ['摊销方法', '摊销方式'],
};

const LABELS = {
  category: '物品类别', name: '物品名称', unit: '计量单位',
  beginQty: '期初数量', beginAmount: '期初金额',
  inQty: '本期入库数量', inAmount: '本期入库金额',
  outQty: '本期领用数量', amortAmount: '本期摊销金额', amortCum: '累计已摊销金额',
  endQty: '期末数量', endAmount: '期末金额', method: '摊销方法',
};

/* 必需列 = 参与"两条滚存线 + 合计勾稽 + 重复/空缺"的列。
   ⛔ 缺列**不**等于材料不足：只缺个别列时照常执行，并报一条「列缺失」结论
      （上一轮踩过：把缺列当成 insufficient_input，这条检查就**永远不触发**）。
   计量单位 / 摊销方法 属于口径列，不进必需列。 */
const REQUIRED = ['category', 'name', 'beginQty', 'beginAmount', 'inQty', 'inAmount',
  'outQty', 'amortAmount', 'amortCum', 'endQty', 'endAmount'];
/* 合计行要逐列复核的 9 个数值列（口径来自产品规则）。 */
const SUM_ROLES = ['beginQty', 'beginAmount', 'inQty', 'inAmount', 'outQty',
  'amortAmount', 'amortCum', 'endQty', 'endAmount'];
const AMORT_METHODS = ['一次转销法', '五五摊销法', '分次摊销法'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?|合计行)$/;
const TOL = 0.01;

/* ⚠️ 付费开关**只声明一次**（形态 B）：`strip_free_engine` 按「常量名 + Boolean(」这一整行
   识别并摘掉付费语句；写成别的形式（例如数组的 `.some()`）会**留下开关不删**
   ⇒ 泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断，
      写了就会被当成"没删干净"而整包跳过。两个形态（MARKER + 开关）同时出现
      还会把免费检查也整块删掉（第 236 轮踩过）。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（期初数量/期初金额/入库数量/入库金额/领用数量/摊销/累计摊销/期末数量/期末金额）',
  '同一物品名称+类别重复行检测',
  '期末数量 = 期初数量 + 本期入库数量 − 本期领用数量（不符报 P0）',
  '期末金额 = 期初金额 + 本期入库金额 − 本期摊销金额（不符报 P0）',
  '本期摊销金额 ≤ 期初金额 + 本期入库金额（超摊报 P0）',
  '累计已摊销金额 ≤ 期初金额 + 本期入库金额（累计超摊报 P1）',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '期末数量为负（P0）',
  '期末金额为负（P1）',
  '本期摊销金额为负（P1）',
  '摊销方法不在常见口径（P2）提示',
  '本期领用数量 > 期初数量 + 本期入库数量（领用超库存，P1）提示',
];

const OUT_OF_SCOPE = [
  '判断该用一次转销法 / 五五摊销法 / 分次摊销法中的哪一种（属于会计政策判断）',
  '判断本期该摊销多少金额、残值怎么定（属于会计估计，不由本工具出数）',
  '核对发票、入库单、领料单的**真伪**，或与 ERP / 仓管系统的逐行明细比对',
  '读取 ERP / 进销存 / 仓管系统的导出文件（需要你先导出成文本贴进来）',
  '判断低值易耗品的**分类**对不对（某件物品算低值易耗品还是固定资产），也不出具审计意见',
];

const SAMPLE_TEXT = [
  '物品类别\t物品名称\t计量单位\t期初数量\t期初金额\t本期入库数量\t本期入库金额\t本期领用数量\t本期摊销金额\t累计已摊销金额\t期末数量\t期末金额\t摊销方法',
  '劳保用品\t工作服\t套\t100\t5000.00\t200\t10000.00\t150\t7500.00\t7500.00\t150\t7500.00\t五五摊销法',
  '包装物\t纸箱\t个\t50\t2000.00\t0\t0.00\t20\t800.00\t800.00\t30\t1200.00\t一次转销法',
  '合计\t\t\t150\t7000.00\t200\t10000.00\t170\t8300.00\t8300.00\t180\t8700.00\t',
].join('\n');

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|不详)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  let neg = false;
  if (/^\(.*\)$/.test(s)) { neg = true; s = s.slice(1, -1); }
  if (s.endsWith('%')) s = s.slice(0, -1);
  if (!/^-?\d+(\.\d+)?$/.test(s)) return null;
  const n = Number(s);
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const who = (it) => {
  const nm = String(it.name || '').trim();
  const cat = String(it.category || '').trim();
  if (nm && cat) return `${cat}-${nm}`;
  if (nm) return nm;
  return `第 ${it.line} 行`;
};

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) {
    return { items: [], totals: {}, missingColumns: [], header: [], recognized: 0 };
  }
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const recognized = cols.filter((c) => c.role).length;
  const missingColumns = REQUIRED.filter((r) => !cols.some((c) => c.role === r));
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => {
      if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i];
    });
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header, recognized, cols };
}

/* ================================ 免费档检查项 ================================ */

function checkTotalRow(items, totals) {
  if (!totals.row) return [];
  const out = [];
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let sum = 0;
    let n = 0;
    for (const it of items) {
      const v = normNumber(it[role]);
      if (v === null) continue;
      sum += v;
      n += 1;
    }
    sum = round2(sum);
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        line: totals.line, level: 'P1', category: '合计复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细逐行相加是 ${sum}`,
        evidence: `合计行第 ${totals.line} 行「${LABELS[role]}」=${stated}；明细 ${n} 行相加=${sum}；差异=${round2(stated - sum)}`,
      });
    }
  }
  return out;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const nm = String(it.name || '').trim();
    if (!nm) continue;
    const cat = String(it.category || '').trim();
    const key = `${cat}\u0001${nm}`;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「物品类别 + 物品名称」完全相同 —— 可能重复计入`,
        evidence: `物品类别=${cat || '(空)'}；物品名称=${nm}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

function checkEndQtyRoll(it) {
  const b = normNumber(it.beginQty);
  const i = normNumber(it.inQty);
  const o = normNumber(it.outQty);
  const e = normNumber(it.endQty);
  if (b === null || i === null || o === null || e === null) return null;
  const calc = round2(b + i - o);
  if (Math.abs(calc - e) > TOL) {
    return {
      line: it.line, level: 'P0', category: '期末数量滚存不符',
      message: `${who(it)} 期末数量填 ${e}，但 ${b} + ${i} − ${o} = ${calc}`,
      evidence: `期初数量=${b}；本期入库数量=${i}；本期领用数量=${o}；应有期末数量=${calc}；表列期末数量=${e}；差异=${round2(e - calc)}`,
    };
  }
  return null;
}

function checkEndAmountRoll(it) {
  const b = normNumber(it.beginAmount);
  const i = normNumber(it.inAmount);
  const a = normNumber(it.amortAmount);
  const e = normNumber(it.endAmount);
  if (b === null || i === null || a === null || e === null) return null;
  const calc = round2(b + i - a);
  if (Math.abs(calc - e) > TOL) {
    return {
      line: it.line, level: 'P0', category: '期末金额滚存不符',
      message: `${who(it)} 期末金额填 ${e}，但 ${b} + ${i} − ${a} = ${calc}`,
      evidence: `期初金额=${b}；本期入库金额=${i}；本期摊销金额=${a}；应有期末金额=${calc}；表列期末金额=${e}；差异=${round2(e - calc)}`,
    };
  }
  return null;
}

function checkAmortOver(it) {
  const b = normNumber(it.beginAmount);
  const i = normNumber(it.inAmount);
  const a = normNumber(it.amortAmount);
  if (b === null || i === null || a === null) return null;
  const base = round2(b + i);
  if (a - base > TOL) {
    return {
      line: it.line, level: 'P0', category: '本期摊销超摊',
      message: `${who(it)} 本期摊销金额 ${a} 超过可摊销基础 ${base}（期初金额 ${b} + 本期入库金额 ${i}）`,
      evidence: `期初金额=${b}；本期入库金额=${i}；可摊销基础=${base}；本期摊销金额=${a}；超出=${round2(a - base)}`,
    };
  }
  return null;
}

function checkCumAmortOver(it) {
  const b = normNumber(it.beginAmount);
  const i = normNumber(it.inAmount);
  const c = normNumber(it.amortCum);
  if (b === null || i === null || c === null) return null;
  const base = round2(b + i);
  if (c - base > TOL) {
    return {
      line: it.line, level: 'P1', category: '累计摊销超摊',
      message: `${who(it)} 累计已摊销金额 ${c} 超过可摊销基础 ${base}（期初金额 ${b} + 本期入库金额 ${i}）`,
      evidence: `期初金额=${b}；本期入库金额=${i}；可摊销基础=${base}；累计已摊销金额=${c}；超出=${round2(c - base)}`,
    };
  }
  return null;
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')} —— 与这些列有关的核对已跳过，其余照常执行`,
      evidence: `表头=${header.join('|')}；缺列=${missingColumns.map((r) => LABELS[r]).join('、')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符 —— 这一行无法核对`,
          evidence: `${LABELS[role]}=${it[role] === undefined ? '(空)' : it[role]}`,
        });
      }
    }
  }
  return out;
}

/* ============================== 完整档（付费）检查项 ============================== */

/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') {
    return insufficient(['材料文本为空：请把低值易耗品 / 周转材料台账（含表头）整段贴进来，Tab 分隔最稳']);
  }

  const { items, totals, missingColumns, header, recognized } = parseTable(text);
  if (!recognized) {
    return insufficient([
      '认不出表头：第一行必须是表头，且要能认出「物品类别 / 物品名称 / 期初数量 / 期初金额 / '
      + '本期入库数量 / 本期入库金额 / 本期领用数量 / 本期摊销金额 / 累计已摊销金额 / 期末数量 / 期末金额」这类列名',
      `当前第一行：${header.join(' | ') || '(空)'}`,
    ]);
  }
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（只有「合计」行不算明细）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [
      checkEndQtyRoll(it),
      checkEndAmountRoll(it),
      checkAmortOver(it),
      checkCumAmortOver(it),
    ];
    for (const f of one) if (f) findings.push(f);
  }
  for (const f of checkDuplicate(items)) findings.push(f);
  for (const f of checkBlanks(header, items, missingColumns)) findings.push(f);



  findings.sort((a, b) => (a.line - b.line) || String(a.category).localeCompare(String(b.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const checkList = CHECKS_GIVEN;
  const notRun = CHECKS_WITHHELD;

  return {
    status: 'success',
    result: {
      findings,
      summary: {
        rows: items.length,
        total: findings.length,
        p0, p1, p2,
        verdict: findings.length === 0 ? 'NO_ISSUE_FOUND' : (p0 > 0 ? 'P0_ISSUES' : 'ISSUES'),
        omitted: 0,
      },
      scope: {
        checks: checkList,
        checks_not_run: notRun,
        rows: items.length,
        amort_total: round2(items.reduce((n, it) => n + (normNumber(it.amortAmount) || 0), 0)),
        end_amount_total: round2(items.reduce((n, it) => n + (normNumber(it.endAmount) || 0), 0)),
        missing_columns: missingColumns.map((r) => LABELS[r]),
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, AMORT_METHODS,
};
