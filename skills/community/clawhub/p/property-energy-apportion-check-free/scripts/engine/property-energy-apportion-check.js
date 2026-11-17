/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * property-energy-apportion-check-full.js —— 物业公共能耗分摊核对（完整档 / 买断版）
 *
 * 谁在什么时候必须做这件事：**每个月出账单之前**。物业把公共区域的电和水
 * （公共照明、电梯、水泵、绿化）先抄总表、再摊到各楼栋 / 各户，然后才发账单、才上公示栏。
 * 这张表算错只有两个方向：**少摊**（钱收不回来，物业自己贴）或**多摊**（业主截图、拒缴、投诉）。
 * 两条都会在催缴单、公示栏和投诉件上被翻出来。
 *
 * 好消息：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   本期用量     = 本期读数 − 上期读数
 *   分摊比例     = 分摊基数 ÷ 该组分摊基数合计（分摊口径就是"按什么摊"的那一列文字）
 *   分摊能耗量   = 本期用量 × 分摊比例
 *   分摊额       = 分摊能耗量 × 分摊单价，或 公共总费用 × 分摊比例
 *   分摊额合计   = 公共总费用（按「期间 + 费用项目」去重，只算一次）
 *   分摊比例合计 = 100%
 *   损耗分摊额   = 本期用量 × 损耗率（表里有损耗列时）
 * 分摊单价是**元 / 计量单位**（每组一个价，如 6.00 元/度），所以 分摊额 = 分摊能耗量 × 分摊单价。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），不读环境变量、不写盘。
 *
 * 免费档执行前面 6 项；完整档（买断版）在同一个函数里继续执行追加的检查项（见 CHECKS_WITHHELD）。
 * 材料不足时**绝不给结论**（status = 'insufficient_input'），并逐条列出还缺什么。
 *
 * ⚠️ 本工具**不判断**公共总费用本身真不真实、把物业自用电混进来没有、分摊方式是否合法有效、
 *    空置房该不该优惠、损耗率定得合不合理、转供电加价是否合规 —— 这些都在 OUT_OF_SCOPE 里写清了。
 */

const CHECKS_GIVEN = [
  '总表读数差 = 本期读数 − 上期读数（逐条主表行复算）',
  '分摊额逐行复算（分摊能耗量 × 分摊单价，或 公共总费用 × 分摊比例）',
  '各户分摊合计 = 公共总费用勾稽（金额 / 能耗量两条口径）',
  '分摊比例合计 = 100%（按「期间 + 费用项目」分组）',
  '重复房号、空缺列与占位符检测',
  '分摊额超过公共总费用提示（逐行上限）',
];

const CHECKS_WITHHELD = [
  '跨楼栋 / 跨期间汇总台账（按期间、按楼栋两个维度的汇总视图）',
  '按多摊金额排序的处理清单（多摊在前、少摊在后，可直接拿去改账）',
  '差异归因：总表读数 / 损耗分摊 / 单价口径 / 基数口径 逐类排查',
  '损耗分摊额勾稽（本期用量 × 损耗率）与 分摊口径 ↔ 分摊基数 口径一致性',
];

