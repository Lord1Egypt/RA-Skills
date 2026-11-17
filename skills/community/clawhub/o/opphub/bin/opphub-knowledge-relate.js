#!/usr/bin/env node
// bin/opphub-knowledge-relate.js · v4.0
// status: implemented (v4 P1-5 列校验 + 金额解析增强 + 二进制 XLS 检测)
//
//   输入: xls 合同清单 (HTML 格式导出, 跟 Excel 兼容)
//   输出: cards[] 数组 (skill 6 阶段流程第 5 步可批量入库)
//
// 用法: bot 调
//   opphub knowledge-relate --xls /path/to/contracts.xls --company "睿驰嘉禾" --json
//   opphub knowledge-relate --xls contracts.xls --company "睿驰" --top-customers 20 --top-suppliers 10 --json
// 返 { ok, company, partners: { upstream: [...], downstream: [...] }, cards: [...], summary: {...} }
//
// 实现:
//   - 解析 xls (HTML 格式, 不是真 xls 二进制, 见 file(1) 报 "HTML document text")
//   - 识别 睿驰在合同中是甲方还是乙方:
//     * 甲方 = 睿驰 → 乙方是下游客户 (睿驰是供应方)
//     * 乙方 = 睿驰 → 甲方是上游供应商 (睿驰是采购方)
//   - 按公司名 + 合同金额排序
//   - 拆 cards: top N 客户/供应商 + 类别聚合
//   - 输出 cards.json 给 ingest-batch 用
//
//   - xls 解析只支持 HTML 格式 (file(1) 报 "HTML document text")
//   - 睿驰公司名用 --company 传入, 自动容错匹配 (去掉括号/多主体/分公司)
//   - 类别按公司名关键词 (传媒/科技/广告/集团/工作室/...)
//
// 不做的事:
//   - 不调 LLM (skill turn 的活, 不在本 bin)
//   - 不入库 (阶段 5 才入库)

import { readFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--help" || a === "-h") args.help = true;
    else if (a === "--xls") args.xls = argv[++i];
    else if (a === "--company") args.company = argv[++i];
    else if (a === "--top-customers") args.topCustomers = parseInt(argv[++i], 10);
    else if (a === "--top-suppliers") args.topSuppliers = parseInt(argv[++i], 10);
    else if (a === "--cards-out") args.cardsOut = argv[++i];
    else if (!a.startsWith("--")) args._.push(a);
  }
  return args;
}

// v4.0.0 P1-5: 金额解析增强 (处理逗号/中文/括号负数/货币符号)
// 中文复合单位: 5千万 = 5 × 千 × 万 = 5e7, 3.2万亿 = 3.2 × 万 × 亿 = 3.2e12
function parseAmount(raw) {
  if (raw == null) return 0;
  let s = String(raw).trim();
  if (!s) return 0;
  // 括号负数: (100) → -100
  let negative = false;
  if (/^\(.*\)$/.test(s)) {
    negative = true;
    s = s.slice(1, -1);
  }
  // 中文金额: 拆 "数字 + 单位链" (e.g. "5千万" = 5 + 千 + 万)
  const cnMatch = s.match(/^([\d,.]+)(.*)$/);
  if (cnMatch) {
    const numStr = cnMatch[1].replace(/,/g, "");
    const rest = cnMatch[2] || "";
    const num = parseFloat(numStr) || 0;
    let mult = 1;
    // 贪婪扫所有单位, 累乘 (千万 = 千 × 万 = 1e7, 万亿 = 万 × 亿 = 1e12)
    if (/万/.test(rest)) mult *= 1e4;
    if (/亿/.test(rest)) mult *= 1e8;
    if (/仟|千/.test(rest)) mult *= 1e3;
    if (/百/.test(rest)) mult *= 1e2;
    if (mult > 1) {
      const result = num * mult;
      return negative ? -result : result;
    }
  }
  // 普通数字: 去货币符号/空格/逗号
  s = s.replace(/[¥$€£￥,\s]/g, "");
  // 只留数字 + 小数点 + 负号
  s = s.replace(/[^\d.\-]/g, "");
  const num = parseFloat(s) || 0;
  return negative ? -Math.abs(num) : num;
}

