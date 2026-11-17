/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * iit-annual-settlement-check.js —— 个税年度汇算（综合所得）核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**有综合所得（工资薪金 + 劳务报酬）的自然人 / 代办的 HR、财务**，
 * 在**次年 3 月 1 日 ~ 6 月 30 日办理个税年度汇算**时，以及**汇算申报表报出之前**。
 * 要核的是"全年综合所得 − 各项扣除 = 应纳税所得额"、再按**年度七级超额累进税率表**算出
 * "全年应纳税额"，与"已预缴税额"相减得到"应补(退)税额"。这四步是一串**可手算复现**的勾稽：
 *
 *   应纳税所得额 = 全年工资薪金收入 + 全年劳务报酬收入
 *                  − 减除费用 − 专项扣除 − 专项附加扣除 − 其他扣除   （结果为负时按 0 处理）
 *   全年应纳税额 = 应纳税所得额 × 适用税率 − 速算扣除数
 *   应补(退)税额 = 全年应纳税额 − 已预缴税额
 *   合计行逐列 = 明细逐行相加（适用税率、速算扣除数**不参与**合计）
 *
 * ⚠️ 与「工资个税累计预扣核对」（月度累计预扣）**不是同一件事**：那个核的是**每月累计预扣**过程；
 *    本工具核的是**年度汇算**这一张表（全年综合所得、各项扣除、已预缴税额、应补/应退），
 *    也不判断专项附加扣除是否真实合规（那属于员工申报与税务核验）。
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**，
 * **不读环境变量**。
 */

/* ⛔ 顺序即优先级：**带限定语的列必须排在裸词前面**（本仓库踩过 6 次的坑）。
   若把裸词 `收入` / `税额` 排到前面，`全年工资薪金收入` 会被「收入」抢走、
   `全年应纳税额` 会被「税额」抢走 ⇒ 具体列的值被裸词列**覆盖**（算错但不会报缺列）。
   所以这里把 salary / labor / prepaid / settleAmount / taxPayable 全部排在 bareIncome / bareTax 之前；
   `专项扣除 / 专项附加扣除 / 其他扣除` 三个词互不为子串，各自独立成角色。 */
const ROLES = {
  empNo: ['员工编号', '员工号', '工号'],
  name: ['员工姓名', '姓名'],
  salary: ['全年工资薪金收入', '工资薪金收入', '工资薪金'],
  labor: ['全年劳务报酬收入', '劳务报酬收入', '劳务报酬'],
  basicDeduction: ['基本减除费用', '减除费用'],
  additionalDeduction: ['专项附加扣除', '专项附加'],
  specialDeduction: ['专项扣除', '三险一金'],
  otherDeduction: ['其他扣除'],
  taxableIncome: ['应纳税所得额', '计税所得额'],
  taxRate: ['适用税率', '税率'],
  quickDeduction: ['速算扣除数', '速算扣除'],
  prepaid: ['已预缴税额', '预缴税额', '已预缴'],
  settleAmount: ['应补退税额', '应补退'],
  taxPayable: ['全年应纳税额', '应纳税额', '应纳税'],
  /* ⛔ 裸词兜底只能放最后（排在它们前面的是所有带限定语的具体列）。 */
  bareIncome: ['收入'],
  bareTax: ['税额'],
};

const LABELS = {
  empNo: '员工编号', name: '姓名', salary: '全年工资薪金收入', labor: '全年劳务报酬收入',
  basicDeduction: '减除费用', specialDeduction: '专项扣除', additionalDeduction: '专项附加扣除',
  otherDeduction: '其他扣除', taxableIncome: '应纳税所得额', taxRate: '适用税率',
  quickDeduction: '速算扣除数', taxPayable: '全年应纳税额', prepaid: '已预缴税额',
  settleAmount: '应补(退)税额', bareIncome: '收入', bareTax: '税额',
};

const REQUIRED = ['empNo', 'name', 'salary', 'labor', 'basicDeduction', 'specialDeduction',
  'additionalDeduction', 'otherDeduction', 'taxableIncome', 'taxRate', 'quickDeduction',
  'taxPayable', 'prepaid', 'settleAmount'];

/* 参与合计行逐列复核的列：收入 / 各项扣除 / 应纳税所得额 / 应纳税额 / 已预缴 / 应补退。
   ⛔ `适用税率`（百分比）与 `速算扣除数`（分档定额）**不参与**合计 —— 相加没有意义。 */
const SUM_ROLES = ['salary', 'labor', 'basicDeduction', 'specialDeduction', 'additionalDeduction',
  'otherDeduction', 'taxableIncome', 'taxPayable', 'prepaid', 'settleAmount'];

const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.02;          // 收入/扣除/应纳税所得额/应补退的容差
const TOL_TAX = 0.05;      // 全年应纳税额（乘税率后）的容差

