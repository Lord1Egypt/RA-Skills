#!/usr/bin/env node
/**
 * overtime-pay-check.js —— 加班费核算核对引擎（确定性、纯 Node 标准库）。
 *
 * 真实痛点：**每月发薪前，HR/财务都要核一遍加班费** ——
 * 小时工资 = 月工资 ÷ 21.75 ÷ 8，再按 1.5 / 2 / 3 倍分别算平时、休息日、法定节假日的加班费。
 * 倍数用错、时数录错、合计少加一项，都会直接体现在员工工资条上，**算错就是劳动争议**。
 * 单量一多（几十上百人 × 三个类别），人眼核不动；而这些都是**纯算术**。
 *
 * 与已有能力的区别：`payroll-check` 核的是**发薪总额**（应发/社保/实发是否勾稽），
 * **不算加班倍数、不算小时工资折算**；`lesson-hour-check` 是课时核销，完全另一回事。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：run(payload) -> {status:'success',result} | {status:'insufficient_input',missing,advice}
 * 刻意不做：不联网、不调用大模型；材料不足不给结论；不判断考勤是否真实。
 */
'use strict';

const CHECKS_GIVEN = [
  '小时工资勾稽（月工资 ÷ 计薪天数 ÷ 8；计薪天数缺省按法定 21.75）',
  '平时加班费勾稽（小时工资 × 1.5 × 平时加班时数）',
  '休息日加班费勾稽（小时工资 × 2 × 休息日加班时数）',
  '法定节假日加班费勾稽（小时工资 × 3 × 法定节假日加班时数）',
  '加班费合计勾稽（三项加班费之和）',
  '合计行逐列复核（每一列的合计是否等于各行之和）',
  '重复人员检测',
  '空白与占位符检测',
];

const CHECKS_WITHHELD = [
  '月加班总时数超过 36 小时（法定延长工时上限）检测',
  '折算小时工资低于给定最低工资标准检测（最低工资由入参给出）',
  '月工资非正或加班时数为负检测',
  '计薪天数偏离 20~23 天（含法定 21.75）检测',
];

const OUT_OF_SCOPE = [
  '判断考勤记录是否真实（那是考勤系统与HR的事；本工具只核你给出的这张表算得对不对）',
  '判断加班是否经过审批、是否应认定为加班',
  '判断综合计算工时制 / 不定时工时制的特殊口径（那要按审批的工时制度另算）',
  '给出劳动法意见或预测仲裁结果',
  '读取 .xlsx（需要你先从系统导出、复制成文本贴进来）',
];

const SAMPLE_TEXT = [
  '姓名\t月工资\t计薪天数\t小时工资\t平时加班时数\t休息日加班时数\t法定节假日加班时数\t平时加班费\t休息日加班费\t法定节假日加班费\t加班费合计',
  '张三\t8700.00\t21.75\t50.00\t10\t8\t0\t750.00\t800.00\t0.00\t1550.00',
  '李四\t6960.00\t21.75\t40.00\t6\t0\t7\t360.00\t0.00\t840.00\t1200.00',
  '合计\t15660.00\t\t\t16\t8\t7\t1110.00\t800.00\t840.00\t2750.00',
].join('\n');

const TOL = 0.01;
const LEGAL_BASE_DAYS = 21.75;

const ROLES = {
  party: ['姓名', '员工', '人员', '名字'],
  hourly: ['小时工资', '时薪', '小时单价'],
  baseDays: ['计薪天数', '月计薪天数', '计薪日'],
  feeNormal: ['平时加班费', '工作日加班费', '延时加班费'],
  feeRest: ['休息日加班费', '周末加班费'],
  feeHoliday: ['法定节假日加班费', '节假日加班费'],
  total: ['加班费合计', '合计加班费', '加班费'],
  otNormal: ['平时加班时数', '平时加班', '工作日加班'],
  otRest: ['休息日加班时数', '休息日加班', '周末加班'],
  otHoliday: ['法定节假日加班时数', '法定节假日加班', '节假日加班'],
  wage: ['月工资', '月薪', '应发工资', '工资'],
};

const LABELS = {
  party: '姓名', wage: '月工资', baseDays: '计薪天数', hourly: '小时工资',
  otNormal: '平时加班时数', otRest: '休息日加班时数', otHoliday: '法定节假日加班时数',
  feeNormal: '平时加班费', feeRest: '休息日加班费', feeHoliday: '法定节假日加班费',
  total: '加班费合计',
};

