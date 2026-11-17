/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * construction-wage-special-account-check.js —— 建筑工人工资专户发放核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**总包每月发工资之前**。农民工工资专用账户是监管硬要求：
 * 实名制考勤工时、工资表、专户代发流水**必须三方一致** —— 对不上就是欠薪风险，
 * 轻则被责令补发、重则被人社与住建部门通报（还会被暂停投标 / 记入信用档案）。
 *
 * 这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   应发工资 = 考勤工时 × 小时工资（计件工人则是：计件数量 × 计件单价）
 *   实发工资 = 应发工资 − 代扣项合计
 *   合计行各列 = 明细行相加
 *   实发工资合计 = 专户代发流水合计（工资表与银行代发的钱必须是同一个数）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**某个工人该发多少工资、代扣项合不合法、当地最低工资标准到底是多少
 *    （那属于劳动法与用工管理判断）：表里给的工时、小时工资、代扣项、当地最低工资标准
 *    一律**以你填的为准**，本工具只核表内勾稽，并把可疑处按原文行号列出来。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时会走形态 A 把免费检查也整块删掉）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚。
 */

const CHECKS_GIVEN = [
  '应发工资复算（考勤工时 × 小时工资，或计件数量 × 计件单价 = 应发工资）',
  '实发工资复算（应发工资 − 代扣项合计 = 实发工资）',
  '合计行逐列复核',
  '同一工人同一项目同一期间重复行检测',
  '空白与占位符检测',
  '工时或金额为负检测',
];

const CHECKS_WITHHELD = [
  '实发工资合计与专户代发流水合计不符提示',
  '实发工资低于当地最低工资标准提示（参考口径）',
  '同一工人跨项目重复发放提示',
  '代扣项合计超过应发工资提示',
  '已发工资但无实名制考勤记录提示',
];

const OUT_OF_SCOPE = [
  '判断某个工人该不该发、该发多少工资（劳动合同、计件约定、加班费口径、包工头劳务费与工资的区分，属于劳动法与用工管理判断，请咨询劳资专管员或劳动法顾问）',
  '判断代扣项本身是否合法（个人所得税、社保公积金个人部分、伙食费、借支、罚款等扣款的合规性）',
  '判断当地最低工资标准到底是多少、以及不满勤 / 新进场 / 中途离场工人的折算口径（表里填的「当地最低工资标准」一律以你填的为准）',
  '与住建 / 人社监管平台（实名制管理系统、农民工工资支付监管平台）联网比对，以及专户余额与工程款拨付进度核对',
  '读取考勤机 / 实名制系统 / 银行代发系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t项目名称\t工人姓名\t身份证号\t所属班组\t考勤工时\t小时工资\t计件数量\t计件单价\t应发工资\t代扣项合计\t实发工资\t专户代发金额\t代发流水号\t实名制考勤记录\t当地最低工资标准',
  '2026-03\t幸福家园A区项目\t张建国\t3201**********1234\t钢筋班组\t200\t26.00\t-\t-\t5200.00\t220.00\t4980.00\t4980.00\tDF20260301001\t已实名打卡\t2490.00',
  '2026-03\t幸福家园A区项目\t李秀兰\t3201**********5678\t钢筋班组\t176\t25.00\t-\t-\t4400.00\t108.00\t4292.00\t4292.00\tDF20260301002\t已实名打卡\t2490.00',
  '2026-03\t幸福家园A区项目\t王志强\t3201**********9012\t木工班组\t152\t28.00\t-\t-\t4256.00\t56.00\t4200.00\t4200.00\tDF20260301003\t已实名打卡\t2490.00',
  '合计\t-\t-\t-\t-\t528.00\t-\t-\t-\t13856.00\t384.00\t13472.00\t13472.00\t-\t-\t-',
].join('\n');

