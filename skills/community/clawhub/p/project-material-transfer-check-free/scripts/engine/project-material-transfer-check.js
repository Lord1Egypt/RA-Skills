/**
 * ⚠️ 本文件是 **免费档子集**：只实现免费检查项；**完整档（付费）的实现不在这个包里**。
 * `CHECKS_WITHHELD` 只是"未执行的检查项"的**说明文本**，不是实现。
 */
'use strict';
/**
 * project-material-transfer-check.js —— 工程材料调拨与领用核对（免费档 / 完整档共用源码）
 *
 * 谁在什么时候必须做这件事：**建筑 / 安装企业每月结账前**。总部仓（集中采购仓）与各个项目部
 * 之间每个月都在调拨、领用、退库，月底必须拿一张台账把这四件事逐笔勾稽上：
 *
 *   结存数量 = 期初数量 + 调拨数量（调入） − 调出数量 − 领用数量 + 退库数量
 *   领用金额 = 领用数量 × 单价
 *   合计行各列 = 明细行相加
 *
 * 这三条全是算术，**完全能机械核出来**。调拨单对不上，方向只有两个 ——
 * **材料丢了**（发出去的量收不回来）或**成本串了项目**（一批料被记到别的项目头上）。
 * 两条都会在月报、项目成本归集与审计抽样时暴露出来。
 *
 * 自包含：只用 Node.js 标准库，不 require 本技能包以外的任何文件，
 * **不发起任何网络请求**（没有 fetch / http / https / net / dns / tls）。
 *
 * 免费档执行 6 项；完整档追加 5 项（见 CHECKS_WITHHELD）。材料不足时**绝不给结论**。
 * ⚠️ 本工具**不判断**材料调拨该不该批、领用有没有超授权额度、单价该按哪个口径计价
 *    （那是审批流程、项目管理制度与采购合同的事）：表里给的期初、调拨、调出、领用、退库、
 *    单价、合同单价、预算单价一律**以你填的为准**，本工具只核表内勾稽，并按原文行号列出可疑处。
 * ⚠️ 账上勾稽通过**不代表**材料真的到了工地 —— 那要靠实物盘点（见 checks_out_of_scope）。
 *
 * ⚠️ 付费项用**形态 B**：先把入参里的「完整档」开关算成一个布尔常量，
 *    再把付费检查包进以该常量为条件的 `if` 块（**不要**留「完整档才执行的检查」那类 MARKER——
 *    两个形态同时存在时 `strip_free_engine` 会走形态 A 把免费检查也整块删掉，第 236 轮踩过）。
 *    ⚠️ 也不要在注释里写出开关/条件语句的字面量：`strip_free_engine` 的残渣断言认得那些字面量，
 *    注释里写一遍会被判成「没删干净」而整包回滚（第 236 轮实测连续踩了两次）。
 */

const CHECKS_GIVEN = [
  '结存数量复算（期初 + 调入 − 调出 − 领用 + 退库 = 结存）',
  '领用金额复算（领用数量 × 单价 = 领用金额）',
  '合计行逐列复核',
  '同一材料编码同一项目同一期间重复行检测',
  '空白与占位符检测',
  '数量或金额为负检测',
];

const CHECKS_WITHHELD = [
  '领用数量超过可用数量（期初 + 调入 − 调出）提示',
  '退库数量超过累计领用数量提示',
  '同一材料跨项目重复调拨同一单据号提示',
  '单价与合同单价 / 预算单价不一致提示',
  '结存数量为负提示',
];

const OUT_OF_SCOPE = [
  '判断材料调拨该不该批、领用有没有超授权额度（那是审批流程与项目管理制度的事）',
  '核对材料是否真的到了工地：账上勾稽**不代表**实物在场，那要靠仓库实物盘点',
  '判断合同单价 / 预算单价本身填得对不对（以采购合同、预算书与内部结算价为准）',
  '区分甲供材料与乙供材料的计价口径，处理增值税、运输费与装卸费的归集',
  '读取 ERP / 物资系统 / 仓库台账的导出文件（需要你先导出成文本贴进来）',
];

