/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * goodwill-impairment-check.js —— 商誉减值测试底稿核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**有商誉（非同一控制下企业合并形成）的公司**，
 * 在**每年年度终了做商誉减值测试、以及年审提供减值测试底稿之前**。
 * 会计与评估要把每个资产组的「商誉 + 可辨认净资产 = 资产组账面价值」与可收回金额比一遍，
 * 算出减值损失（先冲商誉），并逐行维护「商誉减值 / 本期商誉净额」这几列；
 * 审计盯的就是它们能不能**逐行对上**。
 *
 * 核心可算关系（都能手算复现）：
 *   资产组账面价值 = 商誉账面价值 + 可辨认净资产账面价值
 *   减值损失       = max(0, 资产组账面价值 − 可收回金额)
 *   商誉减值       ≤ 商誉账面价值（不能超冲商誉）
 *   本期商誉净额   = 商誉账面价值 − 商誉减值
 *   合计行各列     = 明细行逐列相加
 *
 * 免费档执行 7 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**资产组怎么划分、商誉怎么分摊、可收回金额该用哪种口径（那属于会计与评估判断）。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls），**不写任何文件**。
 */

/* ⛔ 顺序即优先级：**更具体的词必须排在更宽泛的词前面**。
   `资产组账面价值合计` 里含 `资产组`/`账面价值`；`商誉账面价值` 里含 `账面价值`
   ⇒ 宽泛的键排前面会把这两列抢走（本仓库踩过 6 次）。 */
const ROLES = {
  group: ['资产组名称', '所属资产组'],
  goodwill: ['商誉账面价值', '分摊后商誉', '商誉原值'],
  netAssets: ['可辨认净资产账面价值', '可辨认净资产'],
  carrying: ['资产组账面价值合计', '资产组账面价值', '账面价值合计'],
  recoverable: ['可收回金额', '可回收金额'],
  impairment: ['减值损失', '本期减值损失', '减值金额'],
  goodwillImpairment: ['商誉减值', '其中商誉减值', '商誉减值金额'],
  goodwillNet: ['本期商誉净额', '商誉净额', '本期商誉余额'],
  method: ['测试方法', '减值测试方法', '估值方法'],
};

const LABELS = {
  group: '资产组名称', goodwill: '商誉账面价值', netAssets: '可辨认净资产账面价值',
  carrying: '资产组账面价值合计', recoverable: '可收回金额', impairment: '减值损失',
  goodwillImpairment: '商誉减值', goodwillNet: '本期商誉净额', method: '测试方法',
};