const MULT = { feeNormal: 1.5, feeRest: 2, feeHoliday: 3 };
const HOURS_OF = { feeNormal: 'otNormal', feeRest: 'otRest', feeHoliday: 'otHoliday' };
const SUM_ROLES = ['wage', 'otNormal', 'otRest', 'otHoliday', 'feeNormal', 'feeRest', 'feeHoliday', 'total'];

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

const round2 = (n) => Math.round(n * 100) / 100;

const REQUIRED = ['party', 'wage', 'otNormal', 'otRest', 'otHoliday',
  'feeNormal', 'feeRest', 'feeHoliday', 'total'];

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
      row.isTotal = true; totals.push(row);
    } else {
      items.push(row);
    }
  }
  return { cols, items, totals };
}

/** 计薪天数：表里有就按表里的，没有就按法定 21.75（并在结果里说明）。 */
function baseDaysOf(it, used) {
  const n = normNumber(it.byRole.baseDays);
  if (n !== null && n > 0) return n;
  used.default = true;
  return LEGAL_BASE_DAYS;
}

function hourlyOf(it, used) {
  const stated = normNumber(it.byRole.hourly);
  if (stated !== null && stated > 0) return stated;
  const wage = normNumber(it.byRole.wage);
  if (wage === null) return null;
  return wage / baseDaysOf(it, used) / 8;
}

function label(it) {
  return `${LABELS.party}「${it.byRole.party || '(未命名)'}」`;
}

function checkHourly(it, used) {
  const stated = normNumber(it.byRole.hourly);
  if (stated === null) return null;                    // 表里没有这列 -> 本检查未执行（会在 checks_not_run 里说明）
  const wage = normNumber(it.byRole.wage);
  if (wage === null) return null;
  const days = baseDaysOf(it, used);
  const expect = round2(wage / days / 8);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: '小时工资与折算不符', line: it.line,
    message: `${label(it)}的小时工资是 ${stated.toFixed(2)}，`
      + `按 ${wage.toFixed(2)} ÷ ${days} 天 ÷ 8 小时复算应为 ${expect.toFixed(2)}。`,
    advice: '小时工资是全表的地基：它错了，三项加班费会一起错。请先确认月工资与计薪天数。',
  };
}

function checkFee(it, role, used) {
  const hours = normNumber(it.byRole[HOURS_OF[role]]);
  const stated = normNumber(it.byRole[role]);
  const hourly = hourlyOf(it, used);
  if (hours === null || stated === null || hourly === null) return null;
  const expect = round2(hourly * MULT[role] * hours);
  if (Math.abs(expect - stated) <= TOL) return null;
  return {
    level: 'P0', category: `${LABELS[role]}与复算不符`, line: it.line,
    message: `${label(it)}的${LABELS[role]}是 ${stated.toFixed(2)}，`
      + `按 小时工资 ${round2(hourly).toFixed(2)} × ${MULT[role]} 倍 × ${hours} 小时复算应为 ${expect.toFixed(2)}。`,
    advice: `确认倍数（${LABELS[role]}法定为 ${MULT[role]} 倍）与加班时数是否录错。`,
  };
}

function checkTotal(it) {
  const stated = normNumber(it.byRole.total);
  if (stated === null) return null;
  const parts = ['feeNormal', 'feeRest', 'feeHoliday'].map((r) => normNumber(it.byRole[r]));
  if (parts.some((p) => p === null)) return null;
  const sum = round2(parts.reduce((s, p) => s + p, 0));
  if (Math.abs(sum - stated) <= TOL) return null;
  return {
    level: 'P0', category: '加班费合计与三项之和不符', line: it.line,
    message: `${label(it)}的加班费合计是 ${stated.toFixed(2)}，三项相加是 ${sum.toFixed(2)}，`
      + `相差 ${round2(stated - sum).toFixed(2)} 元。`,
    advice: '通常是漏加了某一类加班费，或某一项算完后没回写到合计。',
  };
}

