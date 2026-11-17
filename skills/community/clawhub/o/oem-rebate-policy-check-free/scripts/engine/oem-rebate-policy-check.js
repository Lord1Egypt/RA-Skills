/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * oem-rebate-policy-check.js —— 整车厂返利与商务政策核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**4S 店 / 经销商的财务每月（以及每个季度返利结算前）**。
 * 整车厂按商务政策给的返利 —— 提车返利、零售返利、达标返利、广告补贴 —— 必须与
 * **提车台数、零售台数、考核目标**逐项勾稽：返利算错就是几十万白丢，也是厂家结算
 * 扯皮的高发区（"你的零售台数没达标所以我扣了达标返利"、"这台车你已经计过提车返利了"）。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   单车返利金额 = 返利金额 ÷ 台数
 *   应返利金额   = 台数 × 单车返利标准
 *   合计行各列   = 明细行相加
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**商务政策条款本身该怎么解释（返利档位、达标口径、阶梯比例、返利上限、
 *    扣罚与质保金条款）：表里的提车台数、零售台数、考核目标、单车返利标准一律
 *    **以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '单车返利金额复算（返利金额 ÷ 台数 = 单车返利金额）',
  '应返利金额复算（台数 × 单车返利标准 = 应返利金额）',
  '合计行逐列复核',
  '同一期间同一返利类型重复行检测',
  '空白与占位符检测',
  '金额或台数为负检测',
];

const CHECKS_WITHHELD = [
  '零售台数超过提车台数（异常）提示',
  '达标率未达考核线却计提达标返利提示',
  '已收返利超过应返利金额提示',
  '单车返利标准与商务政策不一致提示',
  '同一台数重复计入不同返利类型提示',
];

const OUT_OF_SCOPE = [
  '判断商务政策条款本身该怎么解释（返利档位、阶梯比例、达标口径、返利上限、扣罚与质保金条款，属于商务政策与合同判断）',
  '判断返利该按含税还是不含税口径计提，以及返利开票、红字发票、增值税与所得税处理',
  '判断跨期返利该挂在哪一期、是否需要追溯调整（属于会计期间与会计政策判断）',
  '核对厂家返利系统 / DMS / ERP 里的原始数据与实物台数（需要你先导出成文本贴进来）',
  '读取 DMS / 厂家返利系统 / ERP 导出文件（本工具不联网、不调用任何接口）',
];

/** 14 列表头：所属期间 / 整车厂 / 商务政策编号 / 返利类型 / 提车台数 / 零售台数 / 目标台数 /
    台数 / 返利金额 / 应返利金额 / 单车返利标准 / 单车返利金额 / 达标率 / 已收返利 */
const COLS = ['所属期间', '整车厂', '商务政策编号', '返利类型', '提车台数', '零售台数', '目标台数',
  '台数', '返利金额', '应返利金额', '单车返利标准', '单车返利金额', '达标率', '已收返利'];

const SAMPLE_TEXT = [
  COLS.join('\t'),
  ['2026-05', '上汽大众', 'SWP-2026-01', '提车返利', '120', '100', '100', '120',
    '240000.00', '240000.00', '2000.00', '2000.00', '100.00%', '240000.00'].join('\t'),
  ['2026-05', '上汽大众', 'SWP-2026-01', '零售返利', '120', '100', '100', '100',
    '150000.00', '150000.00', '1500.00', '1500.00', '100.00%', '150000.00'].join('\t'),
  ['2026-05', '上汽大众', 'SWP-2026-01', '达标返利', '120', '100', '100', '100',
    '80000.00', '80000.00', '800.00', '800.00', '100.00%', '80000.00'].join('\t'),
  ['2026-06', '上汽大众', 'SWP-2026-01', '提车返利', '130', '120', '110', '130',
    '260000.00', '260000.00', '2000.00', '2000.00', '109.09%', '260000.00'].join('\t'),
  ['2026-06', '上汽大众', 'SWP-2026-01', '零售返利', '130', '120', '110', '120',
    '180000.00', '180000.00', '1500.00', '1500.00', '109.09%', '180000.00'].join('\t'),
  ['2026-06', '上汽大众', 'SWP-2026-01', '达标返利', '130', '120', '110', '110',
    '88000.00', '88000.00', '800.00', '800.00', '109.09%', '88000.00'].join('\t'),
  ['合计', '', '', '', '750', '660', '630', '680',
    '998000.00', '998000.00', '', '', '', '998000.00'].join('\t'),
].join('\n');

