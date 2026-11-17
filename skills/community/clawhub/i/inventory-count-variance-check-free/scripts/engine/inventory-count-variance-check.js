/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * inventory-count-variance-check.js —— 存货盘点差异与账实调整核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**有实物存货的仓库/工厂/门店**，在**月度（或年终）盘点结束、
 * 出"盘点差异表"报审批、以及做账实调整凭证之前**。仓管给出实盘数量，会计给出账面数量与单价，
 * 差异表上要同时填「差异数量 / 差异金额 / 差异原因」三列；审批人（财务负责人/内审）盯的就是
 * 它们能不能**逐行对上、合计加得上、有差异的都要写清原因**。这三件事一旦有一处对不上，
 * 账实调整凭证的金额就是错的 —— 而且**表本身不会报错**，只会静默地把错的差异金额过进账里。
 *
 * 核心可算关系（都能手算复现）：
 *   差异数量 = 实盘数量 − 账面数量
 *   差异金额 = 实盘金额 − 账面金额
 *   账面金额 = 账面数量 × 账面前单价
 *   实盘金额 = 实盘数量 × 盘点单价
 *   合计行逐列 = 明细行逐行相加（账面/实盘的数量、金额、差异的数量与金额）
 *   有差异的行必须有差异原因；|差异金额| 超过账面金额 30% 属重大差异
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**盘盈盘亏该走什么审批与账务处理、不判断差异的责任归属与跌价准备
 *   （那属于会计政策、管理与会计估计判断），只做上面这些**能算出来的核对**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 *
 * ⚠️ 完整档（付费）的检查项用**形态 B**：先声明一个布尔开关（三个开关字段任一为真即为完整档），
 *    再把完整档的检查包进 `if (开关) { ... }` 分支里（**不要**再留 MARKER 那类整块标记：
 *    两个形态同时出现时 `strip_free_engine` 会走形态 A，把免费档的检查也整块删掉）。
 * ⚠️ 免费包里的付费实现由 `tools/strip_free_engine.py --apply` 机械摘除，所以：
 *    · 完整档的检查必须各自是一个**顶层 function**，且只被付费分支引用（否则摘不干净）；
 *    · 开关三个字段的字面量**不要**写进注释（摘除后还要做残留断言，命中就整包回滚）。
 */

/* ⛔ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**（本仓库踩过 6 次的坑，header_map_check 会拦）。
   本表的坑：
     · `账面金额` 里含 `金额`；`实盘金额`、`差异金额` 同理 —— 宽泛的 `金额` 排前面会把三列全抢走；
     · `账面数量` / `实盘数量` / `差异数量` 里都含 `数量`；`账面前单价` / `盘点单价` 里都含 `单价`；
     · `差异数量` 里含 `数量`、`差异金额` 里含 `金额`、`差异原因` 里含 `差异` —— 三列必须各自独立，
       一旦两列落到同一个角色，后一列会把前一列**覆盖**（解析出的列数变少，算错但不会报缺列）。
   所以：带限定语的列（账面/实盘/差异 × 数量/单价/金额）**一律排在裸词（数量/单价/金额）前面**。 */
const ROLES = {
  warehouse: ['仓库', '库房', '存货地点', '存放地点'],
  itemCode: ['存货编码', '存货代码', '存货编号', '物料编码', '物料编号', '编码'],
  itemName: ['存货名称', '物料名称', '存货品名', '品名', '名称'],
  unit: ['计量单位', '单位'],
  bookQty: ['账面数量', '账存数量', '账面数'],
  countQty: ['实盘数量', '盘点数量', '实存数量', '实盘数'],
  diffQty: ['差异数量', '盘盈盘亏数量', '差额数量'],
  /* ⛔ `账面前单价` 必须排在 `账面单价` 之前（前者是这张表的实际写法），两者都排在裸词 `单价` 之前 */
  bookPrice: ['账面前单价', '账面单价', '账面前价', '账面价格'],
  countPrice: ['盘点单价', '实盘单价', '盘点价'],
  bookAmount: ['账面金额', '账存金额', '账面价值'],
  countAmount: ['实盘金额', '盘点金额', '实存金额'],
  diffAmount: ['差异金额', '盘盈盘亏金额', '差额金额'],
  diffReason: ['差异原因', '差异说明', '差异事由'],
  /* 兜底：只有表头写的是裸词（数量/单价/金额）时才轮到它们 —— 必须排在所有带限定语的列之后 */
  qty: ['数量'],
  price: ['单价'],
  amount: ['金额'],
};