const OUT_OF_SCOPE = [
  '判断公共总费用本身是否真实、是否把物业自用电（办公室、门岗、广告位、员工宿舍）混进了公共能耗（以供电 / 供水公司账单和物业账为准）',
  '核对分摊方式（按建筑面积 / 按户数 / 按人数 / 阶梯、各业态不同系数）是否符合物业服务合同与管理规约',
  '判断空置房、未售房、开发商产权房、公共部位是否应当分摊及其优惠口径（以合同、地方规定与业委会决议为准）',
  '判断损耗率定得合不合理、总表与分表差值该不该由业主承担',
  '处理转供电加价、增值税、公共收益冲抵、政府补贴、滞纳金等价格与税务问题',
  '读取物业收费系统 / Excel / 电表照片（需要你先导出或抄成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t费用项目\t楼栋\t上期读数\t本期读数\t本期用量\t分摊能耗量\t分摊单价\t公共总费用\t分摊基数\t分摊口径\t分摊比例\t分摊额',
  '2026-06\t公共照明\t1号楼\t1800.00\t2400.00\t600.00\t600.00\t6.00\t7200.00\t500.00\t建筑面积㎡\t50.00%\t3600.00',
  '2026-06\t公共照明\t2号楼\t1200.00\t1600.00\t400.00\t360.00\t6.00\t7200.00\t300.00\t建筑面积㎡\t30.00%\t2160.00',
  '2026-06\t公共照明\t3号楼\t600.00\t800.00\t200.00\t240.00\t6.00\t7200.00\t200.00\t建筑面积㎡\t20.00%\t1440.00',
  '2026-06\t电梯用电\t1号楼\t1350.00\t1800.00\t450.00\t600.00\t12.00\t12000.00\t1200.00\t建筑面积㎡\t60.00%\t7200.00',
  '2026-06\t电梯用电\t2号楼\t900.00\t1250.00\t350.00\t240.00\t12.00\t12000.00\t720.00\t建筑面积㎡\t24.00%\t2880.00',
  '2026-06\t电梯用电\t3号楼\t600.00\t800.00\t200.00\t160.00\t12.00\t12000.00\t480.00\t建筑面积㎡\t16.00%\t1920.00',
  '2026-06\t绿化用水\t1号楼\t300.00\t400.00\t100.00\t100.00\t5.00\t1000.00\t500.00\t建筑面积㎡\t50.00%\t500.00',
  '2026-06\t绿化用水\t2号楼\t180.00\t240.00\t60.00\t60.00\t5.00\t1000.00\t300.00\t建筑面积㎡\t30.00%\t300.00',
  '2026-06\t绿化用水\t3号楼\t120.00\t160.00\t40.00\t40.00\t5.00\t1000.00\t200.00\t建筑面积㎡\t20.00%\t200.00',
  '合计\t\t\t\t\t2350.00\t1400.00\t\t15400.00\t3000.00\t\t\t15400.00',
].join('\n');

const TOL = 0.05;             // 金额容差：5 分（分摊表按户四舍五入到分，合计会差几分）
const TOL_OVER = 0.05;        // "超上限"判据的容差（5 分）
const PCT_SCALE_TOL = 0.005;  // 比例（百分数形式）容差：0.005 个百分点

/* —— 表头 → 角色。顺序即优先级：更具体的别名必须排在更宽泛的前面 ——
   （「损耗分摊额」不能被「分摊额」抢走、「分摊单价」不能排在「公共总费用」后面、
     「分摊口径」不能被「分摊基数」抢走）—— tools/header_map_check.py 钉的就是这个坑。 */
const ROLES = {
  period: ['所属期间', '账单期间', '费用期间', '会计期间', '抄表期间', '所属期', '期间', '月份', '月度'],
  feeItem: ['费用项目', '能耗项目', '公摊项目', '费用类别', '费用类型', '能源类型', '项目名称', '能源种类'],
  building: ['楼栋', '楼号', '楼座', '栋号', '幢', '分区', '区域', '小区'],
  meter: ['总表编号', '总表号', '公共总表', '计量表号', '总表', '表号'],
  prevReading: ['上期读数', '上期示数', '期初读数', '上月读数', '上期止度'],
  currReading: ['本期读数', '本期示数', '期末读数', '本月读数', '本期止度'],
  lossRate: ['损耗率', '线损率', '损耗比例'],
  lossAmt: ['损耗分摊额', '损耗金额', '损耗分摊', '分摊损耗'],
  unitPrice: ['分摊单价', '公共能耗单价', '能耗单价', '单价'],
  sharedTotal: ['公共总费用', '公共能耗总额', '公共区域能耗总额', '能耗总额', '公摊总额', '总费用'],
  base: ['分摊基数', '分摊面积', '计费面积', '建筑面积', '面积', '户数', '人数', '基数'],
  basis: ['分摊口径', '分摊方式', '计费口径', '分摊方法', '计费方式'],
  ratio: ['负担分摊比例', '分摊比例', '分摊率', '比例'],
  energy: ['分摊能耗量', '分摊用量', '分摊电量', '分摊水量'],
  apportioned: ['分摊额', '应分摊金额', '分摊金额', '本期分摊额', '本期应付'],
  usage: ['本期用量', '本期耗用量', '耗用量', '用电量', '抄见量', '用量'],
  note: ['备注', '说明', '附注'],
};

