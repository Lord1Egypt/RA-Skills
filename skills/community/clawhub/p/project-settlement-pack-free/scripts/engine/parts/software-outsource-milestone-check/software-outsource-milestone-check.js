'use strict';
/**
 * software-outsource-milestone-check.js —— 软件外包里程碑验收与付款核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**软件公司 / 系统集成商每个月给外包方付款之前**。
 * 外包合同是按里程碑付钱的（合同签订 30%、需求确认 20%、上线验收 40%…），
 * 每一笔都要同时回答三个问题：**这个里程碑到底验收了没有、这一笔该付多少、质保金扣了没有**。
 * 这张表填错，方向只有两个 —— **付早了**（没验收就付款，质量压不住、返工没人管）或
 * **付少了 / 付重了**（外包方停工，或者同一里程碑被付了两次追不回来）。
 * 两条都会在月度资金计划、项目成本归集与审计抽样上暴露出来。
 *
 * 好消息是：这张表每一格都能手算复现，所以"对不对"完全可以机械核出来：
 *
 *   本期应付 = 里程碑金额 × 付款比例
 *   累计已付 = 前期已付 + 本期应付
 *   合计行各列 = 明细行相加（合同总额按合同去重、里程碑金额按里程碑去重，
 *               同一合同的同一里程碑只算一次，否则会被重复加总）
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**该里程碑算不算交付完成、质保金该不该扣、该扣多少（那属于合同与验收判断）：
 *    表里给的合同总额、里程碑金额、付款比例、合同质保金比例、验收状态一律**以你填的为准**，
 *    本工具只核表内勾稽与档位口径，并把可疑处按原文行号列出来。
 *
 * ⚠️ 完整档（付费）检查项用**形态 B**：先把入参里的档位开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的带花括号的块（**不要**留「完整档才执行的检查」那类整块注释标记——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关或条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成"没删干净"而整包回滚（第 236 轮实测连续踩了两次）。
 * * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。

 * 契约：parseTable / roleOf / normNumber / round2 / CHECKS_GIVEN / CHECKS_WITHHELD /
 *       OUT_OF_SCOPE / SAMPLE_TEXT 一律照原样导出，免费包与完整档共用同一份源码。
 */

const CHECKS_GIVEN = [
  '本期应付复算（里程碑金额 × 付款比例 = 本期应付）',
  '累计已付复算（前期已付 + 本期应付 = 累计已付）',
  '合计行逐列复核',
  '同一里程碑重复行检测',
  '空白与占位符检测',
  '金额为负检测',
];

const CHECKS_WITHHELD = [
  '累计已付超过合同总额提示（付超合同）',
  '未验收却已付款提示（验收状态与已付款额矛盾）',
  '质保金比例与合同不符提示',
  '付款比例合计不等于 100% 提示（里程碑没付完 / 比例填错）',
  '同一里程碑重复付款提示（同一里程碑被付了两次）',
];

const OUT_OF_SCOPE = [
  '判断某个里程碑到底算不算"已交付、已验收"（交付物是否齐全、验收标准是否达成，属于合同与验收判断，请以验收单与合同约定为准）',
  '判断质保金该不该扣、该扣多少、什么时候退（质保期与退还条件属于合同条款判断）',
  '核对外包合同条款本身（税率、发票、违约金、变更签证、汇率）对付款金额的影响',
  '处理付款的会计科目、预付款冲抵、进项税抵扣与资金计划审批',
  '读取 ERP / 项目管理系统 / 网银导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t外包方\t外包合同编号\t合同总额\t里程碑名称\t里程碑金额\t付款比例\t本期应付\t前期已付\t累计已付\t验收状态\t合同质保金比例\t质保金比例',
  '2026-01\t蓝海软件\tHT-2026-101\t900000.00\t需求与设计确认\t300000.00\t90%\t270000.00\t0.00\t270000.00\t已验收\t10%\t10%',
  '2026-02\t蓝海软件\tHT-2026-101\t900000.00\t开发与联调完成\t400000.00\t90%\t360000.00\t270000.00\t630000.00\t已验收\t10%\t10%',
  '2026-03\t蓝海软件\tHT-2026-101\t900000.00\t上线与终验\t200000.00\t90%\t180000.00\t630000.00\t810000.00\t已验收\t10%\t10%',
  '2026-02\t天翼集成\tHT-2026-102\t500000.00\t原型与需求确认\t200000.00\t95%\t190000.00\t0.00\t190000.00\t已验收\t5%\t5%',
  '2026-03\t天翼集成\tHT-2026-102\t500000.00\t系统验收与交付\t300000.00\t95%\t285000.00\t190000.00\t475000.00\t已验收\t5%\t5%',
  '合计\t\t\t1400000.00\t\t1400000.00\t\t1285000.00\t1090000.00\t2375000.00\t\t\t',
].join('\n');

