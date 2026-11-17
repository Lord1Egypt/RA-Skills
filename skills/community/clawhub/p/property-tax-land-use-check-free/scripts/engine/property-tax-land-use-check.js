'use strict';
/**
 * property-tax-land-use-check.js —— 房产税与城镇土地使用税申报核对（免费档 / 完整档共用源码）
 *
 * 真实痛点：**有自有房产/土地的企业，每半年（多数省份）或每年申报前必须把这张表核一遍**：
 *   ① 从价计征：年应纳税额 = 房产原值 ×（1 − 扣除比例）× 1.2%
 *   ② 从租计征：年应纳税额 = 租金收入 × 12%
 *   ③ 城镇土地使用税：年应纳税额 = 土地面积 × 等级税额
 *   ④ 本期应纳 = 年应纳税额 ÷ 分期期数 − 减免税额，再与申报表、账面税金勾稽
 * 从价/从租混在一行算、土地等级税额用错、免租期没按从价口径补算，是最常见的多缴/少缴点。
 *
 * 与已有能力的区别：`vat-burden-check` 核的是增值税进销项与税负率；`invoice-consistency-check`
 * 核的是单张发票内部一致性；本能力核的是**房产税与城镇土地使用税的计税依据、分期与申报勾稽**，
 * 算式与口径都不一样（房产原值/余值/租金/土地面积/等级税额）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不查地方税额标准与减免政策文库、不调用大模型；
 * 材料不足不给结论（逐处算不出的行会进 not_concluded，绝不用 0 或默认值顶替）；不给税务意见、不做税收筹划。
 *
 * 分层实现：完整档追加的检查由入参开关控制的那个分支执行（函数只被该分支引用）；
 * 免费包由 tools/strip_free_engine.py 自动摘掉该分支与只被它引用的函数。
 * ⚠️ 本文件不要出现「完整档才执行的检查」那类区块标记：那种形态与开关并存时剥离脚本会误删免费检查。
 */

const CHECKS_GIVEN = [
  '房产余值复算（房产原值 ×（1 − 扣除比例））',
  '从价计征年应纳税额复算（房产余值 × 1.2%）',
  '从租计征年应纳税额复算（租金收入 × 12%）',
  '城镇土地使用税年应纳税额复算（土地面积 × 等级税额）',
  '分期缴纳的本期应纳复算（年应纳税额 ÷ 分期期数 − 减免税额）',
  '分期期数非正检测',
  '申报税额与本期应纳勾稽（差异定位：多申报/少申报多少）',
  '账面税金与本期应纳勾稽（账表差异）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复明细行检测（同一处房产/宗地列示两行）',
  '关键字段缺失或占位符检测（按计征方式判该填哪几格）',
  '计征方式无法识别检测',
];

const CHECKS_WITHHELD = [
  '计征方式与填报数据口径不符检测（从价行填了租金、从租行填了原值/土地面积、土地行填了房产原值）',
  '免租期未按规定从价计征检测（按从价口径补算免租期部分并给出差额）',
  '表内口径一致性检测（同一张表里从价房产的扣除比例、同一土地等级的等级税额是否一致）',
  '更正清单（逐处归因 + 更正金额 + 申报前处理清单，按金额排序）',
];

const OUT_OF_SCOPE = [
  '判断房产原值是否应当包含地价、是否应当包含附属设备与配套设施（以你提供的账面口径为准）',
  '判断本地适用的房产原值减除比例、土地等级税额标准、减免政策与免租期的特殊规定（本工具按你表里填的数复算）',
  '处理跨省多地块适用不同税额标准的分摊（请按宗地/等级分行列示）',
  '给出税务意见或做税收筹划；读取 .xlsx（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '房产名称/宗地\t计征方式\t房产原值\t扣除比例\t房产余值\t租金收入\t免租期月数\t土地面积\t土地等级\t等级税额\t年应纳税额\t分期期数\t本期应纳\t减免税额\t申报税额\t账面税金',
  '厂房A\t从价计征\t5000000.00\t30%\t3500000.00\t\t0\t\t\t\t42000.00\t2\t21000.00\t0.00\t21000.00\t21000.00',
  '商铺B\t从租计征\t\t\t\t600000.00\t0\t\t\t\t72000.00\t2\t36000.00\t0.00\t36000.00\t36000.00',
  '厂区土地C\t城镇土地使用税\t\t\t\t\t0\t10000.00\t二级\t12.00\t120000.00\t2\t60000.00\t0.00\t60000.00\t60000.00',
  '合计\t\t5000000.00\t\t3500000.00\t600000.00\t\t10000.00\t\t\t234000.00\t\t117000.00\t0.00\t117000.00\t117000.00',
].join('\n');