const LABELS = {
  period: '所属期间', feeItem: '费用项目', building: '楼栋', meter: '总表',
  prevReading: '上期读数', currReading: '本期读数', usage: '本期用量',
  lossRate: '损耗率', lossAmt: '损耗分摊额', unitPrice: '分摊单价',
  sharedTotal: '公共总费用', base: '分摊基数', basis: '分摊口径', ratio: '分摊比例',
  energy: '分摊能耗量', apportioned: '分摊额', note: '备注',
};

/** 必需角色：缺一个就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'feeItem', 'building', 'currReading', 'unitPrice', 'sharedTotal', 'base', 'ratio', 'apportioned'];
/** 合计行里**直接相加**的列（楼栋级明细行） */
const SUM_ROLES = ['usage', 'base', 'apportioned', 'energy', 'lossAmt'];
/** 合计行里**按「期间 + 费用项目」去重**再加的列（同一个总额在每组多行里重复出现，只算一次） */
const DEDUP_ROLES = ['sharedTotal', 'currReading', 'prevReading'];
/** 缺了就少一项检查的角色（不是"必需"，但影响"能核多少"） */
const OPTIONAL_ROLES = ['basis', 'prevReading', 'usage', 'energy'];
/** 一条明细行里**不该空着**的关键列 */
const KEY_ROLES = ['period', 'feeItem', 'building', 'unitPrice', 'base', 'ratio', 'apportioned'];
/** 负值检测覆盖的列：金额、单价、数量与比例都不该为负 */
const NEGATIVE_ROLES = ['unitPrice', 'sharedTotal', 'base', 'apportioned', 'usage', 'energy', 'lossAmt'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|汇总|汇总行|合计[:：]?)$/;

/* —— 契约工具函数 —— */

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  if (line.indexOf('|') >= 0 && line.split('|').length > 2) return line.split('|').map((s) => s.trim());
  if (line.indexOf(',') >= 0 && line.split(',').length > 2) return line.split(',').map((s) => s.trim());
  if (line.indexOf('，') >= 0 && line.split('，').length > 2) return line.split('，').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  let s = String(raw).trim().replace(/[¥￥$€£,，\s]/g, '');
  s = s.replace(/元|度|吨|千瓦时|千瓦|立方米|㎡|平方米/g, '');
  if (s === '' || /^[-—–－]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  let t = s.replace(/[()]/g, '');
  let pct = false;
  if (/%$/.test(t)) { pct = true; t = t.slice(0, -1); }
  else if (/‰$/.test(t)) { pct = true; t = t.slice(0, -1); }
  if (!/^[-+]?\d+(\.\d+)?$/.test(t)) return null;
  const n = Number(t);
  if (!Number.isFinite(n)) return null;
  const v = neg ? -n : n;
  return pct ? v / 100 : v;
}

const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–－]+$/.test(s)
    || /^(n\/?a|无|待填|待补|待定|不详|略|\?)$/i.test(s);
}

function roleOf(header) {
  if (header === undefined || header === null) return null;
  const h = String(header).trim().replace(/\s+/g, '');
  if (!h) return null;
  if (TOTAL_WORDS.test(h)) return 'total';
  for (const role of Object.keys(ROLES)) {
    for (const alias of ROLES[role]) {
      if (h === alias || h.indexOf(alias) >= 0) return role;
    }
  }
  return null;
}

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: advice || '请把公共能耗抄表与分摊明细表（含表头）贴进来；材料不足时本工具不做任何认定，也不套用默认值。',
  };
}

