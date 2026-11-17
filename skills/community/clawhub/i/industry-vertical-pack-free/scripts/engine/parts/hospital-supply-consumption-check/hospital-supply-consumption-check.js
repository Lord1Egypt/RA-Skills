/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * hospital-supply-consumption-check.js —— 药品耗材进销存与科室领用核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**医院 / 诊所每月结账前**。药房与耗材库每个月都要把
 * 进货（入库）、发货（出库）、科室领用、退货与期末结存逐笔勾稽一遍；账实不符就是
 * 药品耗材流失的信号，也是医保飞行检查最先翻的那本账。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   期末结存数量 = 期初结存数量 + 入库数量 − 出库数量 − 科室领用数量 + 退货数量
 *   领用金额     = 科室领用数量 × 单价
 *   合计行各列   = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**药品耗材该按什么价格入库、科室领用该不该批、效期报废该怎么入账
 *    （那属于药事管理、物价与医保政策判断）：表里给的期初、入库、出库、科室领用、退货、
 *    单价、入库单价、中标价一律**以你填的为准**，本工具只核表内勾稽，并按原文行号列出可疑处。
 * ⚠️ 账上勾稽通过**不代表**实物在场 —— 那要靠药房 / 耗材库实物盘点（见 checks_out_of_scope）。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '期末结存数量复算（期初 + 入库 − 出库 − 科室领用 + 退货 = 期末结存）',
  '领用金额复算（科室领用数量 × 单价 = 领用金额）',
  '合计行逐列复核',
  '同一药品编码同一期间重复行检测',
  '空白与占位符检测',
  '数量或金额为负检测',
];

const CHECKS_WITHHELD = [
  '出库数量超过期初加入库提示（仓库里没有的量发不出去）',
  '期末结存为负提示（账上不可能有负库存）',
  '领用数量超过出库数量提示（科室领用必须先有出库）',
  '单价与中标价 / 采购价不一致提示',
  '同一药品同一期间重复入库（同一单据号）提示',
];

const OUT_OF_SCOPE = [
  '判断药品耗材该按什么价格入库、科室领用该不该批（属于药事管理、采购合同与审批流程）',
  '核对实物是否在场：账上勾稽**不代表**实物在库，那要靠药房 / 耗材库实物盘点',
  '判断中标价 / 挂网价 / 集采价本身填得对不对（以招采平台、集采中选结果与调价文件为准）',
  '效期报废、破损、赠送、拆零与整包装单位换算的业务处理（请按本单位药事制度单独列示）',
  '处理增值税、医保结算、财政补助与药品零差率的会计与税务口径',
  '读取 HIS / 药房系统 / SPD / 耗材库系统的导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t药品编码\t药品名称\t单位\t期初结存数量\t入库数量\t入库单价\t出库数量\t科室领用数量\t退货数量\t期末结存数量\t单价\t领用金额\t中标价\t单据号',
  '2026-01\tYP-1001\t阿莫西林胶囊 0.25g\t盒\t100.00\t800.00\t4.50\t400.00\t380.00\t20.00\t140.00\t4.50\t1710.00\t4.50\tRK-20260101',
  '2026-01\tHC-2001\t一次性输液器 0.7mm\t支\t200.00\t1000.00\t1.20\t500.00\t480.00\t0.00\t220.00\t1.20\t576.00\t1.20\tRK-20260102',
  '2026-02\tYP-1001\t阿莫西林胶囊 0.25g\t盒\t140.00\t300.00\t4.50\t200.00\t190.00\t0.00\t50.00\t4.50\t855.00\t4.50\tRK-20260201',
  '2026-02\tHC-2001\t一次性输液器 0.7mm\t支\t220.00\t400.00\t1.20\t300.00\t280.00\t10.00\t50.00\t1.20\t336.00\t1.20\tRK-20260202',
  '合计\t\t\t\t660.00\t2500.00\t\t1400.00\t1330.00\t30.00\t460.00\t\t3477.00\t\t',
].join('\n');