const LABELS = {
  warehouse: '仓库', itemCode: '存货编码', itemName: '存货名称', unit: '计量单位',
  bookQty: '账面数量', bookPrice: '账面前单价', bookAmount: '账面金额',
  countQty: '实盘数量', countPrice: '盘点单价', countAmount: '实盘金额',
  diffQty: '差异数量', diffAmount: '差异金额', diffReason: '差异原因',
  qty: '数量', price: '单价', amount: '金额',
};

/* 必需列：缺了就没法给出结论的定位与数量列。**只缺个别列照样给结论**（报「列缺失」），
   只有"空文本 / 认不出表头 / 没有明细行"才不给结论。 */
const REQUIRED = ['warehouse', 'itemCode', 'itemName', 'bookQty', 'countQty', 'diffQty', 'diffAmount'];
/* 合计行要逐列复核的列（明细逐行相加 = 合计） */
const SUM_ROLES = ['bookQty', 'bookAmount', 'countQty', 'countAmount', 'diffQty', 'diffAmount'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
/* 等式类核对（差异数量/差异金额、合计行）允许的分位四舍五入误差 */
const TOL = 0.01;
/* 乘法类核对（数量 × 单价 = 金额）多给一点点：两处单价各自四舍五入到分，误差会叠加 */
const MUL_TOL = 0.02;
/* 重大差异线：|差异金额| 超过账面金额的这个比例即提示 */
const MATERIAL_RATIO = 0.3;
/* 差异原因里出现这些词 ⇒ 等于没写原因（要求写清责任与处理） */
const UNCLEAR_WORDS = ['未查明', '尚未查明', '待查', '不详', '待查明'];

const CHECKS_GIVEN = [
  '合计行逐列复核（账面数量 / 账面金额 / 实盘数量 / 实盘金额 / 差异数量 / 差异金额）',
  '同一「仓库 + 存货编码」重复行检测',
  '差异数量 = 实盘数量 − 账面数量（不符报 P0）',
  '差异金额 = 实盘金额 − 账面金额（不符报 P0）',
  '账面金额 = 账面数量 × 账面前单价（不符报 P1，容差 0.02）',
  '实盘金额 = 实盘数量 × 盘点单价（不符报 P1，容差 0.02）',
  '空白与占位符检测（含必需列缺失 —— 只缺个别列照常给结论并报「列缺失」）',
];

const CHECKS_WITHHELD = [
  '差异金额为正（盘盈）但差异原因空白提示',
  '差异金额为负（盘亏）但差异原因空白提示',
  '差异金额绝对值超过账面金额 30%（重大差异）提示',
  '实盘数量为负（实盘数填错）检测',
  '差异原因为「未查明 / 待查 / 不详」提示（要求写清责任与处理）',
];

const OUT_OF_SCOPE = [
  '判断盘盈盘亏该走什么审批流程、怎么做账务调整（属于会计政策与授权判断）',
  '代替监盘程序、核对实物是否真实存在，也不出具审计或鉴证意见',
  '核对盘点表与 ERP / 存货系统的逐行明细（需要你自己先导出成文本贴进来）',
  '判断差异的责任归属、赔偿或考核（属于管理与法律判断）',
  '判断存货跌价准备与可变现净值（属于会计估计）',
];

/* 样例是**干净稿**：3 行明细 + 合计行，上面每一条等式都成立、有差异的行都写了原因、
   |差异金额| 都不到账面金额的 30%、实盘数量都非负 ⇒ 免费档与完整档都应当是 0 条发现。
   （样例不干净的话，对照测试里的"干净样例零误报"就恒真了，等于没测。） */
const SAMPLE_TEXT = [
  '仓库\t存货编码\t存货名称\t计量单位\t账面数量\t账面前单价\t账面金额\t实盘数量\t盘点单价\t实盘金额\t差异数量\t差异金额\t差异原因',
  '主料仓\tA001\t钢材\t吨\t100\t3000.00\t300000.00\t100\t3000.00\t300000.00\t0\t0.00\t无差异',
  '主料仓\tA002\t铝材\t吨\t50\t3000.00\t150000.00\t48\t3000.00\t144000.00\t-2\t-6000.00\t运输途中损耗，已由物流部确认',
  '成品仓\tB001\t成品A\t台\t200\t500.00\t100000.00\t202\t500.00\t101000.00\t2\t1000.00\t上期漏记入库，本期已补记',
  '合计\t\t\t\t350\t\t550000.00\t350\t\t545000.00\t0\t-5000.00\t',
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

/** 定位用：`钢材（主料仓/A001）`；连名称都没有就退化成行号——绝不编造一个存货名 */
const who = (it) => {
  const nm = String(it.itemName || '').trim();
  const wh = String(it.warehouse || '').trim();
  const code = String(it.itemCode || '').trim();
  const loc = [wh, code].filter((s) => s !== '').join('/');
  if (nm || loc) return `${nm || '(未填名称)'}${loc ? `（${loc}）` : ''}`;
  return `第 ${it.line} 行`;
};

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [], header: [] };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const missingColumns = REQUIRED.filter((r) => !cols.some((c) => c.role === r));
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => { if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i]; });
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header };
}

