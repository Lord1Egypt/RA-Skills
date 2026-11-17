/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * logistics-fuel-card-check.js —— 车队油卡与油耗核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**物流公司 / 车队的车辆管理员与财务，在每月油卡充值与油耗结算时**。
 * 这张「油卡充值与油耗明细表」每一格都能手算复现，而每月都要吵的就是这几处：
 *   · 卡余额对不上：有一笔充值或扣款没落在这张表上；
 *   · 百公里油耗填错，或者加油站按升扣款、表里按金额填，两边差一截；
 *   · 同一台车同一天被记了两次加油（重复贴行 / 一车两卡）；
 *   · 里程表读数倒着走（换表、抄错、跨月抄表）；
 *   · 报了油耗却漏填行驶里程，油耗复算不出来。
 *
 * 表内勾稽（每一步都能被第三方用同一份输入复算）：
 *   期末余额   = 期初余额 + 充值金额 − 油卡扣款金额
 *   百公里油耗 = 加油量 ÷ 行驶里程 × 100
 *   油卡扣款金额 = 加油量 × 加油单价
 *   行驶里程   = 里程表读数 − 上期读数
 *   合计行各列 = 各明细行逐列相加（充值金额 / 加油量 / 油卡扣款金额 / 行驶里程）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，不读环境变量、不写盘，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 3 项（见 CHECKS_WITHHELD），其中最重要的是免费档**结构上做不到**的
 * 「跨车 / 跨车队汇总台账 + 按超额金额排序的油耗异常处理清单 + 油耗异常归因」。
 *
 * ⚠️ 本工具**不判断**加油量 / 加油单价是否与油站小票一致、里程表读数是否与 GPS 一致、
 *    参考上限该定多少（那属于油卡流水、车载终端与运价 / 油耗标准的核定）：
 *    表中的加油量、单价、扣款、余额、里程、路况、载重、用车性质一律**以你填的为准**。
 *
 * ⚠️ 付费项只声明**一次**档位开关常量（布尔），付费检查统一包在以该常量为条件的语句块里；
 *    ⛔ 注释里**不要**写出那一行的字面量，也不要在别处再声明一次：
 *    `strip_free_engine` 的残渣断言是**纯字符串包含**判断，写了就会被判「没删干净」而整包跳过。
 *    ⛔ 也不要在付费实现之外另立「完整档才执行的检查」那类 MARKER —— 本文件只有一处 MARKER，
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉（第 236 轮踩过）。
 */

const CHECKS_GIVEN = [
  '卡余额勾稽复算（期初余额 + 充值金额 − 油卡扣款金额 = 期末余额）与合计行逐列复核',
  '公里油耗复算（加油量 ÷ 行驶里程 × 100 = 百公里油耗）',
  '油耗高于参考上限检测（按行驶里程折算超额油量与超额金额）',
  '同一车同一日期重复加油检测',
  '加油量与油卡扣款一致性检测（加油量 × 加油单价 = 油卡扣款金额）',
  '里程回退、空缺与读数不符检测（里程表读数 − 上期读数 = 行驶里程）',
];

const CHECKS_WITHHELD = [
  '跨车 / 跨车队汇总台账（按车队 × 期间汇总充值金额、加油量、油卡扣款、行驶里程、平均油耗与超额金额）',
  '按超额金额排序的油耗异常处理清单（逐条带原文行号、车牌号与建议，金额从大到小）',
  '油耗异常归因（按路况 / 载重 / 用车性质分组，区分私车公用与非公务用车）',
];

