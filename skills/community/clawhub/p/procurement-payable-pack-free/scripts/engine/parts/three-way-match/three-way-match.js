'use strict';
/**
 * three-way-match.js —— 三单匹配AI核对（采购订单 / 入库单 / 发票）
 *
 * 为什么做这个：
 *   应付账款的标准动作是「三单匹配」——把**采购订单、入库单、发票**放在一起核对，
 *   确认"订购了、收到了、才付款"。漏掉这一步的常见后果是多付、错付、重复付款，
 *   金额直接是钱。而它**完全是确定性的**：
 *     · 订单号 / 供应商 / 物料 在各单据上是否一致；
 *     · 数量 × 单价 = 金额、不含税 + 税额 = 价税合计 是否自洽；
 *     · 发票数量与入库数量、发票金额与订单金额是否在容差内；
 *     · 同一张发票号有没有出现两次（重复付款线索）。
 *
 * 设计原则（与本仓库其它引擎一致）：
 *   · 自包含：只用 Node.js 标准库，**不发起任何网络请求**；
 *   · 每条结论都引用原文与行号，第三方可用同一份输入复算；
 *   · 材料不足时返回 insufficient_input 并说明缺什么，**绝不输出"未发现问题"**；
 *   · 只做AI比对，**不判断这笔付款是否合规**（那是财务制度与审批的事）。
 */

const CHECKS_GIVEN = [
  '关键字段跨单据一致（订单号 / 供应商 / 物料）',
  '数量 / 单价 / 金额跨单据一致',
  '重复发票号线索',
  '模板占位符残留',
];

const CHECKS_WITHHELD = [
  '行内算术（数量 × 单价 = 金额）',
  '税额与价税合计自洽（不含税 + 税额 = 价税合计）',
  '发票数量与入库数量的容差核对',
  '发票金额与订单金额的容差核对',
  '订单数量与入库数量的容差核对',
  '同一物料的单价跨单据偏离提示',
  '日期逻辑（订单 ≤ 入库 ≤ 发票）',
  '付款条款与账期字段核对',
];

/** 跨单据比对的关键字段：内部名 → 标签（中英） */
const FIELD_LABELS = [
  ['poNo', ['采购订单号', '订单号', '采购单号', 'po号', 'po no', 'po number', 'purchase order']],
  ['grnNo', ['入库单号', '收货单号', '验收单号', 'grn no', 'goods receipt', 'receipt no']],
  ['invoiceNo', ['发票号', '发票号码', 'invoice no', 'invoice number', 'inv. no']],
  ['supplier', ['供应商', '供应商名称', '供货方', '卖方', 'vendor', 'supplier']],
  ['item', ['物料', '物料名称', '品名', '货物名称', 'item', 'material', 'description']],
  ['quantity', ['数量', 'qty', 'quantity']],
  ['unitPrice', ['单价', 'unit price', 'price']],
  ['amount', ['金额', '不含税金额', 'amount', 'net amount']],
  ['tax', ['税额', '税金', 'tax', 'vat']],
  ['gross', ['价税合计', '含税金额', '应付金额', 'total', 'gross amount']],
  ['currency', ['币种', '货币', 'currency', 'ccy']],
];

const RECEIPT_RE = /入库|收货|验收|grn|goods receipt|receipt/i;
const ORDER_RE = /采购订单|订单|采购单|purchase order|\bpo\b/i;
const INVOICE_RE = /发票|invoice/i;

/* ---------------------------------------------------------------- 工具 */

function finding(level, category, line, message, advice, evidence) {
  return { level, category, line, message, advice, evidence };
}

/** 金额/数量归一：去千分位、货币符号与单位，返回可比较的数字字符串 */
function normNumber(s) {
  const t = String(s == null ? '' : s)
    .replace(/[,，\s\u00A0]/g, '')
    .replace(/^[¥￥$€£]/, '')
    .replace(/(元|美元|美金|欧元|港币|日元|人民币|usd|eur|cny|rmb|hkd|jpy)$/i, '');
  if (!/^\d+(\.\d+)?$/.test(t)) return null;
  return String(Math.round(parseFloat(t) * 100) / 100);
}

function numOf(s) {
  const n = normNumber(s);
  return n === null ? null : parseFloat(n);
}