/* ================================ 免费档检查项 ================================ */

/** 1. 合计行逐列复核：明细逐行相加必须等于合计行填的数（差异表最常见的错就是合计没跟着改） */
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
        message: `合计行「${LABELS[role]}」填 ${stated}，但明细逐行相加是 ${sum}（差 ${round2(stated - sum)}）`,
        evidence: `合计=${stated}；明细合计=${sum}（${n} 行）`,
      });
    }
  }
  return out;
}

/** 2. 同一「仓库 + 存货编码」重复行检测：同一存货在同一仓库被盘了两次，差异会被重复计 */
function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const wh = String(it.warehouse || '').trim();
    const code = String(it.itemCode || '').trim();
    if (!wh && !code) continue;
    const key = `${wh}|${code}`;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「仓库 + 存货编码」完全相同（${key}）—— 可能重复计入差异`,
        evidence: `仓库=${wh}；存货编码=${code}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 3. 差异数量 = 实盘数量 − 账面数量（不符就是 P0：账实调整的数量直接是错的） */
function checkDiffQty(it) {
  const bq = normNumber(it.bookQty);
  const cq = normNumber(it.countQty);
  const dq = normNumber(it.diffQty);
  if (bq === null || cq === null || dq === null) return null;
  const expect = round2(cq - bq);
  if (Math.abs(expect - dq) > TOL) {
    return {
      line: it.line, level: 'P0', category: '差异数量不符',
      message: `${who(it)} 差异数量填 ${dq}，但实盘数量 ${cq} − 账面数量 ${bq} = ${expect}`,
      evidence: `账面数量=${bq}；实盘数量=${cq}；差异数量=${dq}；应为=${expect}`,
    };
  }
  return null;
}

/** 4. 差异金额 = 实盘金额 − 账面金额（不符就是 P0：过进账里的金额直接是错的） */
function checkDiffAmount(it) {
  const ba = normNumber(it.bookAmount);
  const ca = normNumber(it.countAmount);
  const da = normNumber(it.diffAmount);
  if (ba === null || ca === null || da === null) return null;
  const expect = round2(ca - ba);
  if (Math.abs(expect - da) > TOL) {
    return {
      line: it.line, level: 'P0', category: '差异金额不符',
      message: `${who(it)} 差异金额填 ${da}，但实盘金额 ${ca} − 账面金额 ${ba} = ${expect}`,
      evidence: `账面金额=${ba}；实盘金额=${ca}；差异金额=${da}；应为=${expect}`,
    };
  }
  return null;
}