const TOL = 0.01;

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前。
  //    角色之间也讲顺序：「专户代发金额」不能被「实发」抢走、「代发流水号」不能被「代发金额」抢走、
  //    「当地最低工资标准」不能被「实发工资」抢走 ⇒ 更具体的角色（paidOut / serial / attendance / minWage）
  //    排在更宽泛的金额角色（gross / deduction / net）前面。
  period: ['所属期间', '工资期间', '发放期间', '所属期', '期间', '月份', '月度'],
  project: ['项目名称', '工程项目', '在建项目', '工程名称', '项目'],
  worker: ['工人姓名', '人员姓名', '姓名', '工人', '人员'],
  idcard: ['身份证号', '身份证件号', '证件号码', '身份证'],
  team: ['所属班组', '班组名称', '班组', '工种'],
  hours: ['考勤工时', '出勤工时', '实名制工时', '工时'],
  hourlyRate: ['小时工资', '小时单价', '计时单价', '时薪'],
  pieces: ['计件数量', '完成数量', '计件量', '数量'],
  pieceRate: ['计件单价', '计件工资单价', '单价'],
  paidOut: ['专户代发金额', '专户发放金额', '代发流水金额', '银行代发金额', '代发金额'],
  serial: ['代发流水号', '发放流水号', '交易流水号', '流水号', '代发批次'],
  attendance: ['实名制考勤记录', '实名制考勤', '考勤记录', '考勤状态', '实名制打卡', '考勤'],
  minWage: ['当地最低工资标准', '最低工资标准', '最低工资'],
  gross: ['应发工资', '应发金额', '应发合计', '应发'],
  deduction: ['代扣项合计', '代扣合计', '代扣款项', '代扣金额', '扣款合计', '代扣'],
  net: ['实发工资', '实发金额', '实发合计', '实发'],
};

const LABELS = {
  period: '所属期间', project: '项目名称', worker: '工人姓名', idcard: '身份证号', team: '所属班组',
  hours: '考勤工时', hourlyRate: '小时工资', pieces: '计件数量', pieceRate: '计件单价',
  gross: '应发工资', deduction: '代扣项合计', net: '实发工资', paidOut: '专户代发金额',
  serial: '代发流水号', attendance: '实名制考勤记录', minWage: '当地最低工资标准',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'project', 'worker', 'gross', 'deduction', 'net'];
/** 应发工资的两条口径：任一组成立即可复算（计时 或 计件） */
const TIMED_PAIR = ['hours', 'hourlyRate'];
const PIECE_PAIR = ['pieces', 'pieceRate'];
/** 合计行逐列复核的列 */
const SUM_ROLES = ['hours', 'gross', 'deduction', 'net'];
/**
 * 免费档负值检测覆盖的列：**投入侧与工资表侧**的工时与金额。
 * ⚠️ 刻意**不含**实发工资 —— "代扣项合计超过应发工资"就是实发为负的那种表，
 *    那是完整档的独立检查项（见 CHECKS_WITHHELD）；免费档提前报出实发为负，
 *    等于把付费结论送出去了。⚠️ 也不含专户代发金额与当地最低工资标准（它们的口径属于完整档）。
 */
const NEGATIVE_ROLES = ['hours', 'pieces', 'hourlyRate', 'pieceRate', 'gross', 'deduction'];
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

const cell = (v) => (v === undefined || v === null ? '' : String(v).trim());

