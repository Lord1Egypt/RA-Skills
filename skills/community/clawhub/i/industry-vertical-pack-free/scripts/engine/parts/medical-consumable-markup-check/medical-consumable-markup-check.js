'use strict';
/**
 * medical-consumable-markup-check-full.js —— 医院耗材加成与零差率核对引擎
 * （免费档 / 完整档共用源码；确定性、纯 Node 标准库、不联网）。
 *
 * 谁在什么时候必须做这件事：**医院 / 诊所每月结账与物价检查前**。
 * 卫生耗材这一块要同时讲清三件事：
 *   ① 进销存对得上：期初 + 入库 − 出库 = 结存（数量），结存 × 采购单价 = 结存金额；
 *   ② 零差率执行到位：政策写"零差率 / 据实收费"的品目，收费价不得高于采购单价；
 *   ③ 可收费耗材（含植入类）不得低于成本收费：收费价低于采购单价 = 每发一件亏一件。
 * 这三件事每月都由物价员 / 财务 / 耗材会计各算一遍，而**零差率品被加价、可收费耗材定价低于成本、
 * 进销存对不上被认定"账实不符"**正是每月都在发生的合规与亏损点。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来。
 * ⚠️ 每个等式后面标的是**它由哪一档执行** —— 没被执行的那一项绝不能写进"已核对 / 已勾稽"里：
 *
 *   结存数量 = 期初数量 + 入库数量 − 出库数量             免费档执行
 *   结存金额 = 结存数量 × 采购单价                         免费档执行
 *   加成率   =（收费价 − 采购单价）÷ 采购单价              免费档执行
 *   期初金额 + 入库金额 − 出库金额 = 结存金额               仅完整档执行（免费档把它列进未执行项）
 *
 * 与已有能力的区别：`hospital-supply-consumption-check` 核的是**药房 / 耗材库的进销存与科室领用**
 * （期初 + 入库 − 出库 − 科室领用 + 退货 = 期末结存、领用金额、单据重复过账）；
 * **完整档**核的是**收费价格与成本的关系**（加成率 / 零差率是否被加价 / 收费价是否低于成本）
 * 与金额侧的三段勾稽；**免费档只执行它自己的那 7 项**（上面四个等式里的前三个在其中，
 * 第四个列在 `CHECKS_WITHHELD` 里，属于未执行的检查项）——
 * 取数口径与结论层面都不同，不是重复品。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 7 项；完整档追加 4 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**只核表内可算关系**：不判断地方物价政策是否适用、不判断集采中选价 / 挂网价填得对不对，
 *    **不给医疗建议、不做诊疗判断**；表里给的采购单价、收费价、数量、金额一律**以你填的为准**。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 *
 * ⚠️ 档位开关用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把完整档检查包进以该常量为条件的 if 块（**不要**留「完整档才执行的检查」那类 MARKER ——
 *    两个形态同时存在时 strip_free_engine 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关 / 条件语句的字面量：strip_free_engine 的残渣断言认得那些字面量。
 */

const CHECKS_GIVEN = [
  '结存数量勾稽（期初数量 + 入库数量 − 出库数量 = 结存数量）',
  '结存金额勾稽（结存数量 × 采购单价 = 结存金额）',
  '加成率勾稽（（收费价 − 采购单价）÷ 采购单价 = 加成率）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '同一期间同一耗材重复行检测',
  '空白与占位符检测',
  '数量、单价或金额为负检测',
];

const CHECKS_WITHHELD = [
  '零差率（据实收费等不计加成）耗材被加价判定 —— 逐项给出单件价差与影响金额',
  '收费价低于采购成本的亏损判定 —— 逐项给出单件亏损与期间亏损金额',
  '进销存金额三段勾稽（期初金额 + 入库金额 − 出库金额 = 结存金额）—— 给出差异金额与折合数量',
  '按影响金额排序的「调整 / 申诉清单」（逐条带原文行号与建议动作）',
];