const SAMPLE_TEXT = [
  '所属期间\t单据号\t项目名称\t材料编码\t材料名称\t单位\t期初数量\t调拨数量\t调出数量\t领用数量\t退库数量\t结存数量\t合同单价\t单价\t领用金额',
  '2026-01\tDB-20260101\t项目A-1号楼\tCL-1001\t螺纹钢 HRB400\t吨\t100\t50\t20\t30\t5\t105\t3800.00\t3800.00\t114000.00',
  '2026-01\tDB-20260102\t项目B-2号楼\tCL-2001\t商品混凝土 C30\tm³\t200\t80\t0\t120\t10\t170\t460.00\t460.00\t55200.00',
  '2026-02\tDB-20260201\t项目A-1号楼\tCL-1001\t螺纹钢 HRB400\t吨\t105\t0\t10\t40\t0\t55\t3800.00\t3800.00\t152000.00',
  '合计\t\t\t\t\t\t405\t130\t30\t190\t15\t330\t\t\t321200.00',
].join('\n');

const TOL = 0.01;              // 算术复算容差（精确勾稽）
const PRICE_TOL = 0.01;        // 单价比对：0.01 元以内的差算四舍五入
const PRICE_REL_TOL = 0.001;   // 单价比对：合同单价的 0.1%（大额单价的小数尾差不算不一致）

const ROLES = {
  // ⚠️ 顺序即优先级：**更具体的别名必须排在更宽泛的词前面**。
  //    · 「数量」两个字是 `qtyOther` 的别名，它**必须排在最后** ——「退库数量」「调拨数量」
  //      「领用数量」「结存数量」「期初数量」「调出数量」都含「数量」两个字，兜底角色一旦
  //      排在前面就会把它们整列抢走：表现是**不报缺列、只是算错**（第 232 轮同类事故：
  //      「本期摊销月数」抢走「摊销月数」，月摊销额整列误报）。
  //    · **金额列必须排在数量列之前**：「领用金额」含「领用」两个字，被更宽泛的「领用」
  //      抢走时不会报缺列，只会让 15 个表头只解析出 14 个字段（本引擎第一版实测踩到，
  //      header_map_check 当场报「有 1 列被覆盖/丢掉了」）。同理「退库金额」不能被「退库」抢走。
  //    · 「合同单价」「预算单价」必须先被 contractPrice 认走，否则会被更宽泛的 price 抢走。
  //    · 「材料编码」必须先被 materialCode 认走，否则会被更宽泛的「材料」抢走。
  period: ['所属期间', '会计期间', '所属期', '期间', '月份', '月度'],
  docNo: ['调拨单号', '领用单号', '出库单号', '退库单号', '单据编号', '单据号', '单号'],
  project: ['项目名称', '工程项目', '项目部', '施工项目', '项目'],
  materialCode: ['材料编码', '材料编号', '物料编码', '物资编码', '材料代码', '编码'],
  materialName: ['材料名称', '物料名称', '材料品名', '材料规格', '品名', '材料'],
  unit: ['计量单位', '材料单位', '单位'],
  contractPrice: ['合同单价', '预算单价', '合同约定单价', '合同价', '预算价'],
  price: ['材料单价', '实际单价', '领用单价', '含税单价', '单价'],
  amount: ['领用金额', '材料金额', '发出金额', '领用成本', '金额'],
  qtyBegin: ['期初结存数量', '期初库存数量', '期初数量', '期初结存', '期初余额', '期初'],
  qtyIn: ['调拨数量', '调入数量', '调拨入库数量', '调入量', '调入', '调拨'],
  qtyOut: ['调出数量', '调出量', '调出'],
  qtyIssue: ['领用数量', '领用量', '耗用数量', '领用'],
  qtyReturn: ['退库数量', '退料数量', '退回数量', '退库量', '退库', '退料'],
  qtyEnd: ['结存数量', '期末结存数量', '期末结存', '结存库存', '期末数量', '结存', '期末'],
  qtyOther: ['数量'],
};

