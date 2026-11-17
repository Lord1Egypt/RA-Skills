/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * non-recurring-gain-loss-check.js —— 非经常性损益与扣非净利润核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**上市公司 / 拟上市公司 / 集团合并报表的财务、审计与券商**，
 * 在**每个报告期编制「非经常性损益明细表」底稿、以及年报 / 中报披露"扣除非经常性损益后的净利润"之前**。
 * 底稿必须把每一笔非经常性损益逐项列示，并同时满足三组可手算复现的内部勾稽：
 *   ① 扣除所得税影响后金额 = 本期金额 − 涉及所得税影响
 *   ② 归属母公司 + 归属少数股东 = 扣除所得税影响后金额
 *   ③ 明细逐行相加 = 合计行（本期 / 上期 / 所得税影响 / 扣除后 / 归属母公司 / 归属少数股东 六列）
 * 这三个等式一旦对不上，"扣非净利润"就会被审核与券商追问；本工具把等式变成机械判据。
 *
 * ⚠️ 本工具**不判断**某笔收支**实质上**是否属于非经常性损益（那是会计判断，须在底稿逐项说明），
 *    也不替代审计程序、不出具任何鉴证意见。
 *
 * 免费档执行 7 项；完整档（付费）追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 http / https / net / dns / tls 模块），**不写任何文件**、**不读环境变量**。
 */

/* ⛔ 顺序即优先级：**带限定语的列必须排在裸词前面**（本仓库踩过 6 次的坑）。
   ① `扣除所得税影响后金额` 里含 `所得税影响` ⇒ 若 `taxImpact` 排在前面，这一列会被抢走；
   ② `本期金额` / `上期金额` 里含 `金额` ⇒ 裸词 `金额` 必须排在这两列**之后**；
   ③ `项目类别` 里含 `项目` ⇒ `category` 必须排在 `item` 前面。
   顺序一错的表现是"跑起来不报错，只是**某列永远认不出来 / 被别的列覆盖**"（`header_map_check` 会拦）。 */
const ROLES = {
  category: ['项目类别', '类别', '损益类别'],
  item: ['项目名称', '项目'],
  amountCur: ['本期金额', '本期发生额', '本期数'],
  amountPrev: ['上期金额', '上期发生额', '上期数'],
  afterTax: ['扣除所得税影响后金额', '扣除所得税影响后', '扣非后金额'],
  taxImpact: ['涉及所得税影响', '所得税影响额', '所得税影响'],
  isNonRec: ['是否非经常性', '是否属于非经常性', '非经常性标识'],
  note: ['说明', '备注', '附注'],
  parentShare: ['归属母公司', '归属于母公司', '归母金额'],
  minorityShare: ['归属少数股东', '归属于少数股东', '少数股东金额'],
  amount: ['金额'],
};

const LABELS = {
  category: '类别', item: '项目',
  amountCur: '本期金额', amountPrev: '上期金额',
  afterTax: '扣除所得税影响后金额', taxImpact: '涉及所得税影响',
  isNonRec: '是否非经常性', note: '说明',
  parentShare: '归属母公司', minorityShare: '归属少数股东',
  amount: '金额',
};

/* 必需列：缺**个别**列时照常给结论并报「列缺失」；只有一列都认不出来 / 没有明细行才不给结论。
   ⚠️ 裸词 `金额` 不在必需列里 —— 它是兜底角色，样例表里本来就没有这一列。 */
const REQUIRED = ['item', 'category', 'amountCur', 'amountPrev', 'isNonRec', 'note',
  'taxImpact', 'afterTax', 'parentShare', 'minorityShare'];
const SUM_ROLES = ['amountCur', 'amountPrev', 'taxImpact', 'afterTax', 'parentShare', 'minorityShare'];
const TOTAL_WORDS = /^(合计|总计|小计|合计数?)$/;
const TOL = 0.02;
/* 「大额非经常性项目」的可复核口径：本期金额绝对值 ≥ 10 万元。取整数是因为它只是提示阈值，
   写死在代码里比读配置更可复核（本工具不读环境变量、不读配置文件）。 */
const BIG_NONREC = 100000;

const CHECKS_GIVEN = [
  '合计行逐列复核（本期金额 / 上期金额 / 所得税影响 / 扣除所得税影响后金额 / 归属母公司 / 归属少数股东 —— 明细逐行相加 = 合计）',
  '同一「项目 + 类别」重复行检测',
  '扣除所得税影响后金额 = 本期金额 − 涉及所得税影响',
  '归属母公司 + 归属少数股东 = 扣除所得税影响后金额',
  '类别与「是否非经常性」口径矛盾检测（非经常性损益却填"否"，或反之）',
  '非经常性项目未写说明 / 说明为占位符检测',
  '空白与占位符检测（含必需列缺失）',
];