const OUT_OF_SCOPE = [
  '判断地方物价政策是否适用、医疗服务价格项目与耗材编码该挂哪一档（以医保局 / 卫健委发布的价格文件为准）',
  '判断集采中选价、挂网价、中标价本身填得对不对（以招采平台结果与调价文件为准）',
  '给出医疗、诊疗、用药与临床使用建议（本工具只核表内可算关系，不做任何诊疗判断）',
  '核对实物是否在库：账上勾稽通过**不代表**实物在场，那要靠耗材库实物盘点',
  '处理植入类耗材的追溯码 / UDI、跟台记录与患者计费明细的对应关系',
  '处理增值税、医保结算、DRG / DIP 支付与财政补助口径',
  '读取 HIS / SPD / 耗材管理系统 / Excel 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t耗材编码\t耗材名称\t规格型号\t计价单位\t采购单价\t收费价\t加成率\t价格政策\t期初数量\t入库数量\t出库数量\t结存数量\t期初金额\t入库金额\t出库金额\t结存金额',
  '2026-01\tHC-1001\t一次性使用输液器\t0.7mm\t支\t1.20\t1.20\t0.00%\t零差率\t200.00\t1000.00\t500.00\t700.00\t240.00\t1200.00\t600.00\t840.00',
  '2026-01\tHC-1002\t一次性使用无菌注射器\t5ml\t具\t0.45\t0.45\t0.00%\t零差率\t300.00\t2000.00\t1200.00\t1100.00\t135.00\t900.00\t540.00\t495.00',
  '2026-01\tHC-2001\t一次性使用无菌手术刀片\t15#\t片\t2.00\t2.20\t10.00%\t可收费加成\t100.00\t500.00\t200.00\t400.00\t200.00\t1000.00\t400.00\t800.00',
  '2026-01\tHC-3001\t一次性使用吻合器\t60mm\t把\t380.00\t380.00\t0.00%\t据实收费\t20.00\t60.00\t35.00\t45.00\t7600.00\t22800.00\t13300.00\t17100.00',
  '2026-02\tHC-1001\t一次性使用输液器\t0.7mm\t支\t1.20\t1.20\t0.00%\t零差率\t700.00\t500.00\t900.00\t300.00\t840.00\t600.00\t1080.00\t360.00',
  '合计\t\t\t\t\t\t\t\t\t1320.00\t4060.00\t2835.00\t2545.00\t9015.00\t26500.00\t15920.00\t19595.00',
].join('\n');

const TOL = 0.01;        // 数量与金额勾稽到分的容差
const RATE_TOL = 0.02;   // 加成率保留两位小数，容差 0.02 个百分点

/**
 * 引擎输出的免责声明 —— ⚠️ 这里列的等式**必须与实际执行的检查逐项一致**：
 * 免费档不做进销存金额三段勾稽，就一个字都不许把它写进"已核对"里（虚假保证 = 免费版不如实）。
 * 措辞按档位取：**本档的等式清单 = 本档真的执行的等式** —— 免费档是「三个等式」，
 * 完整档是「四个等式」（多出来的那一项就是进销存金额三段勾稽）。
 */
const DISCLAIMER_FREE = '只核"期初数量 + 入库数量 − 出库数量 = 结存数量"'
  + '"结存数量 × 采购单价 = 结存金额""（收费价 − 采购单价）÷ 采购单价 = 加成率"这三个等式这类**表内可算关系**'
  + '（"期初金额 + 入库金额 − 出库金额 = 结存金额"属于本次**未执行**的检查项，见 scope.checks_not_run，'
  + '本工具不会声称核过它）';