const TOL = 0.01;

// 税率与税额标准**不由本工具设定**：1.2%/12% 是房产税从价/从租的法定年税率（算式口径），
// 等级税额由你的表提供。本工具只做「按上面这个口径复算」与「表内勾稽」，不判定适用性。
const PRICE_RATE_PCT = 1.2;
const RENT_RATE_PCT = 12;

const MODE_LABELS = { price: '从价计征', rent: '从租计征', land: '城镇土地使用税' };

// ⚠️ 更具体的关键词必须排在更宽泛的前面（本仓库踩过两次的坑，见 tools/header_map_check.py）：
//    「等级税额」必须排在「土地等级」之前，否则「等级税额」会被「等级」抢走；
//    「免租期月数」不能被「租金」抢走；「房产余值」不能被「房产原值」抢走。
const ROLES = {
  item: ['房产名称', '房屋名称', '宗地名称', '土地名称', '明细项目', '项目名称', '房产/宗地', '名称'],
  mode: ['计征方式', '计征', '计税方式', '征收方式'],
  original: ['房产原值', '房屋原值', '原值'],
  deduct: ['扣除比例', '减除比例', '扣除率', '扣除'],
  residual: ['房产余值', '房屋余值', '计税余值', '余值'],
  freeMonths: ['免租期月数', '免租月数', '免租期'],
  rent: ['租金收入', '租赁收入', '租金'],
  area: ['土地面积', '占地面积', '面积'],
  unitTax: ['等级税额', '单位税额', '土地等级税额', '税额标准'],
  landLevel: ['土地等级', '地段等级', '土地级别', '等级'],
  annual: ['年应纳税额', '年应纳', '年应缴'],
  instN: ['分期期数', '缴纳期数', '期数'],
  periodTax: ['本期应纳', '本期应缴', '本期税额'],
  reduction: ['减免税额', '减免', '减征'],
  declared: ['申报税额', '申报表税额', '申报数', '本期申报税额'],
  bookTax: ['账面税金', '账面税额', '账载税金', '账面'],
};

const LABELS = {
  item: '房产名称/宗地', mode: '计征方式', original: '房产原值', deduct: '扣除比例',
  residual: '房产余值', freeMonths: '免租期月数', rent: '租金收入', area: '土地面积',
  unitTax: '等级税额', landLevel: '土地等级', annual: '年应纳税额', instN: '分期期数',
  periodTax: '本期应纳', reduction: '减免税额', declared: '申报税额', bookTax: '账面税金',
};

const REQUIRED = ['item', 'mode', 'original', 'deduct', 'residual', 'freeMonths', 'rent', 'area',
  'unitTax', 'landLevel', 'annual', 'instN', 'periodTax', 'reduction', 'declared', 'bookTax'];

const SUM_ROLES = ['original', 'residual', 'rent', 'area', 'annual', 'periodTax', 'reduction', 'declared', 'bookTax'];

// 每种计征方式「该填哪几格」——缺了就算不出这处的税额（按行判，不按整表判）
const COMMON_REQUIRED = ['annual', 'instN', 'periodTax', 'declared', 'bookTax', 'reduction'];
const MODE_REQUIRED = {
  price: ['original', 'deduct', 'residual'],
  rent: ['rent', 'freeMonths'],
  land: ['area', 'unitTax'],
};

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|不适用)$/i.test(s);
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
const fmt = (n) => Number(n).toFixed(2);
const fill = (v) => String(v === undefined || v === null ? '' : v).trim();