const TOL = 0.01;              // 算术复算容差（数量与金额都精确勾稽到分）
const PRICE_TOL = 0.01;        // 单价比对：0.01 元以内的差算四舍五入
const PRICE_REL_TOL = 0.001;   // 单价比对：中标价的 0.1%（大额单价的小数尾差不算不一致）

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的别名必须排在更宽泛的词前面**（第 232 轮的坑：
  //    宽泛别名把具体列抢走时**不报缺列、只是算错**）。
  //    · 「科室领用数量」必须排在「领用数量」「领用」前 —— 否则整列被抢，领用金额与结存全错；
  //    · 「期末结存数量」必须排在「结存数量」「期末」前；
  //    · 「入库单价」必须排在「单价」前 —— 否则入库单价被当成核算单价，两边一起报错；
  //    · 「领用金额」必须排在「科室领用数量 / 领用数量」前（金额列含"领用"两个字，
  //      被数量列抢走时 15 个表头只会解析出 14 个字段 —— header_map_check 会当场报"列被覆盖"）；
  //    · 「出库单价」必须由 price 认走，所以 price 必须排在「出库数量」所在的 qtyOut 前；
  //    · 「中标单价」必须由 bidPrice 认走，所以 bidPrice 必须排在 price 前。
  period: ['所属期间', '会计期间', '所属期', '期间', '月份', '月度'],
  code: ['药品编码', '耗材编码', '药品编号', '耗材编号', '物资编码', '物料编码', '器械编码', '商品编码', '存货编码', '编码'],
  name: ['药品名称', '耗材名称', '材料名称', '药品品名', '耗材品名', '器械名称', '品名', '药品', '耗材'],
  unit: ['计量单位', '包装单位', '规格单位', '单位'],
  qtyBegin: ['期初结存数量', '期初库存数量', '期初数量', '期初结存', '期初余额', '期初'],
  inPrice: ['入库单价', '进货单价', '购进单价', '购入单价', '进价'],
  bidPrice: ['中标价', '中标单价', '中标价格', '挂网价', '集采价', '采购价格', '采购价', '医保支付价'],
  price: ['领用单价', '出库单价', '领用价格', '核算单价', '单价'],
  amount: ['领用金额', '领用成本', '领用合计', '发出金额', '金额'],
  qtyIn: ['入库数量', '购进数量', '采购入库数量', '入库数', '入库量'],
  qtyOut: ['出库数量', '发出数量', '出库数', '出库量', '出库'],
  deptQty: ['科室领用数量', '科室领用量', '临床领用数量', '护理领用数量', '科室领用', '领用数量', '领用量', '耗用数量', '领用'],
  qtyReturn: ['退货数量', '退回数量', '退库数量', '退料数量', '退货量', '退货'],
  qtyEnd: ['期末结存数量', '期末库存数量', '期末结存', '结存数量', '期末数量', '期末余额', '结存', '期末'],
  docNo: ['单据号', '入库单号', '单据编号', '进货单号', '单号', '凭证号'],
};

const LABELS = {
  period: '所属期间', code: '药品编码', name: '药品名称', unit: '单位',
  qtyBegin: '期初结存数量', qtyIn: '入库数量', inPrice: '入库单价', qtyOut: '出库数量',
  deptQty: '科室领用数量', qtyReturn: '退货数量', qtyEnd: '期末结存数量',
  price: '单价', amount: '领用金额', bidPrice: '中标价', docNo: '单据号',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'code', 'qtyBegin', 'qtyIn', 'qtyOut', 'deptQty', 'qtyReturn',
  'qtyEnd', 'price', 'amount'];
/** 合计行逐列复核的列（单价是"每单位"的量，加总没有意义，刻意不列） */
const SUM_ROLES = ['qtyBegin', 'qtyIn', 'qtyOut', 'deptQty', 'qtyReturn', 'qtyEnd', 'amount'];
/**
 * 免费档负值检测覆盖的列：**数量侧与金额侧**。
 * ⚠️ 刻意**不含**期末结存数量 —— "期末结存为负"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出期末结存为负就等于把付费结论送出去了。
 * ⚠️ 也刻意不查中标价：它是对比用的参考价，"中标价为负"属于材料本身填错，由人工看。
 */
const NEG_ROLES = ['qtyBegin', 'qtyIn', 'qtyOut', 'deptQty', 'qtyReturn', 'price', 'inPrice', 'amount'];
/** 「同一行被粘贴两遍」的数值指纹：这几列逐列相同才算重复行（不含单据号，见 checkDuplicates） */
const SIG_ROLES = ['qtyBegin', 'qtyIn', 'qtyOut', 'deptQty', 'qtyReturn', 'qtyEnd', 'price', 'inPrice', 'amount', 'bidPrice'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（不会输出「未发现问题」）。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–−]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

/** 归一化数量 / 金额：认千分位、货币符号、百分号、Unicode 负号与尾部计量单位（盒 / 支 / 袋 / 瓶 …） */
function normNumber(raw) {
  if (isBlank(raw)) return null;
  let s = String(raw).trim()
    .replace(/[−–—]/g, '-')
    .replace(/[,，\s¥￥$]/g, '')
    .replace(/%$/, '');
  s = s.replace(/[^\d.]*$/, '');
  if (!s || !/^[-+]?(\d+(\.\d*)?|\.\d+)$/.test(s)) return null;
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

const round2 = (n) => Math.round(n * 100) / 100;

const str = (v) => (v === undefined || v === null ? '' : String(v).trim());

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
    roles.forEach((role, c) => {
      if (!role) return;
      row[role] = cells[c] === undefined ? '' : cells[c];
    });
    const head = str(cells[0]);
    const periodCell = str(row.period);
    const isTotal = TOTAL_WORDS.test(head) || TOTAL_WORDS.test(periodCell);
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && str(it.period) !== '' ? str(it.period) : `第 ${it && it.line} 行`;
  const n = [str(it && it.code), str(it && it.name)].filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = str(it && it.period);
  return p || `第 ${it && it.line} 行`;
};

/** 数值指纹：把 SIG_ROLES 归一化后拼成字符串（空值记 '-'，缺列也认） */
const numSignature = (it) => SIG_ROLES
  .map((role) => {
    const v = normNumber(it[role]);
    return v === null ? '-' : v.toFixed(2);
  })
  .join('|');

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