/** 两档共用的边界声明（与执行了哪几项无关） */
const DISCLAIMER_TAIL = '：以你提供的采购单价与收费标准为准，**不判断地方物价政策是否适用**，'
  + '不给医疗建议、不做诊疗判断；结论可由第三方用同一份输入复算。';

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的别名必须排在更宽泛的词前面**（宽泛别名把具体列抢走时不报缺列、只是算错）。
  //    · 「耗材编码」必须排在「耗材名称」前（两列都含"耗材"）；
  //    · **金额列必须排在数量列前**：否则「期初金额」「结存金额」会被「期初数量 / 结存数量」
  //      所在的宽泛别名抢走，四列金额会静默地不参与任何检查（算错但不会报缺列）；
  //    · 「收费价」不能被「采购单价」抢走，两者都要排在只写"单价"的兜底别名前。
  period: ['所属期间', '会计期间', '所属期', '期间', '月份', '月度'],
  code: ['耗材编码', '材料编码', '物资编码', '物料编码', '器械编码', '商品编码', '耗材编号', '编码'],
  name: ['耗材名称', '材料名称', '耗材品名', '器械名称', '品名', '耗材'],
  spec: ['规格型号', '规格', '型号'],
  unit: ['计价单位', '计量单位', '包装单位', '规格单位', '单位'],
  cost: ['采购单价', '进货单价', '购进单价', '购入单价', '成本单价', '进价', '成本价'],
  chargePrice: ['收费价', '收费价格', '收费单价', '零售价', '销售价', '收费标价', '医保支付价'],
  markupRate: ['加成率', '加价率', '加成比例', '毛利率'],
  policy: ['价格政策', '收费政策', '加成政策', '价格类别', '收费类别', '零差率'],
  amtBegin: ['期初金额', '期初存货金额', '期初库存金额', '期初余额金额', '期初结存金额'],
  amtIn: ['入库金额', '入库金额合计', '采购金额', '进货金额'],
  amtOut: ['出库金额', '发出金额', '领用金额', '消耗金额'],
  amtEnd: ['结存金额', '期末结存金额', '结存金额合计', '库存金额'],
  qtyBegin: ['期初数量', '期初库存数量', '期初结存数量', '期初数'],
  qtyIn: ['入库数量', '购进数量', '采购入库数量', '入库数'],
  qtyOut: ['出库数量', '发出数量', '领用数量', '消耗数量', '出库数'],
  qtyEnd: ['结存数量', '期末结存数量', '结存数', '库存数量'],
};

const LABELS = {
  period: '所属期间', code: '耗材编码', name: '耗材名称', spec: '规格型号', unit: '计价单位',
  cost: '采购单价', chargePrice: '收费价', markupRate: '加成率', policy: '价格政策',
  qtyBegin: '期初数量', qtyIn: '入库数量', qtyOut: '出库数量', qtyEnd: '结存数量',
  amtBegin: '期初金额', amtIn: '入库金额', amtOut: '出库金额', amtEnd: '结存金额',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'code', 'name', 'cost', 'chargePrice', 'markupRate', 'policy',
  'qtyBegin', 'qtyIn', 'qtyOut', 'qtyEnd', 'amtBegin', 'amtIn', 'amtOut', 'amtEnd'];
/** 合计行逐列复核的列（采购单价 / 收费价是"每单位"的量，加成率是"比率"，加总没有意义，刻意不列） */
const SUM_ROLES = ['qtyBegin', 'qtyIn', 'qtyOut', 'qtyEnd', 'amtBegin', 'amtIn', 'amtOut', 'amtEnd'];
/** 免费档负值检测覆盖的列（数量侧、单价侧与金额侧） */
const NEG_ROLES = ['qtyBegin', 'qtyIn', 'qtyOut', 'qtyEnd', 'cost', 'chargePrice',
  'amtBegin', 'amtIn', 'amtOut', 'amtEnd'];