/* —— 解析：表头 + 明细行 + 合计行（行同时带 byRole 与扁平键，老式/新式守卫都能读）—— */
function parseTable(text) {
  const raw = String(text === undefined || text === null ? '' : text).replace(/^\uFEFF/, '');
  const lines = raw.split(/\r?\n/);
  const rows = [];
  for (let i = 0; i < lines.length; i += 1) {
    if (String(lines[i]).trim() === '') continue;
    rows.push({ line: i + 1, cells: splitRow(lines[i]), raw: String(lines[i]) });
  }
  if (!rows.length) return { items: [], totals: {}, missingColumns: ['整张表是空的'], header: [], headerLine: 0 };

  let hi = -1;
  let header = [];
  for (let i = 0; i < rows.length; i += 1) {
    const hits = rows[i].cells.map((c) => roleOf(c)).filter(Boolean).length;
    if (hits >= 3) { hi = i; header = rows[i].cells.map((c) => String(c).trim()); break; }
  }
  if (hi < 0) {
    return {
      items: [], totals: {}, header: [], headerLine: 0,
      missingColumns: ['认不出表头（第一行应含至少 3 个可识别列名，如 所属期间 / 分摊基数 / 分摊额）'],
    };
  }
  const headerRoles = header.map((h) => roleOf(h));
  const seen = new Set(headerRoles.filter(Boolean));
  const missingColumns = REQUIRED.filter((r) => !seen.has(r))
    .map((r) => '缺少必需列：' + (LABELS[r] || r));
  const missingOptional = OPTIONAL_ROLES.filter((r) => !seen.has(r)).map((r) => LABELS[r] || r);

  const at = (cells, role) => {
    const idx = headerRoles.indexOf(role);
    return idx >= 0 && idx < cells.length ? cells[idx] : undefined;
  };
  const items = [];
  const totals = {};
  for (let i = hi + 1; i < rows.length; i += 1) {
    const r = rows[i];
    const label = r.cells.length ? String(r.cells[0] || '').trim() : '';
    if (!label && r.cells.every((c) => String(c).trim() === '')) continue;
    const byRole = {};
    for (let k = 0; k < headerRoles.length; k += 1) {
      const role = headerRoles[k];
      if (!role || role === 'total') continue;
      const v = k < r.cells.length ? String(r.cells[k]).trim() : '';
      if (!(role in byRole)) byRole[role] = v;
    }
    const isTotal = TOTAL_WORDS.test(label)
      || (isBlank(at(r.cells, 'period')) && isBlank(at(r.cells, 'unitPrice'))
        && !isBlank(at(r.cells, 'apportioned')) && !isBlank(at(r.cells, 'sharedTotal')));
    if (isTotal) { totals.line = r.line; totals.raw = r.raw; totals.byRole = byRole; continue; }
    if (isBlank(at(r.cells, 'period')) && isBlank(at(r.cells, 'feeItem')) && isBlank(at(r.cells, 'building'))) continue;
    items.push(Object.assign({ line: r.line, raw: r.raw, byRole: byRole }, byRole));
  }
  return {
    items: items, totals: totals, missingColumns: missingColumns,
    missingOptional: missingOptional, header: header, headerLine: rows[hi].line,
  };
}

/* —— 分组与合计工具 —— */
const groupKey = (it) => String(it.period || '') + '\u0000' + String(it.feeItem || '');
const bldKey = (it) => String(it.building || '(未列楼栋)');
const lineOf = (it) => (it && it.line ? it.line : 0);
const money = (n) => (Math.round(n * 100) / 100).toFixed(2);