const CHECKS_WITHHELD = [
  '非经常性口径不一致的统计：行数、金额合计、占扣除所得税影响后总额比例 > 50% 提示',
  '涉及所得税影响为负（所得税冲回）检测 —— 须写清冲回依据',
  '归属少数股东不为 0 但归属母公司等于扣除后全额（母公司与少数股东未拆分）检测',
  '上期金额全部为 0 但本期有大额非经常性项目（上期可比性待核）提示',
  '非经常性金额超过本期金额 100%（绝对值口径）提示',
];

const OUT_OF_SCOPE = [
  '判断某笔收支**实质上**是否属于非经常性损益（是否与主营业务无关、是否具有可持续性属于会计判断）',
  '代替审计抽凭程序，也不出具审计或鉴证意见',
  '核对政府补助批文、股权处置协议、判决书等**原始凭据的真伪**，或与业务系统的逐行明细比对',
  '读取 ERP / 合并报表系统的导出文件（需要你先导出成文本贴进来）',
  '计算"扣非净利润"本身（净利润的取数口径、少数股东损益的分摊比例属于报表编制判断）',
];

const SAMPLE_TEXT = [
  '项目\t类别\t本期金额\t上期金额\t是否非经常性\t说明\t涉及所得税影响\t扣除所得税影响后金额\t归属母公司\t归属少数股东',
  '政府补助（与收益相关）\t非经常性损益\t500000\t300000\t是\t与日常经营无关的财政奖励\t125000\t375000\t375000\t0',
  '处置固定资产净收益\t非经常性损益\t200000\t0\t是\t处置一台旧设备\t50000\t150000\t150000\t0',
  '同一控制下企业合并当期净损益\t非经常性损益\t100000\t0\t是\t合并子公司当期净损益\t0\t100000\t80000\t20000',
  '合计\t\t800000\t300000\t\t\t175000\t625000\t605000\t20000',
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
  return s === '' || /^[-—–]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|略)$/i.test(s);
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

function round2(n) { return Math.round(n * 100) / 100; }

function who(it) {
  const name = String(it.item === undefined || it.item === null ? '' : it.item).trim();
  return name ? `${name}（第 ${it.line} 行）` : `第 ${it.line} 行`;
}

/* 「是否非经常性」这一列的取值很脏（是 / Y / 空），类别列反而是稳定口径 ⇒ 两者取或。 */
function isNonRecRow(it) {
  const flag = String(it.isNonRec === undefined || it.isNonRec === null ? '' : it.isNonRec).trim();
  if (flag === '是' || flag === 'Y' || flag === 'y') return true;
  return String(it.category === undefined || it.category === null ? '' : it.category).indexOf('非经常性') >= 0;
}

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

function checkAfterTaxEquation(it) {
  const cur = normNumber(it.amountCur);
  const tax = normNumber(it.taxImpact);
  const after = normNumber(it.afterTax);
  if (cur === null || tax === null || after === null) return null;
  const expect = round2(cur - tax);
  if (Math.abs(expect - after) > TOL) {
    return {
      line: it.line, level: 'P0', category: '扣除所得税影响后金额不平',
      message: `${who(it)}「扣除所得税影响后金额」填 ${after}，但 本期金额 ${cur} − 涉及所得税影响 ${tax} = ${expect}`,
      evidence: `本期金额=${cur}；涉及所得税影响=${tax}；应为=${expect}；实填=${after}；差异=${round2(after - expect)}`,
    };
  }
  return null;
}

function checkParentMinorityEquation(it) {
  const after = normNumber(it.afterTax);
  const parent = normNumber(it.parentShare);
  const minority = normNumber(it.minorityShare);
  if (after === null || parent === null || minority === null) return null;
  const sum = round2(parent + minority);
  if (Math.abs(sum - after) > TOL) {
    return {
      line: it.line, level: 'P0', category: '归属母公司与少数股东不平',
      message: `${who(it)} 归属母公司 ${parent} + 归属少数股东 ${minority} = ${sum}，但「扣除所得税影响后金额」是 ${after}`,
      evidence: `归属母公司=${parent}；归属少数股东=${minority}；两者合计=${sum}；扣除所得税影响后金额=${after}；差异=${round2(sum - after)}`,
    };
  }
  return null;
}

/* 口径矛盾只在**类别列本身给出了经常性/非经常性定性**时才报 ——
   类别可能用别的科目体系（如"资产处置损益"），那时不构成矛盾，不能误报。 */