const OUT_OF_SCOPE = [
  '判断加油量、加油单价、油卡扣款金额是否与油站小票 / 油卡系统流水一致（本工具只核表内算术，以你填的为准）',
  '判断里程表读数是否与 GPS / 车载终端 / 派车单一致（本工具只核表内读数之间的勾稽）',
  '判断「参考上限」该定多少（以你按车型 / 线路填的参考上限为准，本工具不替你定标准）',
  '判断路况 / 载重 / 用车性质三列填得对不对（本工具只按这三列分组归因，不去现场核实）',
  '计算油耗对应的个税 / 增值税进项转出 / 企业所得税扣除，或判断私车公用该不该补贴',
  '读取 Excel / 油卡系统 / TMS 导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '期间\t车队\t车牌号\t油卡号\t业务日期\t业务类型\t充值金额\t加油量(升)\t加油单价\t油卡扣款金额\t期初余额\t期末余额\t里程表读数\t上期读数\t行驶里程\t百公里油耗\t参考上限\t路况\t载重\t用车性质',
  '2026-01\t华东车队\t沪A12345\tYK1001\t2026-01-02\t充值\t5000.00\t0\t0.00\t0.00\t1200.00\t6200.00\t0\t0\t0\t0.00\t32.00\t市区\t满载\t公务',
  '2026-01\t华东车队\t沪A12345\tYK1001\t2026-01-10\t加油\t0.00\t400\t7.50\t3000.00\t6200.00\t3200.00\t42000\t38000\t4000\t10.00\t32.00\t高速\t满载\t公务',
  '2026-01\t华东车队\t沪B23456\tYK1002\t2026-01-03\t充值\t4000.00\t0\t0.00\t0.00\t800.00\t4800.00\t0\t0\t0\t0.00\t30.00\t市区\t空载\t公务',
  '2026-01\t华东车队\t沪B23456\tYK1002\t2026-01-18\t加油\t0.00\t300\t7.50\t2250.00\t4800.00\t2550.00\t62500\t60000\t2500\t12.00\t30.00\t市区\t空载\t公务',
  '2026-02\t华南车队\t粤C34567\tYK2001\t2026-02-05\t充值\t6000.00\t0\t0.00\t0.00\t1500.00\t7500.00\t0\t0\t0\t0.00\t34.00\t高速\t满载\t公务',
  '2026-02\t华南车队\t粤C34567\tYK2001\t2026-02-20\t加油\t0.00\t500\t7.80\t3900.00\t7500.00\t3600.00\t91000\t86000\t5000\t10.00\t34.00\t高速\t满载\t公务',
  '合计\t\t\t\t\t\t15000.00\t1200\t\t9150.00\t\t\t\t\t11500\t\t\t\t\t',
].join('\n');

const TOL = 0.01;

const LABELS = {
  period: '期间', fleet: '车队', plate: '车牌号', cardNo: '油卡号', date: '业务日期',
  bizType: '业务类型', recharge: '充值金额', liters: '加油量(升)', unitPrice: '加油单价',
  cardAmount: '油卡扣款金额', openBalance: '期初余额', closeBalance: '期末余额',
  odometer: '里程表读数', prevOdometer: '上期读数', km: '行驶里程', consumption: '百公里油耗',
  refCap: '参考上限', road: '路况', load: '载重', usage: '用车性质',
};

/* 合计行按这些角色逐列相加（数量列也一起加，单位由列名自己说明） */
const SUM_ROLES = ['recharge', 'liters', 'cardAmount', 'km'];

/* ⚠️ 顺序即优先级：更具体的别名在前，兜底的宽泛别名在后。
 *    「里程表读数」必须排在「行驶里程」前面（否则被 km 的「里程」抢走）；
 *    「上期读数」必须排在「里程表读数」前面（读数 vs 里程读数）；
 *    「油卡号」必须排在「油卡扣款金额」前面（卡号 vs 卡）。 */
const ROLES = [
  ['period', ['结算期间', '所属期间', '费用期间', '所属月份', '账期', '期间', '月份', '月度']],
  ['fleet', ['车队名称', '所属车队', '车队']],
  ['plate', ['车牌号码', '车牌号', '车牌', '车号']],
  ['cardNo', ['油卡卡号', '油卡号', '卡号']],
  ['date', ['业务日期', '加油日期', '交易日期', '日期']],
  ['usage', ['用车性质', '用车类型', '车辆用途', '用车']],
  ['bizType', ['业务类型', '业务种类', '业务']],
  ['recharge', ['本期充值金额', '充值金额', '本期充值', '充值']],
  ['liters', ['加油量', '加油升数', '加注量', '升数']],
  ['unitPrice', ['加油单价', '结算单价', '单价']],
  ['cardAmount', ['油卡扣款金额', '油卡扣款', '扣款金额', '加油金额', '扣款']],
  ['openBalance', ['期初余额', '上期余额', '期初卡余额', '期初']],
  ['closeBalance', ['期末余额', '本期余额', '期末卡余额', '期末']],
  ['prevOdometer', ['上期读数', '期初读数', '上次读数']],
  ['odometer', ['里程表读数', '本期读数', '期末读数', '里程读数', '里程表']],
  ['km', ['本期行驶里程', '行驶里程', '行驶公里', '里程']],
  ['consumption', ['百公里油耗', '百公里耗油', '油耗']],
  ['refCap', ['参考上限', '油耗上限', '参考标准', '上限']],
  ['road', ['行驶路况', '路况']],
  ['load', ['载重情况', '载重']],
];