function itemText(it) {
  return [it.period, it.feeItem, it.building].filter((x) => !isBlank(x)).join(' · ');
}
function rowsOfGroup(items, key) { return items.filter((it) => groupKey(it) === key); }
function sumOf(items, role) {
  let s = 0;
  let n = 0;
  for (const it of items) {
    const v = normNumber(it[role]);
    if (v !== null) { s += v; n += 1; }
  }
  return { sum: round2(s), n: n };
}
/** 按「期间 + 费用项目」去重后的合计（同一总额在每组多行里重复，只算一次） */
function dedupSum(items, role) {
  const seen = new Set();
  const parts = [];
  for (const it of items) {
    const k = groupKey(it);
    if (seen.has(k)) continue;
    seen.add(k);
    const n = normNumber(it[role]);
    if (n !== null) parts.push({ key: k, value: n, line: it.line });
  }
  return parts;
}
function groupSharedTotal(items, key) {
  for (const it of items) if (groupKey(it) === key) return normNumber(it.sharedTotal);
  return null;
}
function groupBaseTotal(items, key) {
  let s = 0;
  for (const it of items) if (groupKey(it) === key) { const n = normNumber(it.base); if (n !== null) s += n; }
  return round2(s);
}
/** 该组本期用量合计（各楼栋分表读数差相加；总量行在表头里，不由这里推算） */
function groupUsageTotal(items, key) {
  let s = 0;
  for (const it of items) if (groupKey(it) === key) { const n = normNumber(it.usage); if (n !== null) s += n; }
  return round2(s);
}
/** 该组分摊能耗量合计（各户分摊能耗量相加） */
/** 明细行的比例（小数）：分摊比例列优先，空着就用 分摊基数 ÷ 该组分摊基数合计 */
function normRatio(it, items) {
  const r = normNumber(it.ratio);
  if (r !== null) return r;
  const b = normNumber(it.base);
  const t = groupBaseTotal(items, groupKey(it));
  if (b === null || !t) return null;
  return b / t;
}
/** 明细行的分摊能耗量：有该列就用，没有就用 该组用量 × 分摊比例 */
function energyOf(it, items) {
  const direct = normNumber(it.energy);
  if (direct !== null) return direct;
  const key = groupKey(it);
  const u = groupUsageTotal(items, key);
  const r = normRatio(it, items);
  return (!u || r === null) ? null : u * r;
}

/* —— 检查（免费档：1–6）—— */

/** 1. 总表读数差 = 本期读数 − 上期读数 */
function checkReadingDiff(it) {
  const prev = normNumber(it.prevReading);
  const curr = normNumber(it.currReading);
  const usage = normNumber(it.usage);
  if (prev === null || curr === null || usage === null) return [];
  const exp = round2(curr - prev);
  if (Math.abs(exp - round2(usage)) <= TOL) return [];
  return [{
    line: lineOf(it), level: 'P0', category: '总表读数差与用量不符',
    message: `${itemText(it) || '该行'}：本期读数 ${money(curr)} − 上期读数 ${money(prev)} = ${money(exp)}，表里用量填 ${money(usage)}，差 ${money(exp - usage)}`,
    expected: exp, actual: round2(usage),
  }];
}

/** 2. 分摊额逐行复算：分摊能耗量 × 分摊单价（该组单价 = 公共总费用 ÷ 该组用量） */
function checkApportioned(it, ctx) {
  const n = normNumber(it.apportioned);
  if (n === null) return [];
  const out = [];
  const key = groupKey(it);
  const e = energyOf(it, ctx.items);
  const u = normNumber(it.unitPrice);
  const gu = groupUsageTotal(ctx.items, key);
  const st = groupSharedTotal(ctx.items, key);
  const rate = u !== null ? u : ((gu && st !== null) ? st / gu : null);
  if (e !== null && rate !== null) {
    const exp = round2(e * rate);
    if (Math.abs(exp - round2(n)) > TOL) {
      out.push({
        line: lineOf(it), level: 'P0', category: '分摊额复算不符',
        message: `${itemText(it)}：分摊能耗量 ${money(e)} × 分摊单价 ${money(rate)} = ${money(exp)}，表里分摊额填 ${money(n)}，差 ${money(exp - n)}（口径：分摊能耗量 × 分摊单价）`,
        expected: exp, actual: round2(n),
      });
    }
    return out;
  }
  const r = normRatio(it, ctx.items);
  if (st !== null && r !== null) {
    const exp = round2(st * r);
    if (Math.abs(exp - round2(n)) > TOL) {
      out.push({
        line: lineOf(it), level: 'P0', category: '分摊额复算不符',
        message: `${itemText(it)}：公共总费用 ${money(st)} × 分摊比例 ${(r * 100).toFixed(2)}% = ${money(exp)}，表里分摊额填 ${money(n)}，差 ${money(exp - n)}（口径：公共总费用 × 分摊比例）`,
        expected: exp, actual: round2(n),
      });
    }
  }
  return out;
}