const TOL = 0.01;             // 金额容差：1 分
const RATIO_TOL = 0.0005;     // 比例容差：0.05 个百分点

const ROLES = {
  // ⚠️ 顺序即优先级：更具体的别名在前
  //    （「所属期间」不能被「期间」抢走、「外包合同编号」不能被「外包方」抢走、
  //     「里程碑金额」不能被「里程碑」抢走、「合同质保金比例」不能被「质保金比例」抢走、
  //     「前期累计已付」不能被「累计已付」抢走 —— 抢走的后果是**算错但不报缺列**）
  period: ['所属期间', '会计期间', '付款期间', '结算期间', '所属月份', '期间', '月份'],
  vendor: ['外包方名称', '外包单位名称', '供应商名称', '外包方', '外包单位', '供应商', '承包方', '乙方'],
  contract: ['外包合同编号', '外包合同号', '合同编号', '合同号', '协议编号'],
  contractAmount: ['外包合同总额', '合同总额', '合同总金额', '合同金额', '合同价款'],
  milestoneAmount: ['里程碑结算金额', '里程碑金额', '节点金额', '阶段金额', '本期里程碑金额'],
  milestone: ['里程碑名称', '里程碑编号', '里程碑节点', '里程碑', '交付节点', '阶段名称', '节点名称'],
  payRatio: ['本期付款比例', '里程碑付款比例', '本期支付比例', '付款比例', '支付比例', '付款比率'],
  payDue: ['本期应付金额', '本期应付', '本期付款金额', '本期支付金额', '应付金额', '本次应付'],
  paidBefore: ['前期累计已付', '上期累计已付', '前期已付金额', '前期已付', '上期已付', '期初已付', '前期付款'],
  paidCum: ['累计已付金额', '累计已付', '累计付款金额', '累计支付金额', '累计支付'],
  accepted: ['验收状态', '验收结论', '验收情况', '是否验收', '验收标志', '验收'],
  retentionContract: ['合同质量保证金比例', '合同质保金比例', '合同质保比例', '合同保留金比例'],
  retentionRatio: ['质量保证金比例', '质保金扣留比例', '质保金比例', '质保比例', '保留金比例', '质保金率'],
};

const LABELS = {
  period: '所属期间', vendor: '外包方', contract: '外包合同编号', contractAmount: '合同总额',
  milestone: '里程碑名称', milestoneAmount: '里程碑金额', payRatio: '付款比例', payDue: '本期应付',
  paidBefore: '前期已付', paidCum: '累计已付', accepted: '验收状态',
  retentionContract: '合同质保金比例', retentionRatio: '质保金比例',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'vendor', 'contract', 'contractAmount', 'milestone', 'milestoneAmount',
  'payRatio', 'payDue', 'paidBefore', 'paidCum', 'accepted', 'retentionContract', 'retentionRatio'];