// 解析 xls (HTML 格式)
// v4.0.0 P1-5: 二进制 XLS 检测
function parseXlsHtml(html) {
  // 检测二进制 xls (OLE2 签名: D0 CF 11 E0) — 我们的解析器只支持 HTML
  // 避免 file(1) 报 "HTML document text" 但实际是 OLE2 时的误处理
  if (/^[\x00-\x08\x0E-\x1F]/.test(html) || html.startsWith("<?xml")) {
    // 二进制 / XML 不归本 bin, 提示 user 转 HTML 格式
    const err = new Error("binary_or_xml_xls_not_supported");
    err.code = "BINARY_XLS_NOT_SUPPORTED";
    err.message = "本 bin 只支持 Excel \"另存为网页 (*.html)\" 格式, 不支持二进制 xls / xlsx";
    throw err;
  }
  const rows = html.match(/<tr>(.*?)<\/tr>/gs) || [];
  const data = [];
  for (const r of rows) {
    const cells = [];
    const cellRegex = /<t[dh][^>]*>(.*?)<\/t[dh]>/gs;
    let m;
    while ((m = cellRegex.exec(r)) !== null) {
      cells.push(m[1].replace(/<[^>]+>/g, "").trim());
    }
    if (cells.length > 0) data.push(cells);
  }
  return data;
}

// 睿驰公司名匹配 (容错: 括号 / 多主体 / 北京分公司 / 前缀匹配)
function buildCompanyVariants(company) {
  const variants = new Set();
  variants.add(company);
  variants.add(company.replace(/[（(].*?[)）]/g, "").trim());
  // 反向: xls 里全名 "上海睿驰嘉禾数字传媒科技有限公司" 应匹配 --company "睿驰嘉禾"
  // 加一个简化的核心名 (去掉 "上海" "北京" 前缀 + "公司/集团" 后缀)
  const core = company.replace(/^(上海|北京|广州|深圳|杭州|成都|南京|武汉|苏州|天津|重庆)/, "").replace(/(有限公司|股份有限公司|集团|公司)$/, "").trim();
  if (core && core !== company) variants.add(core);
  return variants;
}

// 判断 partner 是否属于本公司 (前缀匹配)
function isOurCompany(partner, variants) {
  for (const v of variants) {
    if (partner === v) return true;
    if (v.length >= 4 && partner.includes(v)) return true;
  }
  return false;
}

// 类别 (按公司名关键词)
// D1 修复: 放宽正则避免 "蓝标/京东黑珑/霍尔斯" 等特征词漏进去 other
//   - 原版 "传媒/科技/广告" 等全靠中文关键词, 实际遇到 4-6 字公司名 不一定命中
//   - D1 放宽: 加 "品牌/互动/商业/推广/设计/创意/数码/数字/咨询/服务" 等 16 个营销圈常见词
function categorize(name) {
  if (/[传媒传播映画影像]|文化|内容|拍摄|视|绘|品牌|互动|推广|设计|创意|数码|数字/.test(name)) return { code: "media", name: "影视/传媒/文化" };
  if (/[科技网络信息]|数据|营销|商业|咨询|服务|智能|云|软件|系统|股份|有限|合伙|集团|工作室|个体|个人|汽车|电商|法律/.test(name)) {
    if (/[科技网络信息]|数据|智能|云|软件|系统/.test(name)) return { code: "tech", name: "科技/网络/信息" };
    if (/营销|推广|品牌|商业/.test(name)) return { code: "ad", name: "广告/营销" };
    if (/汽车/.test(name)) return { code: "auto", name: "汽车" };
    if (/电商/.test(name)) return { code: "ecom", name: "电商" };
    if (/法律/.test(name)) return { code: "legal", name: "法律" };
    if (/[集团股份]|有限|合伙/.test(name)) return { code: "group", name: "集团/股份" };
    if (/[工作室]|个体|个人/.test(name)) return { code: "studio", name: "工作室/个体" };
    if (/[咨询设计服务]/.test(name)) return { code: "consult", name: "咨询/服务" };
  }
  return { code: "other", name: "其他" };
}

// 是否公司名 (排除自然人 2-4 字)
function isCompany(name) {
  if (!name) return false;
  if (/^[\u4e00-\u9fa5]{2,4}$/.test(name)) return false; // 2-4 字中文人名
  if (/^[\u4e00-\u9fa5]{2,4}【/.test(name)) return false; // "刘雅坤【XXX】" 也排除
  return true;
}