const CHECKS_GIVEN = [
  '合计行逐列复核（收入 / 各项扣除 / 应纳税所得额 / 应纳税额 / 已预缴 / 应补退；适用税率与速算扣除数不参与合计）',
  '同一员工编号重复行检测',
  '应纳税所得额勾稽（全年工资薪金 + 劳务报酬 − 减除费用 − 专项扣除 − 专项附加扣除 − 其他扣除，结果为负按 0 处理）',
  '全年应纳税额勾稽（应纳税所得额 × 适用税率 − 速算扣除数）',
  '应补(退)税额勾稽（全年应纳税额 − 已预缴税额）',
  '应纳税所得额为负检测（未按 0 处理）',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '适用税率与应纳税所得额不匹配（按 3%/10%/20%/25%/30%/35%/45% 七级超额累进速算表核对区间与速算扣除数）',
  '已预缴税额为负检测',
  '专项附加扣除超过 100000 提示（常见上限量级 60000~96000）',
  '全年收入为 0 但已预缴税额大于 0 提示（核对是否错列）',
  '应补退税额绝对值超过全年收入 20% 提示（异常量级）',
];

const OUT_OF_SCOPE = [
  '判断专项附加扣除、专项扣除是否**真实合规**（那是员工申报、扣缴义务人与税务核验的事）',
  '判断该不该办理年度汇算、该不该豁免（属于税收政策适用判断，也可能涉及免于汇算的情形）',
  '处理全年一次性奖金单独计税、离职补偿、外籍人员、经营所得等**特殊口径**',
  '代替申报系统做申报，也不出具税务意见或测算税负优化',
  '读取 .xlsx / 申报系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '员工编号\t姓名\t全年工资薪金收入\t全年劳务报酬收入\t减除费用\t专项扣除\t专项附加扣除\t其他扣除\t应纳税所得额\t适用税率\t速算扣除数\t全年应纳税额\t已预缴税额\t应补(退)税额',
  'E001\t张三\t180000.00\t0.00\t60000.00\t24000.00\t24000.00\t0.00\t72000.00\t10%\t2520.00\t4680.00\t4680.00\t0.00',
  'E002\t李四\t96000.00\t0.00\t60000.00\t12000.00\t0.00\t0.00\t24000.00\t3%\t0.00\t720.00\t720.00\t0.00',
  'E003\t王五\t300000.00\t0.00\t60000.00\t36000.00\t36000.00\t0.00\t168000.00\t20%\t16920.00\t16680.00\t16000.00\t680.00',
  '合计\t\t576000.00\t0.00\t180000.00\t72000.00\t60000.00\t0.00\t264000.00\t\t\t22080.00\t21400.00\t680.00',
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
  return s === '' || /^[-—–/]+$/.test(s) || /^(n\/?a|无|待填|待补|待定)$/i.test(s);
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
const num = (it, role) => normNumber(it[role]);
const who = (it) => {
  const no = String(it.empNo || '').trim();
  const nm = String(it.name || '').trim();
  if (no || nm) return `${no || '(未填编号)'}${nm ? '（' + nm + '）' : ''}`;
  return `第 ${it.line} 行`;
};

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: REQUIRED.slice(), header: [], cols: [], recognized: 0 };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const hasRole = (r) => cols.some((c) => c.role === r)
    || (r === 'salary' && cols.some((c) => c.role === 'bareIncome'))
    || (r === 'taxPayable' && cols.some((c) => c.role === 'bareTax'));
  const missingColumns = REQUIRED.filter((r) => !hasRole(r));
  const recognized = cols.filter((c) => c.role).length;
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => { if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i]; });
    if (row.salary === undefined && row.bareIncome !== undefined) row.salary = row.bareIncome;
    if (row.taxPayable === undefined && row.bareTax !== undefined) row.taxPayable = row.bareTax;
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header, cols, recognized };
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
        evidence: `合计=${stated}；明细合计=${sum}（${n} 行）`,
      });
    }
  }
  return out;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.empNo || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「员工编号」完全相同 —— 可能重复计入年度汇算`,
        evidence: `员工编号=${key}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/* 应纳税所得额 = 全年工资薪金 + 劳务报酬 − 减除费用 − 专项扣除 − 专项附加扣除 − 其他扣除；
   结果为负时按 0 处理（税法口径：综合所得年度应纳税所得额不为负），并在 evidence 里写明。 */
function checkTaxableIncome(it) {
  const v = ['salary', 'labor', 'basicDeduction', 'specialDeduction', 'additionalDeduction', 'otherDeduction', 'taxableIncome']
    .map((r) => num(it, r));
  if (v.some((x) => x === null)) return null;
  const [salary, labor, basic, special, additional, other, stated] = v;
  const raw = round2(salary + labor - basic - special - additional - other);
  const floored = round2(Math.max(0, raw));
  if (Math.abs(stated - floored) > TOL) {
    return {
      line: it.line, level: 'P0', category: '应纳税所得额勾稽',
      message: `${who(it)} 应纳税所得额填 ${stated}，但按「收入 − 各项扣除」应为 ${floored}（未按 0 处理前的计算值 ${raw}）`,
      evidence: `工资薪金=${salary}；劳务报酬=${labor}；减除费用=${basic}；专项扣除=${special}；`
        + `专项附加扣除=${additional}；其他扣除=${other}；原始计算值=${raw}`
        + `${raw < 0 ? '（结果为负，按 0 处理）' : ''}；应有应纳税所得额=${floored}；表内=${stated}`,
    };
  }
  return null;
}