/** 期末结存数量 = 期初 + 入库 − 出库 − 科室领用 + 退货 */
function checkEndQtyRolling(it) {
  const out = [];
  const begin = normNumber(it.qtyBegin);
  const inn = normNumber(it.qtyIn);
  const outQty = normNumber(it.qtyOut);
  const dept = normNumber(it.deptQty);
  const back = normNumber(it.qtyReturn);
  const stated = normNumber(it.qtyEnd);
  if (begin === null || inn === null || outQty === null || dept === null
    || back === null || stated === null) return out;
  const expect = round2(begin + inn - outQty - dept + back);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '期末结存数量复算不符', line: it.line,
    message: `${who(it)}：期初 ${begin.toFixed(2)} + 入库 ${inn.toFixed(2)} − 出库 ${outQty.toFixed(2)} `
      + `− 科室领用 ${dept.toFixed(2)} + 退货 ${back.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「期末结存数量」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '这一格是五笔业务的汇总：对不上说明有一笔漏记、串了科室，或者退货没有冲回库存 —— '
      + '账实不符正是药品耗材流失与医保飞检最先翻的那一笔。',
  });
  return out;
}

/** 领用金额 = 科室领用数量 × 单价 */
function checkAmountRecompute(it) {
  const out = [];
  const dept = normNumber(it.deptQty);
  const price = normNumber(it.price);
  const stated = normNumber(it.amount);
  if (dept === null || price === null || stated === null) return out;
  const expect = round2(dept * price);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '领用金额复算不符', line: it.line,
    message: `${who(it)}：科室领用数量 ${dept.toFixed(2)} × 单价 ${price.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「领用金额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '金额是数量乘单价乘出来的：差在这里多半是单价用错了版本（中标价 / 入库价 / 零售价混用）、'
      + '或者退货没有从领用里冲减，也可能是拆零与整包装的单位换算没做。',
  });
  return out;
}

/** 合计行逐列复核 */
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
        + `相差 ${round2(stated - expect).toFixed(2)}。`
        + '合计行就是月报、进销存台账与盘点表的取数口径，对不上说明有一边错。',
    });
  }
  return out;
}

/**
 * 同一药品编码 + 同一期间出现**内容逐列相同**的多行（同一行被粘贴了两遍）。
 * ⚠️ 判据要求数值指纹一致：同一期间同一药品"两次金额并不相同的入库"不是"重复行"，
 *    它属于单据层面的重复过账，由完整档那一条检查项负责 —— 两档的结论因此互不串味
 *    （免费档不会漏出付费结论，付费档也不靠"多报一条"撑场面）。
 */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = str(it.period);
    const c = str(it.code);
    if (!p || !c) continue;
    const key = `${p}|${c}|${numSignature(it)}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一药品编码同一期间重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一药品编码、`
          + '各列数量金额逐列相同 —— 这是同一行被粘贴了两遍：'
          + '重复的那一行会把期初、入库、出库、科室领用与期末结存全部重复计一遍，'
          + '整张表的合计数会跟着虚高。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 关键列为空或占位符 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = str(it[role]);
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

/** 数量或金额为负（期末结存为负归完整档） */
function checkNegative(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '数量或金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 期初、入库、出库、科室领用、`
        + '退货、单价与领用金额都不该为负：红字冲回 / 反向退库应当单独列示并在备注里说明，'
        + '否则五笔业务会被负号悄悄抵消。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 出库数量超过期初 + 入库 */
/** 期末结存为负 */
/** 科室领用数量超过出库数量 */
/** 单价与中标价 / 采购价不一致（中标价列缺失或为空时退回按入库单价比对） */
/** 同一药品 + 同一期间 + 同一单据号出现多行入库（各行内容不同 = 同一入库单被重复过账） */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到药品耗材进销存与科室领用核对表正文（text）—— 请把「所属期间 / 药品编码 / 药品名称 / 单位 / 期初结存数量 / 入库数量 / 入库单价 / 出库数量 / 科室领用数量 / 退货数量 / 期末结存数量 / 单价 / 领用金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `药品耗材进销存与科室领用核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何药品耗材明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkEndQtyRolling(it));
    findings.push(...checkAmountRecompute(it));
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

  let deptTotal = 0;
  let amountTotal = 0;
  for (const it of t.items) {
    const d = normNumber(it.deptQty);
    if (d !== null) deptTotal += d;
    const a = normNumber(it.amount);
    if (a !== null) amountTotal += a;
  }

  const result = {
    status: 'success',
    service_type: 'HOSPITAL_SUPPLY_CONSUMPTION_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      dept_qty_total: round2(deptTotal),
      consume_amount_total: round2(amountTotal),
      tolerance: TOL,
      price_tolerance: PRICE_TOL,
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
    disclaimer: '只核"期初 + 入库 − 出库 − 科室领用 + 退货 = 期末结存"与"科室领用数量 × 单价 = 领用金额"这类**表内勾稽**与档位提示，'
      + '**不判断药品耗材该按什么价格入库、科室领用该不该批、效期报废该怎么入账**（以药事制度、招采文件与医保口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