const NUMERIC_ROLES = ['recharge', 'liters', 'unitPrice', 'cardAmount', 'openBalance',
  'closeBalance', 'odometer', 'prevOdometer', 'km', 'consumption', 'refCap'];

const REQUIRED = ROLES.map((r) => r[0]);

const LEVEL_ORDER = { P0: 0, P1: 1, P2: 2 };

const normHeader = (h) => String(h === undefined || h === null ? '' : h)
  .replace(/[\s\u3000]/g, '')
  .replace(/[（(][^）)]*[）)]/g, '')
  .replace(/[：:]/g, '')
  .toLowerCase();

/** 表头 → 角色；认不出返回 null（认不出的列会**静默地不参与任何检查**，所以顺序很要紧） */
function roleOf(header) {
  const h = normHeader(header);
  if (h === '') return null;
  for (let i = 0; i < ROLES.length; i++) {
    const role = ROLES[i][0];
    const aliases = ROLES[i][1];
    for (let j = 0; j < aliases.length; j++) {
      if (h.indexOf(aliases[j]) >= 0) return role;
    }
  }
  return null;
}

function normNumber(raw) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim().replace(/[¥￥,，\s]/g, '');
  if (s === '' || /^[-—–]+$/.test(s)) return null;
  const neg = /^\(.*\)$/.test(s);
  const t = s.replace(/[()]/g, '');
  if (!/^-?\d+(\.\d+)?%?$/.test(t)) return null;
  const n = Number(t.replace('%', ''));
  if (!Number.isFinite(n)) return null;
  return neg ? -n : n;
}
const round2 = (n) => Math.round(n * 100) / 100;

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|不详)$/i.test(s);
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((x) => x.trim());
  return line.split(/\s{2,}/).map((x) => x.trim());
}

/** 解析：返回 { items, totals, missingColumns, header, headerRoles }；items 每条带原文行号 */
function parseTable(text) {
  const raw = String(text === undefined || text === null ? '' : text).replace(/\r\n?/g, '\n');
  const lines = raw.split('\n');
  let header = [];
  let headerLine = 0;
  const headerRoles = [];
  for (let i = 0; i < lines.length; i++) {
    if (isBlank(lines[i])) continue;
    header = splitRow(lines[i]);
    headerLine = i + 1;
    for (let c = 0; c < header.length; c++) headerRoles.push(roleOf(header[c]));
    break;
  }

  const colOf = {};
  for (let c = 0; c < header.length; c++) {
    const role = headerRoles[c];
    if (role && colOf[role] === undefined) colOf[role] = c;
  }

  const items = [];
  const totals = { line: 0, rows: 0, row: {}, sum: {} };
  for (let i = headerLine; i < lines.length; i++) {
    const line = lines[i];
    if (isBlank(line)) continue;
    const cells = splitRow(line);
    const first = String(cells[0] === undefined ? '' : cells[0]).trim();
    const isTotal = /^(合计|总计|小计|合 计|总 计)/.test(first);
    const rec = { line: i + 1, raw: {} };
    for (let r = 0; r < REQUIRED.length; r++) {
      const role = REQUIRED[r];
      const idx = colOf[role];
      const cell = idx === undefined || idx >= cells.length ? '' : cells[idx];
      rec.raw[role] = cell;
      if (NUMERIC_ROLES.indexOf(role) >= 0) {
        rec[role] = normNumber(cell);
      } else {
        rec[role] = String(cell === undefined || cell === null ? '' : cell).trim();
      }
    }
    if (isTotal) {
      totals.line = i + 1;
      totals.rows += 1;
      if (totals.rows === 1) totals.row = rec;
    } else {
      items.push(rec);
    }
  }

  for (let r = 0; r < SUM_ROLES.length; r++) {
    const role = SUM_ROLES[r];
    let s = 0;
    for (let i = 0; i < items.length; i++) s += (items[i][role] === null ? 0 : items[i][role]);
    totals.sum[role] = round2(s);
  }

  const missingColumns = [];
  for (let r = 0; r < REQUIRED.length; r++) {
    if (colOf[REQUIRED[r]] === undefined) missingColumns.push(LABELS[REQUIRED[r]]);
  }

  return {
    error: null,
    header: header,
    headerRoles: headerRoles,
    items: items,
    totals: totals,
    missingColumns: missingColumns,
    missingRoles: missingColumns,
  };
}

const fmt = (n) => (typeof n === 'number' && Number.isFinite(n) ? round2(n).toFixed(2) : '（空）');

function who(it) {
  const bits = [];
  if (it.plate) bits.push('车牌「' + it.plate + '」');
  if (it.cardNo) bits.push('油卡 ' + it.cardNo);
  if (it.date) bits.push(String(it.date));
  if (it.bizType) bits.push(String(it.bizType));
  return bits.length ? bits.join(' ') : '第 ' + it.line + ' 行';
}

/** 超标口径（免费档与完整档共用同一份算术，避免两档算出两个数） */
function excessOf(it) {
  const cons = it.consumption;
  const cap = it.refCap;
  if (cons === null || cap === null) return null;
  if (it.liters === null || it.liters <= 0) return null;
  if (cons <= cap + TOL) return null;
  const km = it.km === null ? 0 : it.km;
  const price = it.unitPrice === null ? 0 : it.unitPrice;
  const excessLiters = round2((cons - cap) / 100 * km);
  return { excess_liters: excessLiters, excess_amount: round2(excessLiters * price) };
}

function insufficient(missing, advice) {
  return {
    status: 'insufficient_input',
    missing: missing,
    advice: advice || '请把油卡充值与油耗明细表（含表头）贴进来：可用 {"text": "…"}，'
      + '或先用 --sample 看看需要什么格式。缺列或认不出表头时，本工具不做任何认定 —— '
      + '既不说「对」，也不说「错」，更不会拿 0 替你假设「这笔没有充值 / 没有扣款」。',
  };
}

/* ========================== 免费档检查（两档都执行） ========================== */

function checkBalance(it) {
  const open = it.openBalance;
  const rec = it.recharge;
  const pay = it.cardAmount;
  const close = it.closeBalance;
  if (open === null || rec === null || pay === null || close === null) {
    const miss = [];
    if (open === null) miss.push('期初余额');
    if (rec === null) miss.push('充值金额');
    if (pay === null) miss.push('油卡扣款金额');
    if (close === null) miss.push('期末余额');
    return {
      line: it.line, level: 'P0', category: '卡余额勾稽缺格', amount: 0,
      message: who(it) + ' 的「' + miss.join(' / ') + '」为空或不是数字，这一行的卡余额勾稽算不出来。',
      evidence: '期初余额=' + it.raw.openBalance + '；充值金额=' + it.raw.recharge
        + '；油卡扣款金额=' + it.raw.cardAmount + '；期末余额=' + it.raw.closeBalance,
      advice: '留空表示「不知道」，本工具不用 0 替你假设；请把这四格补齐再跑一次。',
    };
  }
  const expect = round2(open + rec - pay);
  const diff = round2(close - expect);
  if (Math.abs(diff) <= TOL) return null;
  return {
    line: it.line, level: 'P0', category: '卡余额勾稽不符', amount: Math.abs(diff),
    message: who(it) + ' 期初 ' + fmt(open) + ' + 充值 ' + fmt(rec) + ' − 加油扣款 ' + fmt(pay)
      + ' = ' + fmt(expect) + '，表里期末余额填的是 ' + fmt(close) + '，相差 ' + fmt(diff) + '。',
    evidence: '期末余额=' + it.raw.closeBalance + '；应有余额=' + fmt(expect) + '；差额=' + fmt(diff),
    advice: '卡余额勾稽是这张表最基本的一条：对不上就是有一笔充值或扣款没落在这张表上，先追这笔差额。',
  };
}

function checkConsumption(it) {
  const liters = it.liters;
  const km = it.km;
  const cons = it.consumption;
  if (liters === null || liters <= 0) return null;
  if (cons === null) {
    return {
      line: it.line, level: 'P2', category: '油耗列空缺', amount: 0,
      message: who(it) + ' 有加油量 ' + fmt(liters) + ' 升，但「百公里油耗」这一格是空的。',
      evidence: '加油量=' + it.raw.liters + '；百公里油耗=' + it.raw.consumption,
      advice: '百公里油耗 = 加油量 ÷ 行驶里程 × 100；本工具不替你算一个填进去，请按同一口径补上。',
    };
  }
  if (km === null || km <= 0) return null;
  const expect = round2(liters / km * 100);
  const diff = round2(cons - expect);
  if (Math.abs(diff) <= TOL) return null;
  return {
    line: it.line, level: 'P0', category: '公里油耗复算不符', amount: 0,
    message: who(it) + ' 加油量 ' + fmt(liters) + ' 升 ÷ 行驶里程 ' + fmt(km) + ' 公里 × 100 = '
      + fmt(expect) + '，表里百公里油耗填的是 ' + fmt(cons) + '，相差 ' + fmt(diff) + ' 升/百公里。',
    evidence: '加油量=' + it.raw.liters + '；行驶里程=' + it.raw.km
      + '；百公里油耗=' + it.raw.consumption + '；应有油耗=' + fmt(expect),
    advice: '油耗口径先统一：是加满两次之间的里程，还是本期间行驶里程。口径混了，这一列整体都会偏。',
  };
}

function checkOverCap(it) {
  const ex = excessOf(it);
  if (!ex) return null;
  return {
    line: it.line, level: 'P1', category: '油耗高于参考上限', amount: ex.excess_amount,
    excess_liters: ex.excess_liters,
    message: who(it) + ' 百公里油耗 ' + fmt(it.consumption) + ' 高于参考上限 ' + fmt(it.refCap)
      + '（按行驶里程 ' + fmt(it.km) + ' 公里折算超额油量 ' + fmt(ex.excess_liters)
      + ' 升、超额金额 ' + fmt(ex.excess_amount) + ' 元）。',
    evidence: '百公里油耗=' + it.raw.consumption + '；参考上限=' + it.raw.refCap
      + '；行驶里程=' + it.raw.km + '；加油单价=' + it.raw.unitPrice,
    advice: '先确认这一行的路况 / 载重 / 用车性质填的是不是本期真实工况，再看超额金额要不要业务上解释。',
  };
}

function checkCardAmount(it) {
  const liters = it.liters;
  const price = it.unitPrice;
  const amount = it.cardAmount;
  if (liters === null || liters <= 0) return null;
  if (price === null || price <= 0) return null;
  if (amount === null) return null;
  const expect = round2(liters * price);
  const diff = round2(amount - expect);
  if (Math.abs(diff) <= TOL) return null;
  return {
    line: it.line, level: 'P0', category: '加油量与油卡扣款不一致', amount: Math.abs(diff),
    message: who(it) + ' 加油量 ' + fmt(liters) + ' 升 × 加油单价 ' + fmt(price) + ' = ' + fmt(expect)
      + '，但油卡扣款金额填的是 ' + fmt(amount) + '，相差 ' + fmt(diff) + ' 元。',
    evidence: '加油量=' + it.raw.liters + '；加油单价=' + it.raw.unitPrice
      + '；油卡扣款金额=' + it.raw.cardAmount + '；应扣=' + fmt(expect),
    advice: '加油量与扣款必须同源：升数来自油机、金额来自油卡流水。差值常见于按升结算与按金额结算混填。',
  };
}