/* 全年应纳税额 = 应纳税所得额 × 适用税率 − 速算扣除数（税率列写成 10% 或 10 都按百分数读） */
function checkTaxPayable(it) {
  const taxable = num(it, 'taxableIncome');
  const rate = num(it, 'taxRate');
  const quick = num(it, 'quickDeduction');
  const stated = num(it, 'taxPayable');
  if ([taxable, rate, quick, stated].some((x) => x === null)) return null;
  const expect = round2(Math.max(0, taxable) * (rate / 100) - quick);
  if (Math.abs(stated - expect) > TOL_TAX) {
    return {
      line: it.line, level: 'P0', category: '全年应纳税额勾稽',
      message: `${who(it)} 全年应纳税额填 ${stated}，但按 ${taxable} × ${rate}% − ${quick} 应为 ${expect}`,
      evidence: `应纳税所得额=${taxable}；适用税率=${rate}%；速算扣除数=${quick}；应有应纳税额=${expect}；表内=${stated}`,
    };
  }
  return null;
}

/* 应补(退)税额 = 全年应纳税额 − 已预缴税额（正数补税、负数退税） */
function checkSettleAmount(it) {
  const payable = num(it, 'taxPayable');
  const prepaid = num(it, 'prepaid');
  const stated = num(it, 'settleAmount');
  if ([payable, prepaid, stated].some((x) => x === null)) return null;
  const expect = round2(payable - prepaid);
  if (Math.abs(stated - expect) > TOL) {
    return {
      line: it.line, level: 'P0', category: '应补退税额勾稽',
      message: `${who(it)} 应补(退)税额填 ${stated}，但按 ${payable} − ${prepaid} 应为 ${expect}`,
      evidence: `全年应纳税额=${payable}；已预缴税额=${prepaid}；应有应补(退)税额=${expect}；表内=${stated}`,
    };
  }
  return null;
}

/* 表里直接填了负数应纳税所得额 ⇒ 没按 0 处理（P1，金额本身可能算对，但口径不对） */
function checkNegativeTaxable(it) {
  const taxable = num(it, 'taxableIncome');
  if (taxable === null || taxable >= 0) return null;
  return {
    line: it.line, level: 'P1', category: '应纳税所得额为负',
    message: `${who(it)} 应纳税所得额填 ${taxable}（负数）—— 年度综合所得应纳税所得额不足扣除时应按 0 处理`,
    evidence: `应纳税所得额=${taxable}；口径：结果为负时按 0 处理`,
  };
}

function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')}`,
      evidence: `表头=${header.join('|')}`,
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

/* ------------------------ 完整档（付费）追加检查项 ------------------------ */
/* ⚠️ 下面这些函数只在付费分支里被调用，免费包经 strip 后会被整体摘掉。
   ⛔ 注释里**不许**写出付费开关那一行的字面量：strip 的残渣断言是纯字符串包含判断。 */

/* ================================== 主流程 ================================== */

const COLUMN_HINT = '员工编号 / 姓名 / 全年工资薪金收入 / 全年劳务报酬收入 / 减除费用 / 专项扣除 / '
  + '专项附加扣除 / 其他扣除 / 应纳税所得额 / 适用税率 / 速算扣除数 / 全年应纳税额 / 已预缴税额 / 应补(退)税额';

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') return insufficient(['材料文本为空：请把个税年度汇算表（含表头）贴进来']);

  const parsed = parseTable(text);
  const { items, totals, missingColumns, header, recognized } = parsed;
  if (!recognized) {
    return insufficient([`认不出表头：第一行必须是表头（${COLUMN_HINT}）`]);
  }
  if (!items.length) {
    return insufficient(['没有明细行：至少需要一行员工数据（只有表头、或只有「合计」行时不给结论）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkTaxableIncome(it), checkTaxPayable(it), checkSettleAmount(it), checkNegativeTaxable(it)];
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
  const sumOf = (roles) => round2(items.reduce((n, it) => n
    + roles.reduce((m, r) => m + (normNumber(it[r]) || 0), 0), 0));

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
        checks_executed: checkList,
        checks_not_run: notRun,
        rows: items.length,
        income_total: sumOf(['salary', 'labor']),
        taxable_income_total: sumOf(['taxableIncome']),
        tax_payable_total: sumOf(['taxPayable']),
        prepaid_total: sumOf(['prepaid']),
        settle_total: sumOf(['settleAmount']),
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