const LABELS = {
  period: '所属期间', docNo: '单据号', project: '项目名称', materialCode: '材料编码',
  materialName: '材料名称', unit: '单位', qtyBegin: '期初数量', qtyIn: '调拨数量',
  qtyOut: '调出数量', qtyIssue: '领用数量', qtyReturn: '退库数量', qtyEnd: '结存数量',
  contractPrice: '合同单价', price: '单价', amount: '领用金额', qtyOther: '数量',
};

/** 必需列：缺一列就**不给结论**（宁可说"材料不足"，也不猜到别处去取数） */
const REQUIRED = ['period', 'project', 'materialCode', 'qtyBegin', 'qtyIn', 'qtyOut', 'qtyIssue',
  'qtyReturn', 'qtyEnd', 'price', 'amount'];
/** 合计行逐列复核的列（单价是"每单位"的量，加总没有意义，刻意不列） */
const SUM_ROLES = ['qtyBegin', 'qtyIn', 'qtyOut', 'qtyIssue', 'qtyReturn', 'qtyEnd', 'amount'];
/**
 * 免费档负值检测覆盖的列：**数量侧与金额侧**。
 * ⚠️ 刻意**不含**结存数量 —— "结存为负"是完整档的独立检查项（见 CHECKS_WITHHELD），
 *    免费档提前报出结存为负就等于把付费结论送出去了。
 */
const NEG_ROLES = ['qtyBegin', 'qtyIn', 'qtyOut', 'qtyIssue', 'qtyReturn', 'price', 'amount'];
const TOTAL_WORDS = /^(合计|总计|小计|共计|累计|合计：|汇总)$/;

function insufficient(missing) {
  return {
    status: 'insufficient_input',
    missing: [].concat(missing),
    advice: '请补上这些再跑；材料不足时本工具不做任何认定，也不套用默认值（不会输出「未发现问题」）。',
  };
}

function splitRow(line) {
  if (line.indexOf('\t') >= 0) return line.split('\t').map((s) => s.trim());
  return line.split(/\s{2,}/).map((s) => s.trim());
}

function isBlank(v) {
  if (v === undefined || v === null) return true;
  const s = String(v).trim();
  return s === '' || /^[-—–−]+$/.test(s) || /^(n\/?a|无|待填|待补|待定|空)$/i.test(s);
}

function roleOf(header) {
  const h = String(header).replace(/[\s（）()]/g, '');
  for (const [role, keys] of Object.entries(ROLES)) {
    if (keys.some((k) => h.indexOf(k) >= 0)) return role;
  }
  return null;
}

/** 归一化数量 / 金额：认千分位、货币符号、百分号、Unicode 负号与尾部计量单位（吨 / m³ / 米 / 根 …） */
function normNumber(raw) {
  if (isBlank(raw)) return null;
  let s = String(raw).trim()
    .replace(/[−–—]/g, '-')
    .replace(/[,，\s¥￥$]/g, '')
    .replace(/%$/, '');
  s = s.replace(/[^\d.]*$/, '');
  if (!s || !/^[-+]?(\d+(\.\d*)?|\.\d+)$/.test(s)) return null;
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
    roles.forEach((role, c) => {
      if (!role) return;
      row[role] = cells[c] === undefined ? '' : cells[c];
    });
    const head = String(cells[0] === undefined ? '' : cells[0]).trim();
    const periodCell = row.period === undefined ? '' : String(row.period).trim();
    const isTotal = TOTAL_WORDS.test(head) || TOTAL_WORDS.test(periodCell);
    if (isTotal) { totals.row = row; totals.line = i + 1; }
    else items.push(row);
  }
  return { items, totals, missingColumns };
}

const who = (it) => {
  const p = it && it.period !== undefined && String(it.period).trim() !== ''
    ? String(it.period).trim() : `第 ${it && it.line} 行`;
  const n = [it && it.project, it && it.materialCode]
    .map((v) => (v === undefined || v === null ? '' : String(v).trim()))
    .filter(Boolean).join(' / ');
  return n ? `${p}「${n}」` : p;
};