function checkTotalRow(totals, items, role) {
  const out = [];
  for (const t of totals) {
    const stated = normNumber(t.byRole[role]);
    if (stated === null) continue;
    const sum = round2(items.reduce((s, it) => {
      const n = normNumber(it.byRole[role]);
      return s + (n === null ? 0 : n);
    }, 0));
    if (Math.abs(sum - stated) > TOL) {
      out.push({
        level: 'P0', category: '合计行与明细之和不符', line: t.line,
        message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，各明细行相加是 ${sum.toFixed(2)}，相差 ${round2(stated - sum).toFixed(2)}。`,
        advice: '要么明细行漏了人，要么合计行没跟着更新。',
      });
    }
  }
  return out;
}

function checkDuplicates(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.byRole.party || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一人员出现多行', line: it.line,
        message: `「${key}」在第 ${seen.get(key)} 行已出现，第 ${it.line} 行再次出现。`,
        advice: '同一人多笔加班是正常的；但若本表按人汇总，重复行会让合计翻倍 —— 请确认口径。',
      });
    } else {
      seen.set(key, it.line);
    }
  }
  return out;
}

const PLACEHOLDER = /^(待填|待补|待定|xxx|xxx\.xx|\?+|tbd|n\/?a)$/i;

function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of ['wage', 'otNormal', 'otRest', 'otHoliday', 'feeNormal', 'feeRest', 'feeHoliday', 'total']) {
      const s = String(it.byRole[role] === undefined ? '' : it.byRole[role]).trim();
      if (s === '' || PLACEHOLDER.test(s)) {
        out.push({
          level: 'P0', category: '关键字段缺失或为占位符', line: it.line,
          message: `${label(it)}的「${LABELS[role]}」是空的或占位符（${s || '空'}）。`,
          advice: '缺这一格就算不出加班费；补齐前本工具不会用 0 或默认值替你填。',
        });
      }
    }
  }
  return out;
}

function run(payload) {
  const text = (payload && (payload.text || payload.content)) || '';
  if (!String(text).trim()) return insufficient(['原文（text）']);

  const t = parseTable(text);
  if (t.error === 'empty') return insufficient(['原文（text）']);
  if (t.error === 'no_header') {
    return insufficient([
      '含表头的加班费计算表（要能同时认出「姓名」「月工资」「平时/休息日/法定节假日加班时数」'
      + '「三项加班费」与「加班费合计」这几列）',
      `本次没认出来的列：${t.missingRoles.join('、')}`,
      '从系统导出后连同表头一起复制成文本贴进来（Tab 分隔最稳）',
    ]);
  }
  if (!t.items.length) return insufficient(['至少一人的明细行']);

  const used = { default: false };
  const findings = [];
  const notRun = [];

  for (const it of t.items) {
    const h = checkHourly(it, used); if (h) findings.push(h);
    for (const role of ['feeNormal', 'feeRest', 'feeHoliday']) {
      const f = checkFee(it, role, used); if (f) findings.push(f);
    }
    const tot = checkTotal(it); if (tot) findings.push(tot);
  }
  for (const role of SUM_ROLES) {
    for (const f of checkTotalRow(t.totals, t.items, role)) findings.push(f);
  }
  for (const f of checkDuplicates(t.items)) findings.push(f);
  for (const f of checkBlanks(t.items)) findings.push(f);

    notRun.push.apply(notRun, CHECKS_WITHHELD);
  
  if (!t.cols.some((c) => c.role === 'hourly')) notRun.push(CHECKS_GIVEN[0]);

  findings.sort((x, y) => (x.line - y.line) || String(x.category).localeCompare(String(y.category)));
  const sumOf = (role) => round2(t.items.reduce((s, it) => {
    const n = normNumber(it.byRole[role]);
    return s + (n === null ? 0 : n);
  }, 0));

  const result = {
    findings,
    summary: {
      people: t.items.length,
      total: findings.length,
      p0: findings.filter((f) => f.level === 'P0').length,
      p1: findings.filter((f) => f.level === 'P1').length,
      wage_total: sumOf('wage'),
      overtime_hours_total: round2(sumOf('otNormal') + sumOf('otRest') + sumOf('otHoliday')),
      overtime_pay_total: sumOf('total'),
      basis: '小时工资 = 月工资 ÷ 计薪天数 ÷ 8；平时 1.5 倍、休息日 2 倍、法定节假日 3 倍；'
        + '合计行逐列复核。计薪天数缺省按法定 21.75。',
    },
    columns: t.cols.map((c) => c.header),
    checks_given: CHECKS_GIVEN,
    checks_withheld: CHECKS_WITHHELD,
    checks_executed: CHECKS_GIVEN,
    checks_out_of_scope: OUT_OF_SCOPE,
  };
  if (used.default) {
    result.assumptions = ['材料里没有「计薪天数」列，本次按法定月计薪天数 21.75 折算小时工资。'];
  }
  if (notRun.length) result.checks_not_run = notRun;
  if (findings.length === 0) {
    result.note = '本次实际执行的全部检查项都通过了。这只说明**这张表按上面写明的口径算得对**，'
      + '不代表考勤真实、也不代表加班经过审批 —— 那些不在本工具范围内。';
  }
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, splitRow, roleOf, normNumber, isBlank, round2, CHECKS_GIVEN, CHECKS_WITHHELD, CHECKS_OUT_OF_SCOPE: OUT_OF_SCOPE, SAMPLE_TEXT, LABELS, SUM_ROLES, MULT, LEGAL_BASE_DAYS,
};