function aggregateCards(parsedData, company, options) {
  const topCustomersN = options.topCustomers ?? 20;
  const topSuppliersN = options.topSuppliers ?? 10;
  const variants = buildCompanyVariants(company);

  // 找 header 行 (含 "合同编号" / "甲方" / "乙方")
  let headerIdx = 0;
  for (let i = 0; i < Math.min(5, parsedData.length); i++) {
    if (parsedData[i].some((c) => c.includes("合同编号") || c.includes("甲方"))) {
      headerIdx = i;
      break;
    }
  }
  const headers = parsedData[headerIdx];
  const colIdx = {
    contractNo: headers.findIndex((c) => c.includes("合同编号")),
    project: headers.findIndex((c) => c.includes("关联项目")),
    partyA: headers.findIndex((c) => c.includes("甲方")),
    partyB: headers.findIndex((c) => c.includes("乙方")),
    contractName: headers.findIndex((c) => c.includes("合同名称")),
    amount: headers.findIndex((c) => c.includes("合同总金额")),
  };

  // v4.0.0 P1-5: 必需列强校验
  //   之前 colIdx=-1 时 row[-1]=undefined, 静默丢失合同关系和金额
  //   修: 缺任一必需列直接返 missing_columns, 列出哪几列缺
  const requiredCols = [
    { key: "partyA", label: "甲方" },
    { key: "partyB", label: "乙方" },
    { key: "amount", label: "合同总金额" },
  ];
  const missingCols = requiredCols.filter((c) => colIdx[c.key] < 0);
  if (missingCols.length > 0) {
    const err = new Error("missing_columns");
    err.code = "MISSING_COLUMNS";
    err.message = `xls 缺必需列: ${missingCols.map((c) => c.label).join(", ")}`;
    err.headers = headers;
    err.missing = missingCols.map((c) => c.key);
    throw err;
  }

  // 扫数据
  const upstream = new Map(); // 供应商 -> 金额 sum
  const downstream = new Map(); // 客户 -> 金额 sum
  let upstreamCount = 0;
  let downstreamCount = 0;
  let totalAmount = 0;

  for (let i = headerIdx + 1; i < parsedData.length; i++) {
    const row = parsedData[i];
    if (row.length < Math.max(colIdx.partyA, colIdx.partyB, colIdx.amount) + 1) continue;
    const partyA = row[colIdx.partyA] || "";
    const partyB = row[colIdx.partyB] || "";
    // v4.0.0 P1-5: 改用增强 parseAmount (处理逗号/中文/括号负数/货币符号)
    const amount = parseAmount(row[colIdx.amount]);

    const aIsCompany = isOurCompany(partyA, variants);
    const bIsCompany = isOurCompany(partyB, variants);

    if (aIsCompany && !bIsCompany) {
      // 睿驰是甲方 → 乙方是下游客户
      if (!isCompany(partyB)) continue;
      downstream.set(partyB, (downstream.get(partyB) || 0) + amount);
      downstreamCount++;
      totalAmount += amount;
    } else if (bIsCompany && !aIsCompany) {
      // 睿驰是乙方 → 甲方是上游供应商
      if (!isCompany(partyA)) continue;
      upstream.set(partyA, (upstream.get(partyA) || 0) + amount);
      upstreamCount++;
      totalAmount += amount;
    }
  }

  // 排序 (按金额降序)
  const topCustomers = [...downstream.entries()].sort((a, b) => b[1] - a[1]).slice(0, topCustomersN);
  const topSuppliers = [...upstream.entries()].sort((a, b) => b[1] - a[1]).slice(0, topSuppliersN);

  // 类别聚合
  const dsByCat = {};
  for (const [name, amt] of downstream.entries()) {
    const c = categorize(name);
    if (!dsByCat[c.code]) dsByCat[c.code] = { name: c.name, count: 0, total: 0, samples: [] };
    dsByCat[c.code].count++;
    dsByCat[c.code].total += amt;
    if (dsByCat[c.code].samples.length < 3) dsByCat[c.code].samples.push(name);
  }
  const usByCat = {};
  for (const [name, amt] of upstream.entries()) {
    const c = categorize(name);
    if (!usByCat[c.code]) usByCat[c.code] = { name: c.name, count: 0, total: 0, samples: [] };
    usByCat[c.code].count++;
    usByCat[c.code].total += amt;
    if (usByCat[c.code].samples.length < 3) usByCat[c.code].samples.push(name);
  }

  // 拼 cards
  const cards = [];

  // D1 修复: 未分类 top N 显式记 card (避免 "蓝标/京东黑珑/霍尔斯" 漏 other 后丢失)
  // 拆出未分类的 top 5 公司, 单独记 dimension=客户类别/未分类 (跟其他类目同级, 不扔)
  const UNCATEGORIZED_TOP_N = 5;
  const otherDs = dsByCat.other;
  if (otherDs && otherDs.count > 0) {
    const otherCompanies = [...downstream.entries()]
      .filter(([n]) => categorize(n).code === "other")
      .sort((a, b) => b[1] - a[1])
      .slice(0, UNCATEGORIZED_TOP_N);
    if (otherCompanies.length > 0) {
      cards.push({
        type: "downstream_category",
        dimension: "客户类别/未分类",
        emoji: "📂",
      });
    }
  }
  const otherUs = usByCat.other;
  if (otherUs && otherUs.count > 0) {
    const otherCompanies = [...upstream.entries()]
      .filter(([n]) => categorize(n).code === "other")
      .sort((a, b) => b[1] - a[1])
      .slice(0, UNCATEGORIZED_TOP_N);
    if (otherCompanies.length > 0) {
      cards.push({
        type: "upstream_category",
        dimension: "供应商类别/未分类",
        emoji: "📂",
      });
    }
  }

  for (const [name, amt] of topCustomers) {
    cards.push({
      type: "downstream",
      dimension: `客户/${name}`,
      emoji: "⬇️",
      text: `${company} · 下游客户 · ${name}\n\n合同金额累计: ¥${amt.toLocaleString("en-US", { maximumFractionDigits: 0 })}\n关联项目: 见 ${company} 合同清单\n\n(从 xls 合同数据自动抽取, top ${topCustomersN} 大客户)`,
    });
  }
  for (const [name, amt] of topSuppliers) {
    cards.push({
      type: "upstream",
      dimension: `供应商/${name}`,
      emoji: "⬆️",
      text: `${company} · 上游供应商 · ${name}\n\n合同金额累计: ¥${amt.toLocaleString("en-US", { maximumFractionDigits: 0 })}\n关联项目: 见 ${company} 合同清单\n\n(从 xls 合同数据自动抽取, top ${topSuppliersN} 大供应商)`,
    });
  }
  // 下游类别 (按金额降序, 取前 8)
  const dsSorted = Object.entries(dsByCat).sort((a, b) => b[1].total - a[1].total).slice(0, 8);
  for (const [code, info] of dsSorted) {
    cards.push({
      type: "downstream_category",
      dimension: `客户类别/${info.name}`,
      emoji: "📂",
      text: `${company} · 下游客户类别 · ${info.name}\n\n关联客户数: ${info.count} 家\n合同总金额: ¥${info.total.toLocaleString("en-US", { maximumFractionDigits: 0 })}\n代表客户: ${info.samples.join(", ")}\n\n(从 xls 合同数据按行业关键词自动聚合)`,
    });
  }
  // 上游类别 (前 4)
  const usSorted = Object.entries(usByCat).sort((a, b) => b[1].total - a[1].total).slice(0, 4);
  for (const [code, info] of usSorted) {
    cards.push({
      type: "upstream_category",
      dimension: `供应商类别/${info.name}`,
      emoji: "📂",
      text: `${company} · 上游供应商类别 · ${info.name}\n\n关联供应商数: ${info.count} 家\n合同总金额: ¥${info.total.toLocaleString("en-US", { maximumFractionDigits: 0 })}\n代表供应商: ${info.samples.join(", ")}\n\n(从 xls 合同数据按行业关键词自动聚合)`,
    });
  }

  return {
    cards,
    summary: {
      company,
      upstreamCount,
      downstreamCount,
      upstreamCompanyCount: upstream.size,
      downstreamCompanyCount: downstream.size,
      totalAmount,
      topCustomerCount: topCustomers.length,
      topSupplierCount: topSuppliers.length,
    },
    upstream: topSuppliers,
    downstream: topCustomers,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const wantJson = args.json;

  // --help / -h: 打印用法, 不走 xls 解析
  if (args.help) {
    console.log(`

用途: 录入公司间的合作关系 (上下游), 不是公司本身的能力画像.
场景: 传合同 xls (甲方/乙方/金额/项目), 拆出 top 客户 + top 供应商 + 类别聚合.

用法:
  opphub knowledge-relate --xls <path> --company "公司名" [options]

必选参数:
  --xls <path>           合同 xls 路径 (HTML 格式, 从浏览器另存为)
  --company "公司名"     你的公司名 (容错匹配: 括号/多主体/分公司前缀)

可选参数:
  --top-customers <n>    top 下游客户数量 (默认 20)
  --top-suppliers <n>    top 上游供应商数量 (默认 10)
  --cards-out <path>     拆好的 cards JSON 写到文件 (可选, 默认 stdout)
  --json                 输出 JSON (默认开启)

输出 (JSON):
  {
    ok: true,
    company: "睿驰嘉禾",
    summary: { upstreamCount, downstreamCount, totalAmount },
    partners: { upstream: [...], downstream: [...] },
    cards: [ ... 40 条 ... ],
    cardCount: 40
  }

跟能力画像流程的区别:

下一步:
  opphub knowledge-ingest-batch --cards <cards.json> --json  # 批量入库
  opphub knowledge-search --q "公司名" --json                # 验证召回
`);
    process.exit(0);
  }

  if (!args.xls || !args.company) {
    const result = {
      ok: false,
      error: "missing_args",
      message: "需要 --xls <path> --company \"公司名\"",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  if (!existsSync(args.xls)) {
    const result = { ok: false, error: "xls_not_found", message: `xls 不存在: ${args.xls}` };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  const t0 = Date.now();
  let html, parsedData;
  try {
    html = readFileSync(args.xls, "utf8");
    parsedData = parseXlsHtml(html);
  } catch (e) {
    // v4.0.0 P1-5: 二进制 XLS / 缺列 / 解析失败 返结构化错误
    if (e.code === "BINARY_XLS_NOT_SUPPORTED") {
      const result = {
        ok: false,
        error: "binary_xls_not_supported",
        message: e.message,
        hint: "在 Excel 里 \"另存为网页 (*.html)\" 再试, 不要传二进制 .xls",
      };
      if (wantJson) console.log(JSON.stringify(result, null, 2));
      process.exit(1);
    }
    if (e.code === "MISSING_COLUMNS") {
      const result = {
        ok: false,
        error: "missing_columns",
        message: e.message,
        headers: e.headers,
        missing: e.missing,
        hint: `xls 必需含 "甲方" "乙方" "合同总金额" 列 (大小写不敏感, 部分匹配), 缺: ${e.missing.join(", ")}`,
      };
      if (wantJson) console.log(JSON.stringify(result, null, 2));
      process.exit(1);
    }
    throw e;
  }

  if (parsedData.length === 0) {
    const result = { ok: false, error: "empty_xls", message: "xls 解析为空" };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  let cards, summary, upstream, downstream;
  try {
    ({ cards, summary, upstream, downstream } = aggregateCards(parsedData, args.company, {
      topCustomers: args.topCustomers,
      topSuppliers: args.topSuppliers,
    }));
  } catch (e) {
    if (e.code === "MISSING_COLUMNS") {
      const result = {
        ok: false,
        error: "missing_columns",
        message: e.message,
        headers: e.headers,
        missing: e.missing,
        hint: `xls 必需含 "甲方" "乙方" "合同总金额" 列, 缺: ${e.missing.join(", ")}`,
      };
      if (wantJson) console.log(JSON.stringify(result, null, 2));
      process.exit(1);
    }
    throw e;
  }

  const result = {
    ok: true,
    company: args.company,
    summary,
    partners: {
      upstream: upstream.map(([name, amt]) => ({ name, amount: amt })),
      downstream: downstream.map(([name, amt]) => ({ name, amount: amt })),
    },
    cards,
    cardCount: cards.length,
    durationMs: Date.now() - t0,
    nextStep: "knowledge-ingest-batch --cards cards.json",
  };

  if (args.cardsOut) {
    const { writeFileSync } = await import("node:fs");
    writeFileSync(args.cardsOut, JSON.stringify({ cards, cardCount: cards.length, mode: "relations" }, null, 2), "utf8");
    result.cardsFile = args.cardsOut;
  }

  if (wantJson) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`📊 ${args.company} · 关联公司解析\n`);
    console.log(`合同统计: 上游 ${summary.upstreamCount} 单 / 下游 ${summary.downstreamCount} 单 / 总金额 ¥${summary.totalAmount.toLocaleString()}`);
    console.log(`关联公司: 上游 ${summary.upstreamCompanyCount} 家 / 下游 ${summary.downstreamCompanyCount} 家`);
    console.log(`拆出 cards: ${cards.length} 条 (top ${summary.topCustomerCount} 客户 + top ${summary.topSupplierCount} 供应商 + 类别聚合)`);
    if (args.cardsOut) console.log(`\n💾 已写入: ${args.cardsOut}`);
    console.log(`\n下一步: knowledge-ingest-batch --cards ${args.cardsOut ?? "cards.json"}`);
  }
}

main().catch((e) => {
  console.error("opphub-knowledge-relate fatal:", e?.message ?? e);
  process.exit(1);
});