function checkMileage(it) {
  const out = [];
  const odo = it.odometer;
  const prev = it.prevOdometer;
  const km = it.km;
  const refueling = it.liters !== null && it.liters > 0;
  if (refueling && (km === null || km === 0)) {
    out.push({
      line: it.line, level: 'P0', category: '行驶里程空缺', amount: 0,
      message: who(it) + ' 有加油量 ' + fmt(it.liters) + ' 升，但「行驶里程」为空或 0，这一行的油耗复算不出来。',
      evidence: '行驶里程=' + it.raw.km + '；里程表读数=' + it.raw.odometer + '；上期读数=' + it.raw.prevOdometer,
      advice: '留空表示「不知道」，本工具不用 0 替你假设；请补上本期行驶里程。',
    });
  }
  if (odo !== null && prev !== null && odo < prev - TOL) {
    out.push({
      line: it.line, level: 'P0', category: '里程表读数回退', amount: 0,
      message: who(it) + ' 里程表读数 ' + fmt(odo) + ' 小于上期读数 ' + fmt(prev)
        + '（倒退了 ' + fmt(round2(prev - odo)) + ' 公里）。',
      evidence: '里程表读数=' + it.raw.odometer + '；上期读数=' + it.raw.prevOdometer,
      advice: '换表、抄错、跨月抄表都会让读数倒退；先确认这一行的两个读数是不是同一只表。',
    });
  }
  if (refueling && km !== null && odo !== null && prev !== null) {
    const expect = round2(odo - prev);
    const diff = round2(km - expect);
    if (Math.abs(diff) > TOL) {
      out.push({
        line: it.line, level: 'P0', category: '行驶里程与里程表读数不符', amount: 0,
        message: who(it) + ' 里程表读数 ' + fmt(odo) + ' − 上期读数 ' + fmt(prev) + ' = ' + fmt(expect)
          + '，但行驶里程填的是 ' + fmt(km) + '，相差 ' + fmt(diff) + ' 公里。',
        evidence: '里程表读数=' + it.raw.odometer + '；上期读数=' + it.raw.prevOdometer
          + '；行驶里程=' + it.raw.km + '；读数差=' + fmt(expect),
        advice: '三个里程格必须互相对得上；对不上先别用这一行的油耗去谈考核。',
      });
    }
  }
  return out;
}

function checkDuplicateRefuel(items) {
  const seen = {};
  const out = [];
  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    if (it.liters === null || it.liters <= 0) continue;
    const key = String(it.plate || '') + '|' + String(it.date || '');
    if (key === '|') continue;
    if (seen[key]) {
      seen[key].n += 1;
      out.push({
        line: it.line, level: 'P0', category: '同一车同一日期重复加油', amount: 0,
        message: who(it) + ' 同一天出现第 ' + seen[key].n + ' 次加油（第 ' + it.line + ' 行；'
          + '最早一次在第 ' + seen[key].line + ' 行，加油量 ' + fmt(seen[key].liters) + ' 升），'
          + '本次加油量 ' + fmt(it.liters) + ' 升。',
        evidence: '车牌号=' + it.raw.plate + '；业务日期=' + it.raw.date + '；加油量=' + it.raw.liters,
        advice: '同一台车同一天加两次油本身可能正常（长途 / 一车两卡）；请确认是否重复贴行，'
          + '确属两次就把日期或时段写清楚，别让油卡台账出现两行一模一样的记录。',
      });
    } else {
      seen[key] = { line: it.line, n: 1, liters: it.liters };
    }
  }
  return out;
}

function checkTotalsRow(totals, items) {
  const out = [];
  if (!totals || !totals.line) return out;
  for (let r = 0; r < SUM_ROLES.length; r++) {
    const role = SUM_ROLES[r];
    const actual = totals.row[role];
    if (actual === null || actual === undefined) continue;
    const sum = totals.sum[role];
    const diff = round2(actual - sum);
    if (Math.abs(diff) <= TOL) continue;
    out.push({
      line: totals.line, level: 'P0', category: '合计行与明细之和不符', amount: Math.abs(diff),
      message: '合计行（第 ' + totals.line + ' 行）的「' + LABELS[role] + '」是 ' + fmt(actual)
        + '，明细行逐行相加是 ' + fmt(sum) + '，相差 ' + fmt(diff) + '。',
      evidence: '合计行=' + totals.row.raw[role] + '；明细逐行之和=' + fmt(sum) + '；差额=' + fmt(diff),
      advice: '合计行是对外报出的数；明细改过之后合计必须重算，逐行都对而合计对不上就是合计行本身没刷新。',
    });
  }
  return out;
}