const periodKeyOf = (it) => {
  const p = it && it.period !== undefined ? String(it.period).trim() : '';
  return p || `第 ${it && it.line} 行`;
};

/* ================================ 免费档检查项 ================================ */
/* 契约：以下每个 check* 一律返回**发现数组**（没有发现就是空数组），不混用 null / 单对象 */

/** 结存数量 = 期初 + 调入 − 调出 − 领用 + 退库 */
function checkBalanceIdentity(it) {
  const out = [];
  const begin = normNumber(it.qtyBegin);
  const inn = normNumber(it.qtyIn);
  const outQty = normNumber(it.qtyOut);
  const issue = normNumber(it.qtyIssue);
  const back = normNumber(it.qtyReturn);
  const stated = normNumber(it.qtyEnd);
  if (begin === null || inn === null || outQty === null || issue === null
    || back === null || stated === null) return out;
  const expect = round2(begin + inn - outQty - issue + back);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '结存数量勾稽不符', line: it.line,
    message: `${who(it)}：期初 ${begin.toFixed(2)} + 调入 ${inn.toFixed(2)} − 调出 ${outQty.toFixed(2)} `
      + `− 领用 ${issue.toFixed(2)} + 退库 ${back.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「结存数量」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '这一格是四笔业务的汇总：对不上说明有一笔漏记、串了项目，或者退库没有冲回领用。',
  });
  return out;
}

/** 领用金额 = 领用数量 × 单价 */
function checkAmountRecompute(it) {
  const out = [];
  const issue = normNumber(it.qtyIssue);
  const price = normNumber(it.price);
  const stated = normNumber(it.amount);
  if (issue === null || price === null || stated === null) return out;
  const expect = round2(issue * price);
  if (Math.abs(expect - stated) <= TOL) return out;
  out.push({
    level: 'P0', category: '领用金额复算不符', line: it.line,
    message: `${who(it)}：领用数量 ${issue.toFixed(2)} × 单价 ${price.toFixed(2)} = ${expect.toFixed(2)}，`
      + `表里「领用金额」是 ${stated.toFixed(2)}，相差 ${round2(stated - expect).toFixed(2)}。`
      + '金额是数量乘单价乘出来的，差在这里多半是单价用错了版本（合同价 / 预算价 / 含税价混用），'
      + '或者退库数量没有从领用里冲减。',
  });
  return out;
}

/** 合计行逐列复核 */
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
        + `相差 ${round2(stated - expect).toFixed(2)}。合计行就是月报、项目成本归集与盘点表的取数口径，对不上说明有一边错。`,
    });
  }
  return out;
}

/** 同一材料编码 + 同一项目 + 同一期间出现多行 */
function checkDuplicates(items) {
  const out = [];
  const seen = new Map();
  for (const it of items) {
    const m = String(it.materialCode === undefined ? '' : it.materialCode).trim();
    const p = String(it.project === undefined ? '' : it.project).trim();
    const d = String(it.period === undefined ? '' : it.period).trim();
    if (!m || !p || !d) continue;
    const key = `${m}|${p}|${d}`;
    if (seen.has(key)) {
      out.push({
        level: 'P1', category: '同一材料同一项目同一期间重复行', line: it.line,
        message: `${who(it)}在第 ${seen.get(key)} 行已出现，第 ${it.line} 行同一材料、同一项目、同一期间再次出现 —— `
          + '要么是重复粘贴了一行，要么是同一批料被拆成两行（比如分次到货各建一行）：'
          + '多出来的那一行会把调拨量与领用量都重复计一遍。',
      });
    } else seen.set(key, it.line);
  }
  return out;
}

/** 关键列为空或占位符 */
function checkBlanks(items) {
  const out = [];
  for (const it of items) {
    for (const role of REQUIRED) {
      if (isBlank(it[role])) {
        const s = String(it[role] === undefined ? '' : it[role]).trim();
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

/** 数量或金额为负（结存为负归完整档） */
function checkNegative(it) {
  const out = [];
  for (const role of NEG_ROLES) {
    const v = normNumber(it[role]);
    if (v === null) continue;
    if (v >= -TOL) continue;
    out.push({
      level: 'P0', category: '数量或金额为负', line: it.line,
      message: `${who(it)}的「${LABELS[role]}」是 ${v.toFixed(2)}（负数）—— 期初、调拨、调出、领用、退库、单价与领用金额都不该为负：`
        + '红字冲回 / 反向调拨应当单独列示并在备注里说明，否则四笔业务会被负号悄悄抵消。',
    });
  }
  return out;
}

/* ============================ 完整档（付费）检查项 ============================ */

/** 领用数量超过可用数量（期初 + 调入 − 调出） */
/** 退库数量超过累计领用数量（按材料 + 项目累计） */
/** 同一材料跨项目重复调拨同一单据号 */
/** 单价与合同单价 / 预算单价不一致 */
/** 结存数量为负 */
/* ================================== 主入口 ================================== */

function run(payload) {
  if (payload !== undefined && payload !== null && typeof payload !== 'object') {
    return insufficient(`入参不是对象或数组（收到的是 ${typeof payload}）`);
  }
  const text = payload && typeof payload.text === 'string' ? payload.text : '';
  if (text.trim().length < 5) {
    return insufficient('没有收到工程材料调拨与领用核对表正文（text）—— 请把「所属期间 / 单据号 / 项目名称 / 材料编码 / 材料名称 / 单位 / 期初数量 / 调拨数量 / 调出数量 / 领用数量 / 退库数量 / 结存数量 / 合同单价 / 单价 / 领用金额」这张表贴进来');
  }
  const t = parseTable(text);
  if (t.missingColumns && t.missingColumns.length) {
    return insufficient([
      `工程材料调拨与领用核对表缺少必需列：${t.missingColumns.join('、')}`,
      `已识别的表头：${splitRow(text.split(/\r?\n/)[0]).join(' / ')}`,
    ]);
  }
  if (!t.items.length) {
    return insufficient('表里只有表头，没有任何材料调拨 / 领用明细行');
  }

  const groups = new Map();
  for (const it of t.items) {
    const k = periodKeyOf(it);
    if (!groups.has(k)) groups.set(k, { period: k, rows: [] });
    groups.get(k).rows.push(it);
  }

  const findings = [];
  for (const it of t.items) {
    findings.push(...checkBalanceIdentity(it));
    findings.push(...checkAmountRecompute(it));
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

  let issueTotal = 0;
  let amountTotal = 0;
  for (const it of t.items) {
    const q = normNumber(it.qtyIssue);
    if (q !== null) issueTotal += q;
    const a = normNumber(it.amount);
    if (a !== null) amountTotal += a;
  }

  const result = {
    status: 'success',
    service_type: 'PROJECT_MATERIAL_TRANSFER_CHECK',
    scope: {
      checks: CHECKS_GIVEN,
      checks_not_run: notRun,
      rows: t.items.length,
      periods: groups.size,
      totals_row: Boolean(t.totals && t.totals.row),
      issue_total: round2(issueTotal),
      amount_total: round2(amountTotal),
      tolerance: TOL,
      price_tolerance: PRICE_TOL,
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
    disclaimer: '只核"期初 + 调入 − 调出 − 领用 + 退库 = 结存""领用数量 × 单价 = 领用金额"这类**表内勾稽**'
      + '与档位提示，**不判断**材料调拨该不该批、领用有没有超授权额度、单价该按哪个口径计价'
      + '（以项目管理制度、采购合同与实物盘点为准）；结论可由第三方用同一份输入复算。',
  };
  return { status: 'success', result };
}

module.exports = {
  run, parseTable, roleOf, normNumber, round2, CHECKS_GIVEN, CHECKS_WITHHELD, OUT_OF_SCOPE, SAMPLE_TEXT,
};