const who = (it) => {
  const p = cell(it && it.period) || `第 ${it && it.line} 行`;
  const n = [it && it.project, it && it.worker].map(cell).filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => cell(it && it.period) || `第 ${it && it.line} 行`;

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkGrossRecompute(it) {
  const out = [];
  const gross = normNumber(it.gross);
  if (gross === null) return out;
  const hours = normNumber(it.hours);
  const hourly = normNumber(it.hourlyRate);
  const pieces = normNumber(it.pieces);
  const pieceRate = normNumber(it.pieceRate);
  let expect = null;
  let how = '';
  if (hours !== null && hourly !== null) {
    expect = round2(hours * hourly);
    how = `考勤工时 ${hours} × 小时工资 ${hourly.toFixed(2)}`;
  } else if (pieces !== null && pieceRate !== null) {
    expect = round2(pieces * pieceRate);
    how = `计件数量 ${pieces} × 计件单价 ${pieceRate.toFixed(2)}`;
  }
  if (expect === null) return out;
  if (Math.abs(expect - gross) <= TOL) return out;
  out.push({
    level: 'P0', category: '应发工资复算不符', line: it.line,
    message: `${who(it)}：${how} = ${expect.toFixed(2)}，表里「应发工资」是 ${gross.toFixed(2)}，`
      + `相差 ${round2(gross - expect).toFixed(2)}。`
      + '应发工资就是"工时 × 单价"（计件就是"数量 × 单价"）：这一格错了，后面实发、代发、个税全都跟着错，'
      + '而且监管平台比对考勤工时与工资表时第一个就比出来。',
  });
  return out;
}

function checkNetRecompute(it) {
  const out = [];
  const gross = normNumber(it.gross);
  const deduction = normNumber(it.deduction);
  const stated = normNumber(it.net);
  if (gross === null || deduction === null || stated === null) return out;
  const expect = round2(gross - deduction);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '实发工资复算不符', line: it.line,
    message: `${who(it)}：应发工资 ${gross.toFixed(2)} − 代扣项合计 ${deduction.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「实发工资」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '工人到手的钱与工资表对不上，是最容易被投诉到劳动监察的一类问题：'
      + '要么代扣项合计没算全（个税、社保个人部分、伙食、借支），要么实发那一格是手改过的。',
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
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，本表 ${n} 行明细的「${LABELS[role]}」相加是 `
        + `${expect.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
        + '合计行就是报给监管平台与银行代发的取数口径：对不上说明有一边错，'
        + '多发或少发都是以这个数为准的。',
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = cell(it.period);
    const proj = cell(it.project);
    const w = cell(it.worker);
    if (!p || !proj || !w) continue;
    const key = `${p}|${proj}|${w}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一工人同一项目同一期间重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一期间、同一项目、同一工人再次出现 —— `
          + '要么是重复粘贴了一行（多发一次工资、专户多一笔代发），要么是本月补发上月与本月工资各建了一行却写成了同一个期间。'
          + '专户代发是按行出盘的，重复行就是重复发钱。',
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
        const s = cell(it[role]);
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

function checkNegative(it) {
  const out = [];
  for (const role of NEGATIVE_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '工时或金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 工时、单价、应发工资与代扣项合计都不该为负，`
        + '冲回 / 红字（比如扣回上月多发的工资）应当单独列一行并在备注里说明，'
        + '负号留在这些列里会让合计与代发金额一起算错。',
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
  const src = payload && typeof payload.text === 'string' ? payload.text : '';
  if (src.trim().length < 5) {
    return insufficient('没有收到建筑工人工资专户发放核对表正文（text）—— 请把「所属期间 / 项目名称 / 工人姓名 / 考勤工时 / 小时工资 / 应发工资 / 代扣项合计 / 实发工资」这张表贴进来');
  }
  const t = parseTable(src);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `建筑工人工资专户发放核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(src.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何工人工资明细行');
  }
  const timedOk = TIMED_PAIR.some((r) => t.items.some((it) => !isBlank(it[r])));
  const pieceOk = PIECE_PAIR.some((r) => t.items.some((it) => !isBlank(it[r])));
  if (!timedOk && !pieceOk) {
    return insufficient([
      '既没有「考勤工时 + 小时工资」，也没有「计件数量 + 计件单价」—— 应发工资无从复算',
      '请补上计时口径（考勤工时、小时工资）或计件口径（计件数量、计件单价）两组列中的至少一组',
    ]);
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkGrossRecompute(it));
    findings.push(...checkNetRecompute(it));
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

  let netTotal = 0;
  let payoutTotal = 0;
  let hoursTotal = 0;
  for (const it of t.items) {
    const n = normNumber(it.net);
    if (n !== null) netTotal += n;
    const p = normNumber(it.paidOut);
    if (p !== null) payoutTotal += p;
    const h = normNumber(it.hours);
    if (h !== null) hoursTotal += h;
  }

  return {
    status: 'success',
    result: {
      status: 'success',
      service_type: 'CONSTRUCTION_WAGE_SPECIAL_ACCOUNT_CHECK',
      scope: {
        checks: CHECKS_GIVEN,
        checks_not_run: notRun,
        rows: t.items.length,
        periods: groups.size,
        totals_row: Boolean(t.totals && t.totals.row),
        net_total: round2(netTotal),
        payout_total: round2(payoutTotal),
        hours_total: round2(hoursTotal),
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
      disclaimer: '只核"考勤工时 × 小时工资（或计件数量 × 计件单价）= 应发工资""应发工资 − 代扣项合计 = 实发工资"'
        + '这类**表内勾稽**，以及工资表与专户代发流水的合计一致性；'
        + '**不判断某个工人该发多少工资、代扣项是否合法、当地最低工资标准是多少**（以劳动合同、当地规定与劳资专管员口径为准）；'
        + '结论可由第三方用同一份输入复算。',
    },
  };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