/** 文本归一：名称类字段"看着一样就算一样" */
function normText(s) {
  return String(s == null ? '' : s)
    .replace(/[\s\u00A0]+/g, ' ')
    .replace(/[。．.,，;；:：、"'“”‘’()（）]/g, '')
    .trim()
    .toUpperCase();
}

/** 从一段文本里抽出「标签 值」形式的字段 */
function extractFields(text) {
  const out = {};
  const lines = String(text == null ? '' : text).split(/\r?\n/);
  lines.forEach((raw, idx) => {
    const line = raw.trim();
    if (!line) return;
    for (const [key, labels] of FIELD_LABELS) {
      for (const label of labels) {
        const re = new RegExp(
          '(?:^|[\\s|;；,，])' + label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
            + '\\s*[:：]?\\s*([^|;；\\n]+)',
          'i'
        );
        const m = re.exec(line);
        if (m && m[1] && m[1].trim()) {
          (out[key] = out[key] || []).push({ value: m[1].trim(), line: idx + 1, raw: line });
          break;
        }
      }
    }
  });
  return out;
}

/** 收集材料：documents 数组，或一个 text（空行分隔多张单据） */
function collectMaterial(payload) {
  const p = payload && typeof payload === 'object' ? payload : {};
  const docs = [];
  if (Array.isArray(p.documents)) {
    p.documents.forEach((d, i) => {
      if (!d) return;
      const text = typeof d === 'string' ? d : String(d.text != null ? d.text : (d.content != null ? d.content : ''));
      if (!text.trim()) return;
      const type = (d && (d.type || d.part || d.name)) || ('单据 ' + (i + 1));
      docs.push({ type: String(type).slice(0, 40), text: text });
    });
  } else {
    const single = p.text != null ? p.text : p.content;
    if (typeof single === 'string' && single.trim()) {
      const blocks = single.split(/\n[ \t]*\n+/).map((x) => x.trim()).filter(Boolean);
      if (blocks.length >= 2) {
        blocks.forEach((b, i) => {
          const first = (b.split('\n')[0] || '').trim().slice(0, 40);
          docs.push({ type: first || ('单据 ' + (i + 1)), text: b });
        });
      } else {
        docs.push({ type: p.type ? String(p.type).slice(0, 40) : '单据 1', text: single });
      }
    }
  }
  return docs;
}

/** 给单据归类：order / receipt / invoice / other */
function kindOf(doc) {
  if (INVOICE_RE.test(doc.type)) return 'invoice';
  if (RECEIPT_RE.test(doc.type)) return 'receipt';
  if (ORDER_RE.test(doc.type)) return 'order';
  return 'other';
}

/* ------------------------------------------------------------ 各项检查 */

/** 1. 关键字段跨单据一致 */
function checkCrossDocument(docs, perDoc, skipKeys) {
  const out = [];
  const skip = skipKeys instanceof Set ? skipKeys : new Set();
  for (const [key, labels] of FIELD_LABELS) {
    if (skip.has(key)) continue;   // 已被更具体的检查覆盖，避免同一件事报两遍
    const hits = [];
    perDoc.forEach(({ doc, fields }) => {
      (fields[key] || []).forEach((h) => hits.push({ docType: doc.type, ...h }));
    });
    if (hits.length < 2) continue;
    const byDoc = new Map();
    hits.forEach((h) => { if (!byDoc.has(h.docType)) byDoc.set(h.docType, h); });
    if (byDoc.size < 2) continue;

    const isNumber = ['quantity', 'unitPrice', 'amount', 'tax', 'gross'].includes(key);
    const groups = new Map();
    byDoc.forEach((h) => {
      const n = isNumber ? (normNumber(h.value) || normText(h.value)) : normText(h.value);
      if (!groups.has(n)) groups.set(n, []);
      groups.get(n).push(h);
    });
    if (groups.size <= 1) continue;

    const shown = [...groups.values()].map((hs) =>
      hs.map((h) => `${h.docType}「${h.value}」(第${h.line}行)`).join(' ')).join(' ／ ');
    out.push(finding('P0', '跨单据字段不一致', 0,
      `字段「${labels[0]}」在各单据上写得不一样：${shown}。`,
      '三单匹配要求这些字段一致；先确认以哪一份为准，再统一改正。',
      hits.map((h) => h.raw).filter((v, i, a) => a.indexOf(v) === i).slice(0, 4)));
  }
  return out;
}

/** 2. 重复发票号线索 */
function checkDuplicateInvoice(perDoc) {
  const out = [];
  const seen = new Map();
  perDoc.forEach(({ doc, fields }) => {
    (fields.invoiceNo || []).forEach((h) => {
      const k = normText(h.value);
      if (!k) return;
      if (!seen.has(k)) seen.set(k, []);
      seen.get(k).push({ docType: doc.type, ...h });
    });
  });
  seen.forEach((list, k) => {
    const docsSeen = [...new Set(list.map((x) => x.docType))];
    if (docsSeen.length >= 2 || list.length >= 2) {
      out.push(finding('P1', '重复发票号线索', list[0].line,
        `发票号「${list[0].value}」在同一套材料里出现了 ${list.length} 次（${docsSeen.join('、')}）。`,
        '同一张发票不应重复入账；请确认是不是重复提交或重复付款。',
        list.map((x) => x.raw).slice(0, 3)));
    }
  });
  return out;
}







/** 6. 占位符残留 */
const PLACEHOLDER_RE = /(【[^】]{0,20}】|\[\[[^\]]{0,20}\]\]|\bTBD\b|\bXXX+\b|_{4,}|待填|待定|请填写)/gi;
function checkPlaceholders(docs) {
  const out = [];
  docs.forEach((d) => {
    d.text.split(/\r?\n/).forEach((raw, idx) => {
      PLACEHOLDER_RE.lastIndex = 0;
      const m = PLACEHOLDER_RE.exec(raw);
      if (m) {
        out.push(finding('P0', '模板占位符残留', idx + 1,
          `${d.type} 第${idx + 1}行还留着未替换的内容「${m[0]}」。`,
          '入账前必须逐一替换或删除。', [raw.trim()]));
      }
    });
  });
  return out;
}

/* -------------------------------------------------------------- 主流程 */

function analyze(docs, opts) {
  const perDoc = docs.map((doc) => ({ doc, fields: extractFields(doc.text) }));
  const findings = [
    ...checkCrossDocument(docs, perDoc, new Set()),
    ...checkDuplicateInvoice(perDoc),
    ...checkPlaceholders(docs),
  ];
  const summary = { p0: 0, p1: 0, p2: 0 };
  const byCategory = {};
  findings.forEach((f) => {
    const k = f.level === 'P0' ? 'p0' : (f.level === 'P1' ? 'p1' : 'p2');
    summary[k]++;
    byCategory[f.category] = (byCategory[f.category] || 0) + 1;
  });
  summary.total = findings.length;
  summary.by_category = byCategory;
  summary.verdict = summary.p0 > 0
    ? '发现必须处理的硬错误（P0）'
    : (summary.p1 > 0 ? '没有 P0，但有需要人工核对的项（P1）'
      : (summary.p2 > 0 ? '只有提示性预警（P2），没有硬错误'
        : '在上述检查项范围内没有发现问题 —— 这不等于没有问题'));
  return { findings, summary, docCount: docs.length, kinds: docs.map(kindOf) };
}

function insufficient(missing, advice) {
  return { status: 'insufficient_input', missing: [].concat(missing), advice };
}

/**
 * @param {Object} payload { documents:[{type,text}], tolerancePct?, toleranceAbs? } 或 { text }
 */
function run(payload) {
  const docs = collectMaterial(payload);
  if (docs.length === 0) {
    return insufficient(['没有收到任何单据内容'],
      '请提供至少两张单据（采购订单 / 入库单 / 发票），每张形如 {"type":"采购订单","text":"订单号 …\\n金额 …"}；'
      + '也可以用一个文本、单据之间空一行。');
  }
  const totalChars = docs.reduce((n, d) => n + d.text.length, 0);
  if (totalChars < 30) {
    return insufficient([`单据内容过短（共 ${totalChars} 字）`],
      '请把单据正文完整贴进来；内容过短时无法提取字段，也就做不了有意义的核对。');
  }
  const opts = {
    tolerancePct: payload && Number.isFinite(payload.tolerancePct) ? payload.tolerancePct : undefined,
    toleranceAbs: payload && Number.isFinite(payload.toleranceAbs) ? payload.toleranceAbs : undefined,
  };
  const result = analyze(docs, opts);
  result.scope = { given: CHECKS_GIVEN.slice(), withheld: CHECKS_WITHHELD.slice() };
  result.docs = docs.map((d) => ({ type: d.type, chars: d.text.length }));
  return { status: 'success', result: result };
}

module.exports = {
  run,
  analyze,
  collectMaterial,
  extractFields,
  kindOf,
  normNumber,
  normText,
  CHECKS_GIVEN,
  CHECKS_WITHHELD,
  SAMPLE_TEXT: [
    "采购订单 PURCHASE ORDER",
    "采购订单号: PO-2026-0517",
    "供应商: 河南甲物资有限公司",
    "物料: 螺纹钢 HRB400",
    "数量: 120",
    "单价: 3,850.00",
    "金额: 462,000.00",
    "",
    "入库单 GOODS RECEIPT",
    "采购订单号: PO-2026-0517",
    "供应商: 河南甲物资有限公司",
    "入库单号: GRN-2026-0912",
    "数量: 118",
    "金额: 454,300.00",
  ].join('\n'),
};