const REQUIRED = ['goodwill', 'netAssets', 'carrying', 'recoverable', 'impairment', 'goodwillImpairment', 'goodwillNet'];
const SUM_ROLES = ['goodwill', 'netAssets', 'carrying', 'recoverable', 'impairment', 'goodwillImpairment', 'goodwillNet'];
const TEST_METHODS = ['现金流折现', '预计未来现金流量', '公允价值减处置费用', '公允价值减去处置费用', '市场法', '收益法'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.01;
/* ⚠️ 付费开关**只声明一次**（形态 B，且必须是 `Boolean(...)` 这一种写法）：
   `strip_free_engine` 按「`const paid` + `Boolean(`」这一行识别并摘掉付费语句；
   写成别的形式（例：数组的 `.some()`）会**留下开关不删** ⇒ 泄漏守卫报"免费引擎里仍留着付费开关"。
   ⛔ 注释里也**不要**写出那一行的字面量：`strip` 的残渣断言是**纯字符串包含**判断，
      写了字面量就会被当成"没删干净"而整包跳过（本轮实测踩到）。
   两个形态（MARKER + 开关）同时出现会把免费检查也整块删掉（第 236 轮踩过）。 */

const CHECKS_GIVEN = [
  '合计行逐列复核（明细逐行相加 = 合计）',
  '同一资产组重复行检测',
  '资产组账面价值 = 商誉账面价值 + 可辨认净资产账面价值',
  '减值损失 = max(0, 资产组账面价值 − 可收回金额)',
  '商誉减值 ≤ 商誉账面价值（不能超冲商誉）',
  '本期商誉净额 = 商誉账面价值 − 商誉减值',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '减值损失小于商誉减值（先冲商誉的顺序错了）检测',
  '本期商誉净额为负检测',
  '可收回金额为负检测',
  '账面价值 > 可收回金额却未计提减值（漏提）检测',
  '减值测试方法不在常见口径（收益法/市场法/公允价值减处置费用等）提示',
];

const OUT_OF_SCOPE = [
  '判断资产组怎么划分、商誉怎么分摊（属于会计判断，须与审计/评估沟通）',
  '判断可收回金额该用现金流折现还是公允价值减处置费用，也不核折现率、增长率假设是否合理',
  '出具减值测试的审计或鉴证意见，或判断减值要不要确认递延所得税',
  '读取评估报告 / 财务系统 / 估值模型的原始文件（需要你先导出成文本贴进来）',
  '判断商誉减值在税法上能否税前扣除（属于税务判断）',
];

const SAMPLE_TEXT = [
  '资产组名称\t商誉账面价值\t可辨认净资产账面价值\t资产组账面价值合计\t可收回金额\t减值损失\t商誉减值\t本期商誉净额\t测试方法',
  '豫州智能装备资产组\t5000000.00\t20000000.00\t25000000.00\t26000000.00\t0.00\t0.00\t5000000.00\t预计未来现金流量折现',
  '中岳新材料资产组\t3000000.00\t12000000.00\t15000000.00\t13500000.00\t1500000.00\t1500000.00\t1500000.00\t预计未来现金流量折现',
  '合计\t8000000.00\t32000000.00\t40000000.00\t39500000.00\t1500000.00\t1500000.00\t6500000.00\t',
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
const who = (it) => String(it.group || '').trim() || `第 ${it.line} 行`;

function parseTable(text) {
  const lines = String(text).split(/\r?\n/).map((l) => l.trim()).filter((l) => l !== '');
  if (!lines.length) return { items: [], totals: {}, missingColumns: [], header: [] };
  const header = splitRow(lines[0]);
  const cols = header.map((h, i) => ({ i, role: roleOf(h), raw: h }));
  const missingColumns = REQUIRED.filter((r) => !cols.some((c) => c.role === r));
  const items = [];
  const totals = {};
  for (let li = 1; li < lines.length; li += 1) {
    const cells = splitRow(lines[li]);
    const row = { line: li + 1 };
    cols.forEach((c) => { if (c.role) row[c.role] = cells[c.i] === undefined ? '' : cells[c.i]; });
    const label = (cells[0] || '').replace(/\s/g, '');
    if (TOTAL_WORDS.test(label)) { totals.line = li + 1; totals.row = row; continue; }
    items.push(row);
  }
  return { items, totals, missingColumns, header };
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

function checkCarrying(it) {
  const gw = normNumber(it.goodwill);
  const net = normNumber(it.netAssets);
  const carry = normNumber(it.carrying);
  if (gw === null || net === null || carry === null) return null;
  const want = round2(gw + net);
  if (Math.abs(want - carry) > TOL) {
    return {
      line: it.line, level: 'P0', category: '资产组账面价值不等于商誉加可辨认净资产',
      message: `${who(it)} 资产组账面价值合计 ${carry} ≠ 商誉 ${gw} + 可辨认净资产 ${net} = ${want}`,
      evidence: `商誉账面价值=${gw}；可辨认净资产=${net}；账面价值合计=${carry}；应为 ${want}`,
    };
  }
  return null;
}

function checkImpairmentFormula(it) {
  const carry = normNumber(it.carrying);
  const rec = normNumber(it.recoverable);
  const imp = normNumber(it.impairment);
  if (carry === null || rec === null || imp === null) return null;
  const want = round2(Math.max(0, carry - rec));
  if (Math.abs(want - imp) > TOL) {
    return {
      line: it.line, level: 'P0', category: '减值损失与账面/可收回金额不符',
      message: `${who(it)} 减值损失 ${imp} ≠ max(0, 账面价值 ${carry} − 可收回金额 ${rec}) = ${want}`,
      evidence: `资产组账面价值=${carry}；可收回金额=${rec}；减值损失=${imp}；应为 ${want}`,
    };
  }
  return null;
}

function checkGoodwillImpairmentCap(it) {
  const gw = normNumber(it.goodwill);
  const gwi = normNumber(it.goodwillImpairment);
  if (gw === null || gwi === null) return null;
  if (gwi - gw > TOL) {
    return {
      line: it.line, level: 'P0', category: '商誉减值超过商誉账面价值',
      message: `${who(it)} 商誉减值 ${gwi} > 商誉账面价值 ${gw} —— 商誉不能被超冲（超出部分应分摊到其他资产）`,
      evidence: `商誉账面价值=${gw}；商誉减值=${gwi}；超出=${round2(gwi - gw)}`,
    };
  }
  return null;
}

function checkGoodwillNet(it) {
  const gw = normNumber(it.goodwill);
  const gwi = normNumber(it.goodwillImpairment);
  const net = normNumber(it.goodwillNet);
  if (gw === null || gwi === null || net === null) return null;
  const want = round2(gw - gwi);
  if (Math.abs(want - net) > TOL) {
    return {
      line: it.line, level: 'P0', category: '本期商誉净额不符',
      message: `${who(it)} 本期商誉净额 ${net} ≠ 商誉账面价值 ${gw} − 商誉减值 ${gwi} = ${want}`,
      evidence: `商誉账面价值=${gw}；商誉减值=${gwi}；本期商誉净额=${net}；应为 ${want}`,
    };
  }
  return null;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const key = String(it.group || '').trim();
    if (!key) continue;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「资产组名称」完全相同 —— 可能重复计入`,
        evidence: `资产组名称=${it.group}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
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

/* ============================== 完整档（付费）检查项 ============================== */

/* ================================== 主流程 ================================== */

function run(payload) {
  const p = payload || {};
  const text = p.text === undefined || p.text === null ? '' : String(p.text);
  if (text.trim() === '') return insufficient(['材料文本为空：请把商誉减值测试底稿（含表头）贴进来']);

  const { items, totals, missingColumns, header } = parseTable(text);
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（合计行可留）']);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkCarrying(it), checkImpairmentFormula(it), checkGoodwillImpairmentCap(it), checkGoodwillNet(it)];
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
        checks_not_run: notRun,
        rows: items.length,
        goodwill_total: round2(items.reduce((n, it) => n + (normNumber(it.goodwill) || 0), 0)),
        impairment_total: round2(items.reduce((n, it) => n + (normNumber(it.impairment) || 0), 0)),
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