/** 3. 各户分摊合计 = 公共总费用 勾稽 */
function checkGroupTotal(it, ctx) {
  const key = groupKey(it);
  if (ctx.totalChecked.has(key)) return [];
  ctx.totalChecked.add(key);
  const rows = rowsOfGroup(ctx.items, key);
  const st = groupSharedTotal(ctx.items, key);
  if (st === null) return [];
  const out = [];
  const a = sumOf(rows, 'apportioned');
  if (a.n && Math.abs(a.sum - round2(st)) > TOL) {
    out.push({
      line: lineOf(it), level: 'P0', category: '各户分摊合计与公共总费用不符',
      message: `${it.period} · ${it.feeItem}：各户分摊额合计 ${money(a.sum)}（${a.n} 户相加），公共总费用 ${money(st)}，差 ${money(a.sum - st)}`,
      expected: round2(st), actual: a.sum,
    });
  }
  const e = sumOf(rows, 'energy');
  const u = normNumber(rows[0] && rows[0].unitPrice);
  if (e.n && u !== null) {
    const exp = round2(e.sum * u);
    if (Math.abs(exp - round2(st)) > TOL) {
      out.push({
        line: lineOf(it), level: 'P1', category: '各户分摊合计与公共总费用不符',
        message: `${it.period} · ${it.feeItem}：分摊能耗量合计 ${money(e.sum)} × 分摊单价 ${money(u)} = ${money(exp)}，公共总费用 ${money(st)}，差 ${money(exp - st)}（能耗量口径）`,
        expected: round2(st), actual: exp,
      });
    }
  }
  return out;
}

/** 4. 分摊比例合计 = 100% */
function checkRatioSum(it, ctx) {
  const key = groupKey(it);
  if (ctx.ratioChecked.has(key)) return [];
  ctx.ratioChecked.add(key);
  const rows = rowsOfGroup(ctx.items, key);
  const vals = [];
  for (const row of rows) {
    const r = normRatio(row, ctx.items);
    if (r !== null) vals.push(r);
  }
  if (!vals.length) return [];
  const pct = vals.reduce((a, b) => a + b, 0) * 100;
  if (Math.abs(pct - 100) <= PCT_SCALE_TOL) return [];
  return [{
    line: lineOf(it), level: 'P1', category: '分摊比例合计不等于100%',
    message: `${it.period} · ${it.feeItem}：${vals.length} 户分摊比例合计 ${pct.toFixed(2)}%，与 100% 差 ${(pct - 100).toFixed(2)} 个百分点`,
    expected: 100, actual: round2(pct),
  }];
}

/** 5. 关键字段空缺 / 占位符 / 负值 */
function checkMissing(it) {
  const out = [];
  for (const role of KEY_ROLES) {
    if (isBlank(it[role])) {
      const v = it[role] === undefined || it[role] === null ? '' : String(it[role]).trim();
      out.push({
        line: lineOf(it), level: 'P1', category: '重复房号、空缺列与占位符',
        message: `${itemText(it) || '该行'}：「${LABELS[role] || role}」为空或是占位符（${v || '空白'}），这一格无法参与核对`,
      });
    }
  }
  for (const role of NEGATIVE_ROLES) {
    const n = normNumber(it[role]);
    if (n !== null && n < 0) {
      out.push({
        line: lineOf(it), level: 'P0', category: '金额或数量为负',
        message: `${itemText(it)}：「${LABELS[role] || role}」为负（${money(n)}），分摊表里该列不应为负`,
      });
    }
  }
  return out;
}

/** 6. 重复房号 / 重复分摊行 */
function checkDuplicate(it, ctx) {
  const k = groupKey(it) + '\u0000' + bldKey(it);
  const firstLine = ctx.dupSeen.get(k);
  if (firstLine !== undefined && firstLine !== lineOf(it)) {
    return [{
      line: lineOf(it), level: 'P0', category: '重复房号、空缺列与占位符',
      message: `${itemText(it)} 出现两次（本次第 ${it.line} 行，上一次第 ${firstLine} 行）：同一期间 + 同一费用项目下同一楼栋只能有一行`,
      first: firstLine,
    }];
  }
  return [];
}

/** 7. 分摊额超过公共总费用（逐行上限） */
function checkOverShared(it) {
  const a = normNumber(it.apportioned);
  const st = normNumber(it.sharedTotal);
  if (a === null || st === null || st === 0) return [];
  if (a - st <= TOL_OVER) return [];
  return [{
    line: lineOf(it), level: 'P0', category: '分摊额超过公共总费用',
    message: `${itemText(it)}：该户分摊额 ${money(a)} 已经超过这一期这一项的公共总费用 ${money(st)}（超 ${money(a - st)}）`,
    expected: round2(st), actual: round2(a),
  }];
}

function run(payload) {
  const p = (payload && typeof payload === 'object' && !Array.isArray(payload)) ? payload : null;
  if (!p) {
    return insufficient(['入参不是对象（应为 {"text": "…"}）'],
      '请用 {"text": "…"} 传材料：把公共能耗抄表与分摊明细表的表头和若干行一起复制进来，Tab 分隔最稳。');
  }
  const raw = p.text === undefined || p.text === null ? '' : String(p.text);
  if (raw.trim().length < 8) {
    return insufficient(['材料为空或只有几个字符'],
      '请把公共能耗抄表与分摊明细表（含表头）贴进来：可用 {"text": "…"}，或先跑 --sample 看看需要什么格式。');
  }
  const table = parseTable(raw);
  if (table.missingColumns.length) return insufficient(table.missingColumns);
  if (!table.items.length) {
    return insufficient(['只有表头，没有可核对的明细行'],
      '请把至少一行明细（期间 / 费用项目 / 楼栋 / 读数 / 基数 / 分摊额）一起贴进来。');
  }

  const ctx = { items: table.items, totals: table.totals, totalChecked: new Set(), ratioChecked: new Set(), dupSeen: new Map() };
  for (const it of table.items) {
    const k = groupKey(it) + '\u0000' + bldKey(it);
    if (!ctx.dupSeen.has(k)) ctx.dupSeen.set(k, lineOf(it));
  }

  const findings = [];
  for (const it of table.items) {
    findings.push(...checkReadingDiff(it));
    findings.push(...checkApportioned(it, ctx));
    findings.push(...checkMissing(it));
    findings.push(...checkDuplicate(it, ctx));
    findings.push(...checkOverShared(it));
  }
  for (const it of table.items) {
    findings.push(...checkGroupTotal(it, ctx));
    findings.push(...checkRatioSum(it, ctx));
  }

  const checks_executed = CHECKS_GIVEN.slice();
  const checks_not_run = [];
  const extra = {};
    for (const c of CHECKS_WITHHELD) checks_not_run.push(c);
  

  const rank = { P0: 0, P1: 1, P2: 2 };
  findings.sort((a, b) => (a.line - b.line) || (rank[a.level] - rank[b.level]));

  const counts = { P0: 0, P1: 0, P2: 0 };
  for (const f of findings) counts[f.level] = (counts[f.level] || 0) + 1;

  const shared = dedupSum(table.items, 'sharedTotal');
  const scope = {
    rows: table.items.length,
    buildings: new Set(table.items.map(bldKey)).size,
    periods: new Set(table.items.map((x) => String(x.period || ''))).size,
    groups: new Set(table.items.map(groupKey)).size,
    totals_row: !!table.totals.line,
    shared_total: round2(shared.reduce((a, x) => a + x.value, 0)),
    apportioned_total: sumOf(table.items, 'apportioned').sum,
    executed_locally: true,
    network_used: false,
    checks: checks_executed,
    checks_not_run: checks_not_run,
  };
  if (table.missingOptional && table.missingOptional.length) scope.optional_columns_absent = table.missingOptional;

  const result = Object.assign({
    scope: scope,
    findings: findings,
    summary: {
      rows: table.items.length,
      total: findings.length,
      p0: counts.P0 || 0,
      p1: counts.P1 || 0,
      p2: counts.P2 || 0,
      verdict: counts.P0 ? 'ERROR_FOUND' : (counts.P1 ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: checks_not_run.length,
      counts: counts,
    },
    note: '本工具只核这张表内部的算术与勾稽；核过的检查项见 scope.checks，未执行的见 scope.checks_not_run。',
  }, extra);
  return { status: 'success', result: result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