const TOL = 0.01;
/** 达标率容差：0.5 个百分点（考核线认定以商务政策为准，这里只拦"差得明显"的） */
const ACHIEVE_TOL = 0.005;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前 ——
  //    「提车台数」「零售台数」「目标台数」必须排在「台数」前，否则会被泛化的「台数」抢走；
  //    「应返利金额」「已收返利金额」「单车返利金额」必须排在「返利金额」前，同理。
  period: ['所属期间', '会计期间', '结算期间', '返利期间', '政策期间', '所属期', '期间', '月份', '月度'],
  oem: ['整车厂名称', '整车厂', '主机厂', '汽车厂商', '汽车厂', '品牌厂商'],
  policy: ['商务政策编号', '商务政策号', '政策编号', '政策文号', '商务政策', '政策名称', '政策号'],
  rebateType: ['返利类型', '返利类别', '返利科目', '返利项目', '返利种类', '返利名目'],
  wholesale: ['提车台数', '提车数量', '提车量', '批发台数', '批发数量', '进货台数', '采购台数'],
  retail: ['零售台数', '零售数量', '零售量', '终端台数', '终端销量', '实销台数', '零售销量', '交付台数'],
  target: ['考核目标台数', '目标台数', '考核目标', '目标任务', '目标数量', '目标销量', '目标量'],
  units: ['返利台数', '计奖台数', '结算台数', '返利数量', '计奖数量', '台数', '数量'],
  received: ['已收返利金额', '已收返利', '已结算返利', '已兑付返利', '已到账返利', '实收返利', '厂家已付返利'],
  rebateDue: ['应返利金额', '应计提返利金额', '应结返利金额', '应收返利金额', '应返利', '应结返利'],
  unitRebateAmount: ['单车返利金额', '单台返利金额', '单车返利额', '单台返利额', '单车返利单价'],
  unitStd: ['单车返利标准', '单台返利标准', '单车标准', '单台标准', '返利标准', '单车政策标准', '元/台'],
  achieveRate: ['达标率', '达成率', '完成率', '考核完成率'],
  rebateAmount: ['返利金额', '返利总额', '返利合计', '计提返利', '返利额', '返利'],
};

const LABELS = {
  period: '所属期间', oem: '整车厂', policy: '商务政策编号', rebateType: '返利类型',
  wholesale: '提车台数', retail: '零售台数', target: '目标台数', units: '台数',
  rebateAmount: '返利金额', rebateDue: '应返利金额', unitStd: '单车返利标准',
  unitRebateAmount: '单车返利金额', achieveRate: '达标率', received: '已收返利',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'oem', 'policy', 'rebateType', 'wholesale', 'retail', 'target', 'units',
  'rebateAmount', 'rebateDue', 'unitStd', 'unitRebateAmount', 'received'];
/** 合计行逐列复核的列（台数与金额才可加总；达标率、单车标准是比率/单价，不加总） */
const SUM_ROLES = ['wholesale', 'retail', 'target', 'units', 'rebateAmount', 'rebateDue', 'received'];
/** 负值检测覆盖的列：台数与金额 */
const NEGATIVE_ROLES = ['wholesale', 'retail', 'target', 'units', 'rebateAmount', 'rebateDue',
  'unitStd', 'unitRebateAmount', 'received'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
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

/** 比率归一化成小数：`109.09%` ⇒ 1.0909；`1.0909` ⇒ 1.0909；`109.09` ⇒ 1.0909 */
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
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.oem, it && it.rebateType]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const oemKeyOf = (it) => {
  const v = it && it.oem !== undefined ? String(it.oem).trim() : '';
  return v || `第 ${it && it.line} 行`;
};

const policyKeyOf = (it) => {
  const v = it && it.policy !== undefined ? String(it.policy).trim() : '';
  return v || '（未填商务政策编号）';
};