function parseTable(text) {
  const raw = String(text).split(/\r?\n/).filter((l) => l.trim() !== '');
  if (!raw.length) return { error: 'empty' };
  const cols = splitRow(raw[0]).map((h) => ({ header: h, role: roleOf(h) }));
  const have = new Set(cols.map((c) => c.role).filter(Boolean));
  const missingRoles = REQUIRED.filter((r) => !have.has(r));
  if (missingRoles.length) {
    return { error: 'no_header', missingRoles: missingRoles.map((r) => LABELS[r]) };
  }
  const items = [];
  const totals = [];
  for (let i = 1; i < raw.length; i++) {
    const cells = splitRow(raw[i]);
    const row = { line: i + 1, raw: raw[i], byRole: {} };
    cols.forEach((c, idx) => {
      if (c.role && row.byRole[c.role] === undefined) {
        row.byRole[c.role] = cells[idx] === undefined ? '' : cells[idx];
      }
    });
    const first = String(cells[0] || '').trim();
    if (/^(合计|总计|小计|total)/i.test(first)) {
      row.isTotal = true;
      totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

const num = (it, role) => normNumber(it.byRole[role]);
const labelOf = (it) => fill(it.byRole && it.byRole.item) || '(未命名)';
const who = (it) => `第 ${it.line} 行「${labelOf(it)}」`;

/** 计征方式归一：只认表里写的字，不猜 */
function modeOf(it) {
  const s = fill(it.byRole && it.byRole.mode).replace(/[\s（）()]/g, '');
  if (!s) return null;
  if (s.indexOf('从价') >= 0) return 'price';
  if (s.indexOf('从租') >= 0) return 'rent';
  if (s.indexOf('土地') >= 0 || s.indexOf('面积') >= 0) return 'land';
  return 'unknown';
}

/* ===== 免费档：逐处房产/宗地复算 + 合计与申报表勾稽 + 差异定位 ===== */

/** ① 房产余值 = 房产原值 ×（1 − 扣除比例） */
function checkResidual(it) {
  const mode = modeOf(it);
  if (mode !== 'price' && mode !== 'rent') return null;
  const original = num(it, 'original');
  const deduct = num(it, 'deduct');
  const stated = num(it, 'residual');
  if (original === null || deduct === null || stated === null) return null;
  const expect = round2(original * (1 - deduct / 100));
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '房产余值与复算不符', line: it.line,
    stated, expected: expect,
    message: `${who(it)}的房产余值是 ${fmt(stated)}，`
      + `按 房产原值 ${fmt(original)} ×（1 − 扣除比例 ${deduct}%）应为 ${fmt(expect)}，`
      + `差额 ${fmt(round2(stated - expect))}。`,
    advice: '房产余值是计税依据：这一格错了，从价这条链（余值→年应纳税额→本期应纳→申报税额）会一路跟着错。',
  };
}

/** ② 从价计征：年应纳税额 = 房产余值 × 1.2% */
function checkAnnualPrice(it) {
  if (modeOf(it) !== 'price') return null;
  const base = num(it, 'residual');
  const stated = num(it, 'annual');
  if (base === null || stated === null) return null;
  const expect = round2(base * PRICE_RATE_PCT / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '从价计征年应纳税额与复算不符', line: it.line,
    stated, expected: expect,
    message: `${who(it)}的年应纳税额是 ${fmt(stated)}，`
      + `按 房产余值 ${fmt(base)} × 1.2% 应为 ${fmt(expect)}，差额 ${fmt(round2(stated - expect))}。`,
    advice: '从价计征的计税依据是房产余值（不是原值、也不是租金）：先看余值列，再看年税额。',
  };
}

/** ③ 从租计征：年应纳税额 = 租金收入 × 12%（填了免租期的行不在本档断言，见 checks_not_run） */
function checkAnnualRent(it) {
  if (modeOf(it) !== 'rent') return null;
  const freeM = num(it, 'freeMonths');
  if (freeM !== null && freeM > 0) return null;
  const base = num(it, 'rent');
  const stated = num(it, 'annual');
  if (base === null || stated === null) return null;
  const expect = round2(base * RENT_RATE_PCT / 100);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '从租计征年应纳税额与复算不符', line: it.line,
    stated, expected: expect,
    message: `${who(it)}的年应纳税额是 ${fmt(stated)}，`
      + `按 租金收入 ${fmt(base)} × 12% 应为 ${fmt(expect)}，差额 ${fmt(round2(stated - expect))}。`,
    advice: '从租计征只看租金收入（不是房产余值）：把租金填进「房产原值」再乘 1.2% 就会两条口径都不成立。',
  };
}

/** ④ 城镇土地使用税：年应纳税额 = 土地面积 × 等级税额 */
function checkAnnualLand(it) {
  if (modeOf(it) !== 'land') return null;
  const area = num(it, 'area');
  const unit = num(it, 'unitTax');
  const stated = num(it, 'annual');
  if (area === null || unit === null || stated === null) return null;
  const expect = round2(area * unit);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '城镇土地使用税年应纳税额与复算不符', line: it.line,
    stated, expected: expect,
    message: `${who(it)}的年应纳税额是 ${fmt(stated)}，`
      + `按 土地面积 ${fmt(area)} 平方米 × 等级税额 ${fmt(unit)} 元/平方米 应为 ${fmt(expect)}，`
      + `差额 ${fmt(round2(stated - expect))}。`,
    advice: '计税依据是土地（宗地）面积与本地土地等级税额；拿建筑面积来乘就会差出整片。',
  };
}