function checkNonRecFlagVsCategory(it) {
  const cat = String(it.category === undefined || it.category === null ? '' : it.category).trim();
  const flag = String(it.isNonRec === undefined || it.isNonRec === null ? '' : it.isNonRec).trim();
  if (cat === '' || (flag !== '是' && flag !== '否')) return null;
  const saysNonRec = cat.indexOf('非经常性') >= 0;
  const saysRec = !saysNonRec && cat.indexOf('经常性') >= 0;
  if ((saysNonRec && flag === '否') || (saysRec && flag === '是')) {
    return {
      line: it.line, level: 'P1', category: '非经常性口径矛盾',
      message: `${who(it)} 类别填「${cat}」，但「是否非经常性」填「${flag}」—— 口径互相矛盾，扣非口径无法确认`,
      evidence: `类别=${cat}；是否非经常性=${flag}`,
    };
  }
  return null;
}

function checkNonRecNote(it) {
  if (!isNonRecRow(it)) return null;
  if (!isBlank(it.note)) return null;
  return {
    line: it.line, level: 'P1', category: '非经常性项目未写说明',
    message: `${who(it)} 被列为非经常性损益，但「${LABELS.note}」是空白或占位符 —— 非经常性项目必须逐项说明依据`,
    evidence: `${LABELS.note}=${it.note === undefined || it.note === '' ? '(空)' : it.note}`,
  };
}

function checkTotalRow(items, totals) {
  if (!totals || !totals.row) return [];
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
        line: totals.line, level: 'P1', category: '合计行复核',
        message: `合计行「${LABELS[role]}」填 ${stated}，但 ${n} 行明细逐行相加是 ${sum}`,
        evidence: `合计=${stated}；明细合计=${sum}；参与相加的明细行数=${n}；差异=${round2(stated - sum)}`,
      });
    }
  }
  return out;
}

function checkDuplicate(items) {
  const seen = new Map();
  const out = [];
  for (const it of items) {
    const name = String(it.item === undefined || it.item === null ? '' : it.item).trim();
    const cat = String(it.category === undefined || it.category === null ? '' : it.category).trim();
    if (name === '' && cat === '') continue;
    const key = `${name}|${cat}`;
    if (seen.has(key)) {
      out.push({
        line: it.line, level: 'P1', category: '重复行',
        message: `${who(it)} 与第 ${seen.get(key)} 行的「项目 + 类别」完全相同 —— 可能重复列示、重复扣减`,
        evidence: `项目=${name}；类别=${cat}；与第 ${seen.get(key)} 行重复`,
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/* 「说明」不在这里扫：经常性项目的说明本来就可以空着，它的空白／占位符由
   checkNonRecNote 只对**非经常性**行报，避免同一行被报两次。 */
function checkBlanks(header, items, missingColumns) {
  const out = [];
  if (missingColumns.length) {
    out.push({
      line: 1, level: 'P1', category: '列缺失',
      message: `表头缺少必需列：${missingColumns.map((r) => LABELS[r]).join('、')} —— 缺的列无法核对，其余列照常给出结论`,
      evidence: `表头=${header.join('|')}；缺少=${missingColumns.join('、')}`,
    });
  }
  for (const it of items) {
    for (const role of REQUIRED) {
      if (role === 'note') continue;
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
  if (text.trim() === '') {
    return insufficient(['材料文本为空：请把「非经常性损益明细表」（含表头）贴进来']);
  }

  const { items, totals, missingColumns, header } = parseTable(text);
  if (!items.length) {
    return insufficient(['认不出任何数据行：第一行必须是表头，且至少有一行明细（合计行可以留）']);
  }
  if (missingColumns.length === REQUIRED.length) {
    return insufficient([
      '认不出表头：请保留「项目 / 类别 / 本期金额 / 上期金额 / 是否非经常性 / 说明 / 涉及所得税影响 / 扣除所得税影响后金额 / 归属母公司 / 归属少数股东」这些列名',
      `当前读到的表头：${header.join(' / ')}`,
    ]);
  }

  const findings = [];
  for (const f of checkTotalRow(items, totals)) findings.push(f);
  for (const it of items) {
    const one = [checkAfterTaxEquation(it), checkParentMinorityEquation(it), checkNonRecFlagVsCategory(it)];
    for (const f of one) if (f) findings.push(f);
  }
  if (missingColumns.indexOf('note') < 0) {
    for (const it of items) {
      const f = checkNonRecNote(it);
      if (f) findings.push(f);
    }
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
        p0,
        p1,
        p2,
        verdict: findings.length === 0 ? 'NO_ISSUE_FOUND' : (p0 > 0 ? 'P0_ISSUES' : 'ISSUES'),
        omitted: 0,
      },
      scope: {
        checks: checkList,
        checks_not_run: notRun,
        rows: items.length,
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