const typeKeyOf = (it) => {
  const v = it && it.rebateType !== undefined ? String(it.rebateType).trim() : '';
  return v || '（未填返利类型）';
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkUnitRebateAmount(it) {
  const out = [];
  const amount = normNumber(it.rebateAmount);
  const units = normNumber(it.units);
  const stated = normNumber(it.unitRebateAmount);
  if (amount === null || units === null || stated === null) return out;
  if (units <= 0) return out;                 // 台数填 0 或负：算不出单车返利（负值由负值检测报）
  const expect = round2(amount / units);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '单车返利金额复算不符', line: it.line,
    message: `${who(it)}：返利金额 ${amount.toFixed(2)} ÷ 台数 ${units} = 单车 ${expect.toFixed(2)}，`
      + `表里「单车返利金额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '单车返利金额是拿商务政策档位跟厂家对账的抓手，它跟"返利金额 ÷ 台数"对不上，'
      + '要么返利金额填错，要么台数填错，要么单车金额抄错。',
  });
  return out;
}

function checkRebateDue(it) {
  const out = [];
  const units = normNumber(it.units);
  const std = normNumber(it.unitStd);
  const stated = normNumber(it.rebateDue);
  if (units === null || std === null || stated === null) return out;
  const expect = round2(units * std);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '应返利金额复算不符', line: it.line,
    message: `${who(it)}：台数 ${units} × 单车返利标准 ${std.toFixed(2)} = 应返 ${expect.toFixed(2)}，`
      + `表里「应返利金额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '应返利金额就是本该向厂家索取的金额：算少了就是白丢，算多了厂家结算时会扣回来还留下坏记录。',
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
    const expect = round2(sum);
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是跟厂家对账、向老板汇报时的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const t = it.rebateType !== undefined ? String(it.rebateType).trim() : '';
    if (!p || !t) continue;
    const key = `${periodKeyOf(it)}|${oemKeyOf(it)}|${typeKeyOf(it)}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一期间同一返利类型重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一整车厂、同一返利类型再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一笔返利被拆成两行（比如分两次结算各建一行），'
          + '多出来的那一行会把返利金额与台数都重复计一遍，等于向厂家多要一笔钱。',
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
          message: `${who(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`
            + '这一列缺失时对应的复算与勾稽做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
        });
      }
    }
  }
  return out;
}

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '金额或台数为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 台数、返利金额、单车返利标准都不该为负，`
        + '冲回 / 红字（比如厂家扣回的返利）应单独列示并在备注里说明，而不是直接写成负数。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 这一行的返利按哪个台数口径计提：提车类看「提车台数」，零售类看「零售台数」，其余（达标/广告）不按台数 */
/** 本行的达标率：优先用「零售台数 ÷ 目标台数」实算，算不出来才用表里的「达标率」 */
/** 同一整车厂 + 同一商务政策编号 + 同一返利类型 分组（用来判断单车标准是否跟着政策走） */
/** 同一期间 + 同一整车厂 + 同一商务政策编号 分组（用来判断台数有没有被重复计入） */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到整车厂返利与商务政策核对表正文（text）—— 请把「所属期间 / 整车厂 / 商务政策编号 / 返利类型 / 提车台数 / 零售台数 / 目标台数 / 台数 / 返利金额 / 应返利金额 / 单车返利标准 / 单车返利金额 / 达标率 / 已收返利」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `整车厂返利与商务政策核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何返利明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkUnitRebateAmount(it));
    findings.push(...checkRebateDue(it));
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

  let wholesaleTotal = 0;
  let retailTotal = 0;
  let rebateTotal = 0;
  let rebateDueTotal = 0;
  let receivedTotal = 0;
  for (const it of t.items) {
    const w = normNumber(it.wholesale);
    if (w !== null) wholesaleTotal += w;
    const r = normNumber(it.retail);
    if (r !== null) retailTotal += r;
    const a = normNumber(it.rebateAmount);
    if (a !== null) rebateTotal += a;
    const d = normNumber(it.rebateDue);
    if (d !== null) rebateDueTotal += d;
    const g = normNumber(it.received);
    if (g !== null) receivedTotal += g;
  }

  const result = {
    status: 'success',
    service_type: 'OEM_REBATE_POLICY_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      wholesale_units_total: round2(wholesaleTotal),
      retail_units_total: round2(retailTotal),
      rebate_total: round2(rebateTotal),
      rebate_due_total: round2(rebateDueTotal),
      rebate_received_total: round2(receivedTotal),
      tolerance: TOL,
      achieve_tolerance: ACHIEVE_TOL,
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
    disclaimer: '只核"返利金额 ÷ 台数 = 单车返利金额""台数 × 单车返利标准 = 应返利金额"这类**表内勾稽**与档位提示，'
      + '**不判断商务政策条款本身该怎么解释**（返利档位、达标口径、阶梯比例、返利上限、扣罚与质保金，'
      + '以商务政策原文与厂家结算单为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