/** ⑤ 本期应纳 = 年应纳税额 ÷ 分期期数 − 减免税额 */
function checkPeriodTax(it) {
  const annual = num(it, 'annual');
  const n = num(it, 'instN');
  const reduction = num(it, 'reduction');
  const stated = num(it, 'periodTax');
  if (annual === null || n === null || reduction === null || stated === null) return null;
  if (n <= 0) return null;                       // 期数非正由 checkInstN 单独报
  const expect = round2(annual / n - reduction);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '本期应纳与复算不符', line: it.line,
    stated, expected: expect,
    message: `${who(it)}的本期应纳是 ${fmt(stated)}，`
      + `按 年应纳税额 ${fmt(annual)} ÷ 分期期数 ${n} − 减免税额 ${fmt(reduction)} 应为 ${fmt(expect)}，`
      + `差额 ${fmt(round2(stated - expect))}。`,
    advice: '分期缴纳（多数省份按半年申报）时本期应纳是年额除以期数再减本期减免；把年额直接填进来会整期多缴。',
  };
}

/** ⑥ 分期期数必须为正 */
function checkInstN(it) {
  const n = num(it, 'instN');
  if (n === null || n > 0) return null;
  return {
    level: 'P0', category: '分期期数非正', line: it.line, stated: n, expected: 1,
    message: `${who(it)}的分期期数是 ${n}。`,
    advice: '本期应纳 = 年应纳税额 ÷ 分期期数 − 减免税额，期数必须为正整数（半年申报一般填 2）。',
  };
}

/** ⑦ 申报税额 = 本期应纳（差异定位：多申报/少申报多少） */
function checkDeclared(it) {
  const declared = num(it, 'declared');
  const expect = num(it, 'periodTax');
  if (declared === null || expect === null) return null;
  const diff = round2(declared - expect);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P0', category: '申报税额与本期应纳不符', line: it.line,
    stated: declared, expected: expect,
    message: `${who(it)}的申报税额是 ${fmt(declared)}，本期应纳是 ${fmt(expect)}，`
      + `相差 ${fmt(diff)}（${diff > 0 ? '多申报' : '少申报'} ${fmt(Math.abs(diff))}）。`,
    advice: '这两个数只能有一个对：先核本期应纳那条复算链（年额÷期数−减免），再决定改申报表还是改底稿。',
  };
}

/** ⑧ 账面税金 = 本期应纳（账表差异） */
function checkBookTax(it) {
  const book = num(it, 'bookTax');
  const expect = num(it, 'periodTax');
  if (book === null || expect === null) return null;
  const diff = round2(book - expect);
  if (Math.abs(diff) <= TOL) return null;
  return {
    level: 'P1', category: '账面税金与本期应纳不符', line: it.line,
    stated: book, expected: expect,
    message: `${who(it)}的账面税金是 ${fmt(book)}，本期应纳是 ${fmt(expect)}，`
      + `相差 ${fmt(diff)}（账面${diff > 0 ? '多' : '少'} ${fmt(Math.abs(diff))}）。`,
    advice: '账表差异既可能是计提期间串了（本期提上期的税），也可能是其中一边算错；先定期间口径再定金额。',
  };
}

/** ⑨ 计征方式认不出来 */
function checkModeKnown(it) {
  const raw = fill(it.byRole && it.byRole.mode);
  if (raw === '') return null;                   // 空白由「关键字段缺失」报
  if (modeOf(it) !== 'unknown') return null;
  return {
    level: 'P0', category: '计征方式无法识别', line: it.line,
    message: `${who(it)}的计征方式填的是「${raw}」——认不出是从价计征、从租计征还是城镇土地使用税。`,
    advice: '计征方式决定用哪条算式（余值×1.2%／租金×12%／面积×等级税额）；写清一种，本工具才能复算。',
  };
}

/** ⑩ 合计行逐列复核 */
function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = num(t, role);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = num(it, role);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        stated, expected: sum,
        message: `合计行的「${LABELS[role]}」是 ${fmt(stated)}，各明细行相加是 ${fmt(sum)}，`
          + `相差 ${fmt(round2(stated - sum))}。`,
        advice: '要么明细行漏了一处房产/宗地，要么明细改了合计行没跟着更新；先看这一列有没有重复列示。',
      });
    }
  }
  return out;
}