/** 「同一行被粘贴两遍」的数值指纹：这几列逐列相同才算重复行 */
const SIG_ROLES = ['cost', 'chargePrice', 'markupRate', 'qtyBegin', 'qtyIn', 'qtyOut', 'qtyEnd',
  'amtBegin', 'amtIn', 'amtOut', 'amtEnd'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;
/**
 * 「按进价收费、不得加价」的政策口径关键词。
 * ⚠️ 这是**以你填在「价格政策」列里的原文为准**的文本匹配，不是我们对地方物价政策的判断：
 *    政策列没写、认不出来时本工具不下任何结论（那属于 checks_out_of_scope）。
 */
const ZERO_MARKUP_RE = /零差率|零差价|零加成|不计加成|不加成|平进平出|据实收费|据实结算|按进价|按采购价/;

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

/** 归一化数量 / 金额：认千分位、货币符号、百分号、Unicode 负号与尾部计量单位（支 / 具 / 片 / 把 …） */
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
    if (isTotal) { totals.row = row; totals.line = i + 1; } else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && str(it.period) !== '' ? str(it.period) : `第 ${it && it.line} 行`;
  const n = [str(it && it.code), str(it && it.name)].filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => str(it && it.period) || `第 ${it && it.line} 行`;

/** 影响金额 = 单件价差 × 本期出库数量；出库数量缺失时**如实返回 null**（不编造影响金额） */
/** 计量单位后缀（只用于给影响金额加个可读的单位） */
/* ================================ 免费档检查项 ================================ */

/** 结存数量 = 期初数量 + 入库数量 − 出库数量 */
function checkBalanceQty(it) {
  const begin = normNumber(it.qtyBegin);
  const inn = normNumber(it.qtyIn);
  const outQty = normNumber(it.qtyOut);
  const stated = normNumber(it.qtyEnd);
  if (begin === null || inn === null || outQty === null || stated === null) return null;
  const expect = round2(begin + inn - outQty);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '结存数量与复算不符', line: it.line,
    message: `${who(it)}：期初 ${begin.toFixed(2)} + 入库 ${inn.toFixed(2)} − 出库 ${outQty.toFixed(2)} `
      + `= ${expect.toFixed(2)}，表里「结存数量」是 ${stated.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`
      + '数量对不上是最容易被认定"账实不符"的一格：多半是出库漏登（科室先拿走、单据后补），'
      + '或者退货 / 报损只是口头冲减、没有回填本表。',
  };
}

/** 结存金额 = 结存数量 × 采购单价（按进价计价的库存金额口径） */
function checkBalanceAmt(it) {
  const qty = normNumber(it.qtyEnd);
  const cost = normNumber(it.cost);
  const stated = normNumber(it.amtEnd);
  if (qty === null || cost === null || stated === null) return null;
  const expect = round2(qty * cost);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '结存金额与复算不符', line: it.line,
    message: `${who(it)}：结存数量 ${qty.toFixed(2)} × 采购单价 ${cost.toFixed(2)} `
      + `= ${expect.toFixed(2)}，表里「结存金额」是 ${stated.toFixed(2)}，`
      + `相差 ${round2(stated - expect).toFixed(2)}。`
      + '本工具按**采购单价（进价）**核库存金额：如果贵院的结存金额是按收费价或调拨价计的，'
      + '这一格的口径要先统一，否则它会一直报。',
  };
}

/** 加成率 =（收费价 − 采购单价）÷ 采购单价 */
function checkMarkupRate(it) {
  const cost = normNumber(it.cost);
  const charge = normNumber(it.chargePrice);
  const stated = normNumber(it.markupRate);
  if (cost === null || charge === null || stated === null) return null;
  if (Math.abs(cost) <= 1e-9) return null;      // 采购单价为 0 时加成率没有定义 ⇒ 不给结论
  const expect = round2((charge - cost) / cost * 100);
  if (Math.abs(expect - stated) <= RATE_TOL) return null;
  return {
    level: 'P1', category: '加成率与复算不符', line: it.line,
    message: `${who(it)}：按（收费价 ${charge.toFixed(2)} − 采购单价 ${cost.toFixed(2)}）`
      + `÷ ${cost.toFixed(2)} = ${expect}%，表里「加成率」是 ${stated}%。`
      + '加成率是物价检查的取数口径：它错了，通常意味着收费价或采购单价有一边用错了版本'
      + '（旧调价文件 / 含税与不含税混用 / 把集采价填成了配送价）。',
  };
}

/** 合计行逐列复核 */
function collectTotalRow(totals, items) {
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
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的`
        + `「${LABELS[role]}」相加是 ${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
        + '合计行就是进销存月报与盘点表的取数口径，对不上说明有一边错。',
    });
  }
  return out;
}