/** 5. 账面金额 = 账面数量 × 账面前单价（容差 0.02） */
function checkBookAmount(it) {
  const bq = normNumber(it.bookQty);
  const bp = normNumber(it.bookPrice);
  const ba = normNumber(it.bookAmount);
  if (bq === null || bp === null || ba === null) return null;
  const expect = round2(bq * bp);
  if (Math.abs(expect - ba) > MUL_TOL) {
    return {
      line: it.line, level: 'P1', category: '账面金额与数量×单价不符',
      message: `${who(it)} 账面金额填 ${ba}，但账面数量 ${bq} × 账面前单价 ${bp} = ${expect}（差 ${round2(ba - expect)}）`,
      evidence: `账面数量=${bq}；账面前单价=${bp}；账面金额=${ba}；应为=${expect}`,
    };
  }
  return null;
}

/** 6. 实盘金额 = 实盘数量 × 盘点单价（容差 0.02） */
function checkCountAmount(it) {
  const cq = normNumber(it.countQty);
  const cp = normNumber(it.countPrice);
  const ca = normNumber(it.countAmount);
  if (cq === null || cp === null || ca === null) return null;
  const expect = round2(cq * cp);
  if (Math.abs(expect - ca) > MUL_TOL) {
    return {
      line: it.line, level: 'P1', category: '实盘金额与数量×单价不符',
      message: `${who(it)} 实盘金额填 ${ca}，但实盘数量 ${cq} × 盘点单价 ${cp} = ${expect}（差 ${round2(ca - expect)}）`,
      evidence: `实盘数量=${cq}；盘点单价=${cp}；实盘金额=${ca}；应为=${expect}`,
    };
  }
  return null;
}

/** 7. 空白与占位符检测：必需列缺失只报「列缺失」并**照常给结论**；明细里必需单元格空/占位符则报出来 */
function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')} —— 缺的列不参与核对，其余检查照常执行`,
      evidence: `表头=${header.join('|')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (missingColumns.indexOf(role) >= 0) continue;
      if (isBlank(it[role])) {
        out.push({
          line: it.line, level: 'P1', category: '空白或占位符',
          message: `${who(it)} 的「${LABELS[role]}」是空白或占位符 —— 这一行无法核对${LABELS[role]}`,
          evidence: `${LABELS[role]}=${it[role] === undefined ? '(空)' : it[role]}`,
        });
      }
    }
  }
  return out;
}

/* ============================== 完整档（付费）检查项 ============================== */

/** 完整档 1：差异金额为正（盘盈）却没写差异原因 —— 盘盈不写原因最容易被拿来藏账 */
/** 完整档 2：差异金额为负（盘亏）却没写差异原因 —— 盘亏不写原因是资产流失的典型口子 */
/** 完整档 3：|差异金额| 超过账面金额的 30% —— 达到这个量级就不是"正常损耗"，要单独说明并复核 */
/** 完整档 4：实盘数量为负 —— 实物不可能有负数，是抄串行或符号填反（P0） */
/** 完整档 5：差异原因写的是"未查明 / 待查 / 不详" —— 等于没写，要求写清责任与处理 */
/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') return insufficient(['材料文本为空：请把存货盘点表（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  const recognized = header.filter((h) => roleOf(h) !== null).length;
  if (!recognized) {
    return insufficient(['认不出表头：第一行必须是列名（仓库 / 存货编码 / 存货名称 / 账面数量 / 实盘数量 / 差异数量 / 差异金额 …）']);
  }
  if (!items.length) {
    return insufficient(['没有明细行：第一行必须是表头，且至少有一行明细（合计行可留）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkDiffQty(it), checkDiffAmount(it), checkBookAmount(it), checkCountAmount(it)];
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
        tolerance: TOL,
        executed_locally: true,
        network_used: false,
      },
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES,
};