/** ⑪ 同一处房产/宗地重复列示 */
function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = labelOf(it).replace(/\s/g, '');
    if (!key || key === '(未命名)') continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一房产或宗地重复列示', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一处房产按从价、从租分行列示是正常的（口径不同），但那样两行的名称要能区分；'
          + '若确实重复，年应纳税额与合计都会翻倍。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a|无|不适用)$/i;

/** ⑫ 按计征方式判「该填哪几格」是否缺失 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    const need = ['item', 'mode'].concat(COMMON_REQUIRED).concat(MODE_REQUIRED[modeOf(it)] || []);
    for (const role of need) {
      const raw = fill(it.byRole[role]);
      if (raw === '' || PLACEHOLDER.test(raw)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${raw || '空'}）。`,
          advice: '缺这一格这处的税额就算不出来；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

/* ===== 完整档追加的检查：归因 + 更正金额 + 申报前处理清单（免费档只有说明，没有实现） ===== */

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的房产税与城镇土地使用税申报核对表（要能认出「房产名称/宗地」「计征方式」「房产原值」'
      + '「扣除比例」「房产余值」「租金收入」「免租期月数」「土地面积」「等级税额」「年应纳税额」'
      + '「分期期数」「本期应纳」「减免税额」「申报税额」「账面税金」）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从申报底稿或台账导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一处房产/宗地的明细行']);

  const findings = [];
  const notRun = [];
  const notConcluded = [];
  let remedy = null;

  for (const it of t.items) {
    for (const fn of [checkResidual, checkAnnualPrice, checkAnnualRent, checkAnnualLand,
      checkPeriodTax, checkInstN, checkDeclared, checkBookTax, checkModeKnown]) {
      const f = fn(it);
      if (f) findings.push(f);
    }
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
    for (const it of t.items) {
      if (modeOf(it) !== 'rent') continue;
      const freeM = num(it, 'freeMonths');
      if (freeM !== null && freeM > 0) {
        notConcluded.push({
          line: it.line, item: labelOf(it),
          reason: `本行填了免租期 ${freeM} 个月：年应纳税额里含免租期的从价口径，`
            + '本档不对它下断言（见 checks_not_run）。',
        });
      }
    }
  

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = num(it, role);
    return s + (n === null ? 0 : n);
  }, 0));

  const modes = { price: 0, rent: 0, land: 0, unknown: 0 };
  for (const it of t.items) {
    const m = modeOf(it);
    if (m && m !== null) modes[m] = (modes[m] || 0) + 1;
  }
  const declaredTotal = sumOf('declared');
  const periodTotal = sumOf('periodTax');
  const bookTotal = sumOf('bookTax');

  const result = {
    findings,
    summary: {
      rows: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      p2: findings.filter((f) => f.level === 'P2').length,
      modes: { 从价计征: modes.price, 从租计征: modes.rent, 城镇土地使用税: modes.land, 未识别: modes.unknown },
      annual_total: sumOf('annual'),
      period_total: periodTotal,
      reduction_total: sumOf('reduction'),
      declared_total: declaredTotal,
      book_total: bookTotal,
      declared_diff: round2(declaredTotal - periodTotal),
      book_diff: round2(bookTotal - periodTotal),
      basis: '房产余值 = 房产原值 ×（1 − 扣除比例）；从价计征年应纳税额 = 房产余值 × 1.2%；'
        + '从租计征年应纳税额 = 租金收入 × 12%；城镇土地使用税年应纳税额 = 土地面积 × 等级税额；'
        + '本期应纳 = 年应纳税额 ÷ 分期期数 − 减免税额；申报税额、账面税金分别与本期应纳勾稽；合计行逐列复核。',
    },
    columns: t.cols.map((c) => c.header),
    scope: {
      rows: t.items.length,
      checks_given: CHECKS_GIVEN.length,
      checks_withheld: CHECKS_WITHHELD.length,
      checks_not_run: CHECKS_WITHHELD,
      paid_only_checks_run: 0,
      not_concluded_lines: notConcluded.map((x) => x.line),
    },
    not_concluded: notConcluded,
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (remedy) result.remedy = remedy;
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的算式口径算得对、'
      + '表内与申报表/账面互相勾稽得上**，不代表房产原值口径、减除比例、土地等级税额与减免政策的适用性没问题 —— '
      + '那些不在本工具范围内（见 checks_out_of_scope）。';
  }
  if (notConcluded.length) {
    result.note_not_concluded = '有 ' + notConcluded.length + ' 行本次没有下结论（材料或口径不够），'
      + '它们既不算通过也不算不通过 —— 明细见 not_concluded。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, modeOf, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, ROLES, REQUIRED, SUM_ROLES, MODE_LABELS,
};