/** 合计行逐列复核的列 */
const SUM_ROLES = ['contractAmount', 'milestoneAmount', 'payDue', 'paidBefore', 'paidCum'];
/**
 * 这几列是"按对象"的口径，合计行不能简单相加：
 *   · 合同总额 —— 同一合同的多行里它是**同一个数**，只算一次；
 *   · 里程碑金额 —— 同一里程碑分次付款时它会重复出现，按里程碑去重后只算一次。
 */
const DEDUPE_ROLES = { contractAmount: 'contract', milestoneAmount: 'milestone' };
/**
 * 免费档负值检测覆盖的列：**合同与付款侧的金额**。
 * ⚠️ 刻意**不含**付款比例 / 质保金比例 —— "比例合计算不算付超、质保金比例与合同是否一致"
 *    是完整档的独立检查项（见 CHECKS_WITHHELD），免费档提前报出比例类结论就等于把付费结论送出去了。
 */
const NEGATIVE_ROLES = ['contractAmount', 'milestoneAmount', 'payDue', 'paidBefore', 'paidCum'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|汇总|累计|合计：)$/;

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

/** 比例归一化成小数：`90%` ⇒ 0.9；`0.9` ⇒ 0.9；`90` ⇒ 0.9 */
function rateValue(raw) {
  if (isBlank(raw)) return null;
  const s = String(raw).trim();
  const n = normNumber(s);
  if (n === null) return null;
  if (s.indexOf('%') >= 0) return n / 100;
  return Math.abs(n) > 1 ? n / 100 : n;
}

const round2 = (n) => Math.round(n * 100) / 100;
const round4 = (n) => Math.round(n * 10000) / 10000;

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
  const n = [it && it.milestone, it && it.vendor]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

const contractKeyOf = (it) => {
  const c = it && it.contract !== undefined ? String(it.contract).trim() : '';
  return c || `第 ${it && it.line} 行`;
};

/** 里程碑键：同一合同下的同一里程碑才算同一个里程碑（不同合同的同名里程碑互不相干） */
const milestoneKeyOf = (it) => {
  const m = it && it.milestone !== undefined ? String(it.milestone).trim() : '';
  return `${contractKeyOf(it)}|${m || `第 ${it && it.line} 行`}`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

function checkPayableRecompute(it) {
  const out = [];
  const amount = normNumber(it.milestoneAmount);
  const ratio = rateValue(it.payRatio);
  const stated = normNumber(it.payDue);
  if (amount === null || ratio === null || stated === null) return out;
  if (ratio < 0) return out;                    // 比例为负：付费档才报比例类结论，免费档不越权
  const expect = round2(amount * ratio);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '本期应付复算不符', line: it.line,
    message: `${who(it)}：里程碑金额 ${amount.toFixed(2)} × 付款比例 ${(ratio * 100).toFixed(2)}% = ${expect.toFixed(2)}，`
      + `表里「本期应付」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '里程碑付款就是"这个里程碑值多少钱 × 这次付它的百分之几"：付多了压不住后面的里程碑，付少了外包方会停工。',
  });
  return out;
}

function checkPaidCumulative(it) {
  const out = [];
  const before = normNumber(it.paidBefore);
  const due = normNumber(it.payDue);
  const stated = normNumber(it.paidCum);
  if (before === null || due === null || stated === null) return out;
  const expect = round2(before + due);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '累计已付复算不符', line: it.line,
    message: `${who(it)}：前期已付 ${before.toFixed(2)} + 本期应付 ${due.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「累计已付」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '累计已付滚不动，后面每一期的付款比例与质保金扣留都会跟着错（它们都是按累计口径看的）。',
  });
  return out;
}