/** 同一期间 + 同一耗材编码 + 各列数值逐列相同 = 同一行被粘贴了两遍 */
function collectDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = str(it.period);
    const c = str(it.code);
    if (!p || !c) continue;
    const sig = SIG_ROLES.map((role) => {
      const v = normNumber(it[role]);
      return v === null ? '-' : v.toFixed(2);
    }).join('|');
    const key = `${p}|${c}|${sig}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一期间同一耗材重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已经出现过，第 ${it.line} 行同一期间、同一耗材编码、`
          + '各列数量金额逐列相同 —— 这是同一行被粘贴了两遍：重复行会把入库、出库、结存与金额'
          + '全部重复计一遍，整张表的合计数会跟着虚高。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 关键列为空或占位符 */
function collectBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = str(it[role]);
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算做不了：缺哪一列就补哪一列，'
            + '本工具不会用 0 或默认值替你填（那会把"没查"伪装成"没问题"）。',
        });
      }
    }
  }
  return out;
}

/** 数量、单价或金额为负 */
function collectNegatives(items) {
  const out = [];
  for (const it of items) {
    for (const role of NEG_ROLES) {
      const v = normNumber(it[role]);
      if (v === null || v >= -TOL) continue;
      out.push({
        level: 'P0', category: '数量或金额为负', line: it.line,
        message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）。`
          + '数量、采购单价、收费价与四栏金额都不该为负：红字冲回 / 反向退库应当单独列示并说明，'
          + '否则正负相抵会让整张表"看起来是平的"。',
      });
    }
  }
  return out;
}

/* ====================== 完整档（买断档）才执行的合规判定与清单 ====================== */

/** 零差率 / 据实收费的耗材被加价（以「价格政策」列原文为准） */
/** 收费价低于采购成本：每发一件亏一件（可收费耗材 / 植入类尤其常见） */
/** 进销存金额三段勾稽：期初金额 + 入库金额 − 出库金额 = 结存金额 */
/** 处理清单：按影响金额从大到小排序（影响金额算不出来的排在最后，如实标注） */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 10) {
    return insufficient('没有收到医院耗材加成与零差率核对表正文（text）—— 请把「所属期间 / 耗材编码 / '
      + '耗材名称 / 规格型号 / 计价单位 / 采购单价 / 收费价 / 加成率 / 价格政策 / 期初数量 / 入库数量 / '
      + '出库数量 / 结存数量 / 期初金额 / 入库金额 / 出库金额 / 结存金额」这张表贴上（含表头，Tab 分隔最稳）');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `医院耗材加成与零差率核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何耗材明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    const a = checkBalanceQty(it); if (a) findings.push(a);
    const b = checkBalanceAmt(it); if (b) findings.push(b);
    const c = checkMarkupRate(it); if (c) findings.push(c);

  }
  findings.push(...collectTotalRow(t.totals, t.items));
  findings.push(...collectDuplicates(t.items));
  findings.push(...collectBlanks(t.items));
  findings.push(...collectNegatives(t.items));

  const notRun = [];
  notRun.push.apply(notRun, CHECKS_WITHHELD);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;

  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const v = normNumber(it[role]);
    return s + (v === null ? 0 : v);
  }, 0));
  let chargeAmt = 0;
  for (const it of t.items) {
    const q = normNumber(it.qtyOut);
    const p = normNumber(it.chargePrice);
    if (q !== null && p !== null) chargeAmt += q * p;
  }

  const result = {
    status: 'success',
    service_type: 'MEDICAL_CONSUMABLE_MARKUP_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      policy_basis: '零差率 / 据实收费等口径**以你在「价格政策」列填写的原文为准**，不判断地方物价政策适用性',
      qty_end_total: sumOf('qtyEnd'),
      amt_end_total: sumOf('amtEnd'),
      charge_amount_total: round2(chargeAmt),
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
    disclaimer: (DISCLAIMER_FREE) + DISCLAIMER_TAIL,
  };

  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, REQUIRED, SUM_ROLES, ZERO_MARKUP_RE,
};