function run(payload) {
  const p = payload || {};
  if (payload === null || payload === undefined || typeof payload !== 'object' || Array.isArray(payload)) {
    return insufficient(['入参必须是形如 {"text": "…"} 的对象（收到的类型不对）']);
  }
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  const trimmed = text.trim();
  if (trimmed === '') return insufficient(['材料文本为空：请把油卡充值与油耗明细表（含表头）贴进来']);
  if (trimmed.length < 2) return insufficient(['材料文本只有一个字符，不是一张表']);

  const table = parseTable(text);
  if (!table.header.length || !table.headerRoles.some((r) => r)) {
    return insufficient(['认不出表头：第一行必须是列名（' + REQUIRED.map((r) => LABELS[r]).join(' / ')
      + '），Tab 分隔最稳']);
  }
  if (table.missingColumns.length) {
    return insufficient(['缺少必需列：' + table.missingColumns.join('、'),
      '认出的表头：' + table.header.filter((h) => roleOf(h)).join('、')]);
  }
  if (!table.items.length) {
    return insufficient(['只有表头，没有明细行：这张表至少要有一行油卡充值或加油记录']);
  }

  const items = table.items;
  const findings = [];
  const perRow = [checkBalance, checkConsumption, checkOverCap, checkCardAmount];
  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    for (let c = 0; c < perRow.length; c++) {
      const f = perRow[c](it);
      if (f) findings.push(f);
    }
    const ms = checkMileage(it);
    for (let m = 0; m < ms.length; m++) findings.push(ms[m]);
  }
  const dups = checkDuplicateRefuel(items);
  for (let i = 0; i < dups.length; i++) findings.push(dups[i]);
  const tot = checkTotalsRow(table.totals, items);
  for (let i = 0; i < tot.length; i++) findings.push(tot[i]);

  const executed = CHECKS_GIVEN.slice();
  const notRun = CHECKS_WITHHELD.slice();
  const periods = [];
  const fleets = [];
  const cards = [];
  let rechargeTotal = 0;
  let litersTotal = 0;
  let cardAmountTotal = 0;
  let kmTotal = 0;
  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    if (it.period && periods.indexOf(it.period) < 0) periods.push(it.period);
    if (it.fleet && fleets.indexOf(it.fleet) < 0) fleets.push(it.fleet);
    if (it.cardNo && cards.indexOf(it.cardNo) < 0) cards.push(it.cardNo);
    rechargeTotal = round2(rechargeTotal + (it.recharge === null ? 0 : it.recharge));
    litersTotal = round2(litersTotal + (it.liters === null ? 0 : it.liters));
    cardAmountTotal = round2(cardAmountTotal + (it.cardAmount === null ? 0 : it.cardAmount));
    kmTotal = round2(kmTotal + (it.km === null ? 0 : it.km));
  }

  const result = {
    status: 'success',
    service_type: 'FLEET_FUEL_CARD_CHECK',
    scope: {
      checks: executed,
      checks_not_run: notRun,
      withheld: [],
      rows: items.length,
      periods: periods.length,
      fleets: fleets.length,
      cards: cards.length,
      totals_row: Boolean(table.totals.line),
      totals_rows: table.totals.rows,
      recharge_total: rechargeTotal,
      liters_total: litersTotal,
      card_amount_total: cardAmountTotal,
      km_total: kmTotal,
      consumption_avg: kmTotal > 0 ? round2(litersTotal / kmTotal * 100) : 0,
      tolerance: TOL,
      executed_locally: true,
      network_used: false,
    },
    findings: findings,
    checks_executed: executed,
    checks_withheld: notRun,
    checks_given: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
    note: '每条结论都带原文行号（含表头，从 1 起）与车牌号 / 油卡号，可由第三方用同一份输入复算。',
    disclaimer: '本工具只核表内勾稽：表中的加油量、加油单价、油卡扣款、卡余额、里程与路况 / 载重 / '
      + '用车性质一律以你填的为准，不去查油卡系统、GPS 里程或油站小票。',
  };



  findings.sort((a, b) => (a.line - b.line) || (LEVEL_ORDER[a.level] - LEVEL_ORDER[b.level])
    || (a.category < b.category ? -1 : a.category > b.category ? 1 : 0));

  let p0 = 0;
  let p1 = 0;
  let p2 = 0;
  for (let i = 0; i < findings.length; i++) {
    if (findings[i].level === 'P0') p0 += 1;
    else if (findings[i].level === 'P1') p1 += 1;
    else p2 += 1;
  }
  result.summary = {
    rows: items.length,
    periods: periods.length,
    fleets: fleets.length,
    total: findings.length,
    p0: p0,
    p1: p1,
    p2: p2,
    verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'WARNING_FOUND' : 'NO_ISSUE_FOUND'),
    omitted: 0,
  };
  result.note += '未执行的检查项见 scope.checks_not_run（本工具不会用默认值把它们编出来）。';
  return { status: 'success', result: result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, isBlank, splitRow, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE,
};