function checkTotalRow(totals, items) {
  const out = [];
  if (!totals || !totals.row) return out;
  for (const role of SUM_ROLES) {
    const stated = normNumber(totals.row[role]);
    if (stated === null) continue;
    let expect = null;
    let how = '';
    const dedupe = DEDUPE_ROLES[role];
    if (dedupe) {
      const first = new Map();
      for (const it of items) {
        const v = normNumber(it[role]);
        const k = dedupe === 'contract' ? contractKeyOf(it) : milestoneKeyOf(it);
        if (v !== null && !first.has(k)) first.set(k, v);
      }
      if (!first.size) continue;
      expect = round2(Array.from(first.values()).reduce((a, b) => a + b, 0));
      how = dedupe === 'contract'
        ? `按合同去重后 ${first.size} 份合同的「${LABELS[role]}」相加`
        : `按里程碑去重后 ${first.size} 个里程碑的「${LABELS[role]}」相加`;
    } else {
      let sum = 0;
      let n = 0;
      for (const it of items) {
        const v = normNumber(it[role]);
        if (v !== null) { sum += v; n += 1; }
      }
      if (!n) continue;
      expect = round2(sum);
      how = `本表 ${n} 行明细的「${LABELS[role]}」相加`;
    }
    if (Math.abs(stated - expect) <= TOL) continue;
    out.push({
      level: 'P0', category: '合计行与明细之和不符', line: totals.line,
      message: `合计行的「${LABELS[role]}」是 ${stated.toFixed(2)}，${how}是 ${expect.toFixed(2)}，`
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是月度付款申请与资金计划的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const p = it.period !== undefined ? String(it.period).trim() : '';
    const m = it.milestone !== undefined ? String(it.milestone).trim() : '';
    if (!p || !m) continue;
    const key = `${contractKeyOf(it)}|${p}|${m}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一里程碑重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一合同、同一期间、同一里程碑再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一笔里程碑付款被拆成两行（比如分次付款各建一行但期间写重了），'
          + '多出来的那一行会把本期应付与累计已付都重复计一遍。',
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
            + '这一列缺失时对应的复算与档位判断都做不了：缺哪一列就补哪一列，别让空值静默跳过检查。',
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
      level: 'P0', category: '金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 合同总额、里程碑金额与付款金额都不该为负，`
        + '冲回 / 红字应当单独列示并在备注里说明（否则累计已付会越滚越小，看起来像外包方倒欠钱）。',
    });
  }
  return out;
}

/* ========================== 完整档（付费）专用检查项 ========================== */
/* 契约同上：一律返回发现数组；这一段在免费包里会被整块摘掉 */

/** 验收状态归一化：'yes' 已验收 / 'no' 未验收 / null 认不出来（认不出来就不下结论） */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到软件外包里程碑验收与付款核对表正文（text）—— 请把「所属期间 / 外包方 / 外包合同编号 / 合同总额 / 里程碑名称 / 里程碑金额 / 付款比例 / 本期应付 / 前期已付 / 累计已付 / 验收状态 / 合同质保金比例 / 质保金比例」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `软件外包里程碑验收与付款核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何里程碑付款明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkPayableRecompute(it));
    findings.push(...checkPaidCumulative(it));
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

  let payableTotal = 0;
  let paidTotal = 0;
  for (const it of t.items) {
    const d = normNumber(it.payDue);
    if (d !== null) payableTotal += d;
    const c = normNumber(it.paidCum);
    if (c !== null) paidTotal += c;
  }

  const result = {
    status: 'success',
    service_type: 'SOFTWARE_OUTSOURCE_MILESTONE_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      contracts: new Set(t.items.map(contractKeyOf)).size,
      milestones: new Set(t.items.map(milestoneKeyOf)).size,
      totals_row: Boolean(t.totals && t.totals.row),
      payable_total: round2(payableTotal),
      paid_total: round2(paidTotal),
      tolerance: TOL,
      ratio_tolerance: RATIO_TOL,
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
    disclaimer: '只核"里程碑金额 × 付款比例 = 本期应付"、"前期已付 + 本期应付 = 累计已付"这类**表内勾稽**与档位口径，'
      + '**不判断该里程碑算不算验收完成、质保金该不该扣**（以验收单、外包合同与项目负责人口径为准）；'
      + '结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
