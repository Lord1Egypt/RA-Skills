/**
 * group-finance-monthly-selfcheck.js —— 集团财务月度自查包（free档；每个检查复用仓库里已有的免费引擎）
 *
 * 输入：分段文本，每段以 `=== 检查名 ===` 开头，例如
 *   === 银行流水对账 ===
 *   <把该检查要求的表贴进来>
 *
 * 自包含：只用 Node 标准库，不联网；材料不足**绝不给结论**。
 */
'use strict';
const ENGINES = {
  "集团内部往来对账与抵消核对": require('./parts/01.js'),
  "供应商应付对账": require('./parts/02.js'),
  "应收账款账龄核对": require('./parts/03.js'),
};

const BUNDLE_CHECKS = ["集团内部往来对账与抵消核对", "供应商应付对账", "应收账款账龄核对"];
const CHECKS_GIVEN = BUNDLE_CHECKS.map((c) => `${c}（分段核对）`);
const CHECKS_WITHHELD = ["应付账款账龄与付款计划核对", "部门费用预算执行核对"];
const OUT_OF_SCOPE = [
  '替代做账或出具鉴证意见（只做表内/表间算术与勾稽核对）',
  '读取 ERP/财务系统导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = "=== 集团内部往来对账与抵消核对 ===\n期间\t本方公司\t往来单位\t科目方向\t交易类型\t本方余额\t对方余额\t双方差额\t内部交易额\t抵消金额\n2026-01\t甲集团\t乙公司\t应收\t销售\t1000.00\t1000.00\t0.00\t1000.00\t1000.00\n2026-01\t乙公司\t甲集团\t应付\t采购\t1000.00\t1000.00\t0.00\t1000.00\t1000.00\n2026-02\t甲集团\t乙公司\t应收\t销售\t1000.00\t1000.00\t0.00\t1000.00\t1000.00\n2026-02\t乙公司\t甲集团\t应付\t采购\t1000.00\t1000.00\t0.00\t1000.00\t1000.00\n合计\t\t\t\t\t4000.00\t4000.00\t0.00\t4000.00\t4000.00\n\n=== 供应商应付对账 ===\n供应商\t期初应付\t本期采购\t本期付款\t期末应付\t对方对账金额\t差异\n甲物资有限公司\t100000.00\t50000.00\t30000.00\t120000.00\t120000.00\t0.00\n乙建材有限公司\t50000.00\t20000.00\t60000.00\t10000.00\t10000.00\t0.00\n丙设备有限公司\t0.00\t80000.00\t30000.00\t50000.00\t50000.00\t0.00\n合计\t150000.00\t150000.00\t120000.00\t180000.00\t180000.00\t0.00\n\n=== 应收账款账龄核对 ===\n客户\t期初余额\t本期应收\t本期收款\t期末余额\t0-30天\t31-60天\t61-90天\t90天以上\n甲客户\t100000.00\t50000.00\t30000.00\t120000.00\t60000.00\t40000.00\t20000.00\t0.00\n乙客户\t50000.00\t20000.00\t60000.00\t10000.00\t10000.00\t0.00\t0.00\t0.00\n丙客户\t0.00\t80000.00\t30000.00\t50000.00\t30000.00\t20000.00\t0.00\t0.00\n合计\t150000.00\t150000.00\t120000.00\t180000.00\t100000.00\t60000.00\t20000.00\t0.00";

function splitSections(text) {
  const out = {};
  let cur = null;
  for (const raw of String(text).split(/\r?\n/)) {
    const m = /^===\s*(.+?)\s*===$/.exec(raw.trim());
    if (m) { cur = m[1].trim(); out[cur] = []; continue; }
    if (cur) out[cur].push(raw);
  }
  const res = {};
  for (const k of Object.keys(out)) res[k] = out[k].join('\n').trim();
  return res;
}

function run(payload) {
  const text = payload && typeof payload.text === 'string' ? payload.text : '';

  if (text.trim().length < 5) {
    return { status: 'insufficient_input',
      missing: ['分段正文（每段以 === 检查名 === 开头）'],
      advice: '把要做核对的表按 `=== 检查名 ===` 分段贴进来；材料不足时本工具不给任何结论。' };
  }
  const secs = splitSections(text);
  const findings = [];
  const perCheck = [];
  for (const name of BUNDLE_CHECKS) {
    const body = secs[name];
    const engine = ENGINES[name];
    if (body === undefined) {          // 整段没给 ⇒ 如实标"缺这一段"
      perCheck.push({ check: name, status: 'missing_section', findings: 0 });
      continue;
    }
    const r = engine.run({ text: body });
    if (r.status !== 'success') {
      perCheck.push({ check: name, status: 'insufficient_input', findings: 0,
        missing: (r.missing || []).slice(0, 3) });
      continue;
    }
    const fs = (r.result.findings || []).map((f) => Object.assign({}, f, { check: name }));
    perCheck.push({ check: name, status: 'ok', findings: fs.length,
      p0: r.result.summary.p0, p1: r.result.summary.p1, p2: r.result.summary.p2 });
    findings.push.apply(findings, fs);
  }
  const p0 = findings.filter((f) => f.level === 'P0').length;
  const p1 = findings.filter((f) => f.level === 'P1').length;
  const p2 = findings.filter((f) => f.level === 'P2').length;
  const sectionsDone = perCheck.filter((c) => c.status === 'ok').length;
  const result = {
    status: 'success',
    service_type: 'FINANCE_MONTHLY_SELFCHECK',
    scope: {
      checks: CHECKS_GIVEN.slice(),
      checks_not_run: CHECKS_WITHHELD.slice(),
      sections_done: sectionsDone,
      rows: findings.length,
      periods: sectionsDone,
      executed_locally: true,
      network_used: false,
    },
    findings,
    per_check: perCheck,
    summary: {
      rows: findings.length, periods: sectionsDone,
      total: findings.length, p0, p1, p2,
      verdict: p0 > 0 ? 'ERROR_FOUND' : (findings.length ? 'NEEDS_REVIEW' : 'NO_ISSUE_FOUND'),
      omitted: 0,
    },
    checks_out_of_scope: OUT_OF_SCOPE,
    note: '本版本只执行：' + CHECKS_GIVEN.join('、') + '；未执行的检查项见 scope.checks_not_run。',
    disclaimer: '只核各段表内/表间的算术与勾稽，结论可由第三方用同一份输入复算；不替代鉴证与申报。',
  };

  return { status: 'success', result };
}

module.exports = { run, splitSections, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT };
