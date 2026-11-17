#!/usr/bin/env node
import { DEFAULT_BASE_URL, JARSY_REFERRAL_URL, PLATFORM_IDS, PLATFORMS, VERSION, endpoint } from "./platforms.mjs";
import { requestJson } from "./http.mjs";
import { loadReport, reportIndex, allowedReportUrl } from "./reports.mjs";
import { printSummary, printAssets, printDetail, printDiscovery } from "./jarsy-output.mjs";
import { printPlatformSummary, printPlatformList, printPlatformAsset, printFreshness } from "./platform-output.mjs";

const commonOptions = ["base", "json", "platform", "timeout-ms"];
const pageOptions = ["page", "page-size"];
const filters = [...new Set(Object.values(PLATFORMS).flatMap((p) => p.filters)), "sort"];

function usage() {
  console.log("Pre-IPO Research " + VERSION + " — public read-only query client\n");
  console.log("Usage: node query-preipo.mjs <command> [arguments] [options]");
  console.log("  platforms                         Show sources, identities and capabilities");
  console.log("  summary [--platform all|ID]       Snapshot context and timestamps");
  console.log("  search <keywords> [--platform all|ID] [filters]");
  console.log("  list [--platform ID] [filters]    Platform-specific screens");
  console.log("  detail <assetId> [--platform ID]  Captured profile / full prediction topics");
  console.log("  discover [--category NAME] [--tag NAME]...  Jarsy five opportunity rankings");
  console.log("  report <assetId> [--platform ID]  Read a registered published static report");
  console.log("\nDefault CLI platform: jarsy (legacy compatibility). Natural-language company research uses --platform all.");
  console.log("--json returns pure JSON. --base URL / PREIPO_API_BASE_URL overrides " + DEFAULT_BASE_URL);
  console.log("--timeout-ms N: 1–60000 (default 15000), covers headers and body.");
  console.log("--page N; --page-size N: Jarsy/all 6–48, other platforms 1–100 (default 12).");
  console.log("all is supported only by summary/search; search all accepts keywords and pagination, not platform filters.");
  for (const [id, config] of Object.entries(PLATFORMS)) {
    console.log("\n" + id + " — " + config.name + ": " + config.metrics);
    console.log("  Filters: " + config.filters.map((name) => "--" + name).join(" "));
    for (const [key, values] of Object.entries(config.enums)) console.log("  --" + key + " " + values.join("|"));
    console.log("  --sort " + config.sorts.join("|"));
  }
  console.log("\nJarsy --tag repeats with OR matching; --new maps to new=1 (30-day first-observed + current buy/sell).");
  console.log("Industry/category labels are exact values returned by that platform's summary.");
}

function parse(argv) {
  const options = {}, positional = [];
  const names = new Set([...commonOptions, ...pageOptions, ...filters]);
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") return { help: true };
    if (!arg.startsWith("--")) { positional.push(arg); continue; }
    const [name, inline] = arg.slice(2).split(/=(.*)/s, 2);
    if (!names.has(name)) throw new Error("Unsupported option --" + name);
    if (name === "json" || name === "new") {
      if (inline !== undefined) throw new Error("--" + name + " is a boolean flag, not a value.");
      options[name] = true;
      continue;
    }
    const val = inline ?? argv[++i];
    if (!val || val.startsWith("--")) throw new Error("--" + name + " requires a value.");
    if (name === "tag") options.tag = [...(options.tag || []), val];
    else options[name] = val;
  }
  return { options, command: positional.shift(), positional };
}

function validate(command, positional, options) {
  if (!["platforms", "summary", "search", "list", "detail", "discover", "report"].includes(command)) throw new Error("Unsupported command. Run with --help.");
  const platform = options.platform ?? "jarsy";
  if (platform !== "all" && !PLATFORM_IDS.includes(platform)) throw new Error("Unknown platform: " + platform);
  if (platform === "all" && !["summary", "search"].includes(command)) throw new Error("--platform all is only supported for summary/search.");
  if (command === "discover" && platform !== "jarsy") throw new Error("discover is Jarsy-only; use list with that platform's supported --sort.");
  if (["detail", "report"].includes(command) && (positional.length !== 1 || !positional[0].trim())) throw new Error(command + " requires exactly one assetId.");
  if (command === "search" && !positional.join(" ").trim()) throw new Error("search requires keywords.");
  if (!["search", "detail", "report"].includes(command) && positional.length) throw new Error(command + " does not accept positional arguments.");
  const allowed = new Set(commonOptions);
  if (["list", "search"].includes(command)) {
    pageOptions.forEach((name) => allowed.add(name));
    if (platform !== "all") [...PLATFORMS[platform].filters, "sort"].forEach((name) => allowed.add(name));
  }
  if (command === "discover") ["category", "tag"].forEach((name) => allowed.add(name));
  if (command === "platforms" && options.platform !== undefined) throw new Error("platforms always describes all platforms; omit --platform.");
  for (const key of Object.keys(options)) if (!allowed.has(key)) throw new Error("--" + key + " is not supported by " + command + " --platform " + platform);
  const config = PLATFORMS[platform];
  if (options.sort && !config.sorts.includes(options.sort)) throw new Error("Unsupported --sort for " + platform + ": " + options.sort);
  for (const [name, values] of Object.entries(config?.enums ?? {})) {
    if (options[name] && !values.includes(options[name])) throw new Error("--" + name + " must be " + values.join("|"));
  }
  const limits = { page: [1, platform === "jarsy" || platform === "all" ? 10000 : 1000000], "page-size": platform === "jarsy" || platform === "all" ? [6, 48] : [1, 100], "timeout-ms": [1, 60000] };
  for (const [key, [min, max]] of Object.entries(limits)) {
    if (options[key] !== undefined && (!/^\d+$/.test(options[key]) || Number(options[key]) < min || Number(options[key]) > max)) {
      throw new Error("--" + key + " must be an integer between " + min + " and " + max);
    }
  }
  return platform;
}

function baseUrl(candidate) {
  const url = new URL(candidate || process.env.PREIPO_API_BASE_URL || DEFAULT_BASE_URL);
  if (!["https:", "http:"].includes(url.protocol) || url.username || url.password || url.search || url.hash) throw new Error("--base must be an http(s) URL without credentials, query or fragment.");
  return url.toString().replace(/\/$/, "");
}

function paramsFor(command, positional, options) {
  const params = {};
  if (command === "search") params.q = positional.join(" ").trim();
  for (const key of [...filters, ...pageOptions]) {
    if (options[key] !== undefined) params[key === "page-size" ? "pageSize" : key] = key === "new" ? "1" : options[key];
  }
  return params;
}

function checkShape(command, data, platform) {
  if ((platform !== "jarsy" || data.platform !== undefined) && data.platform !== platform) {
    throw new Error("API platform mismatch; refusing to mix platform snapshots.");
  }
  if (["list", "search"].includes(command) && (!Array.isArray(data.items) || !Number.isInteger(data.total) || data.total < 0 || !Number.isInteger(data.page) || !Number.isInteger(data.pageSize))) {
    throw new Error("Invalid list response; expected items, total, page and pageSize.");
  }
  return data;
}

async function query(command, platform, positional, options, base) {
  const resource = ["search", "list"].includes(command) ? "assets" : command === "discover" ? "discovery" : command;
  const data = await requestJson(base, endpoint(platform, resource, positional[0]), paramsFor(command, positional, options), { timeoutMs: Number(options["timeout-ms"] || 15000) });
  return checkShape(command, data, platform);
}

async function printData(command, platform, data, base) {
  if (platform === "jarsy") {
    if (command === "summary") printSummary(data);
    else if (command === "discover") printDiscovery(data);
    else if (command === "detail") {
      // Retain both the market snapshot and the independently captured profile.
      if (data.companyName) printAssets({ items: [data], total: 1, page: 1, pageSize: 1 });
      printDetail(data);
      const entry = (await reportIndex()).reports[data.token?.trim().toUpperCase()];
      if (entry) console.log("已登记静态研报：" + allowedReportUrl(entry.href, base) + "；使用 report 读取报告截至日期。");
    } else printAssets(data);
    if (command !== "summary") console.log("全站导入时间请另查 summary；此输出中的标的/详情记录时间不能替代全站时间。");
  } else if (command === "summary") printPlatformSummary(platform, data);
  else if (command === "detail") {
    printFreshness(platform, data);
    printPlatformAsset(platform, data, base, { detail: true });
  } else printPlatformList(platform, data, base);
}

function printReport(data) {
  if (data.reportUrl) console.log("研报链接：" + data.reportUrl);
  if (data.status !== "success") {
    console.log(data.message || ("研报读取失败：" + data.error));
    return;
  }
  console.log(data.title + "\n报告截至：" + (data.asOf ?? "未提供") + "；静态版本：" + (data.version ?? "未提供"));
  console.log("以下为已发布报告的文本提取，非重新核验或新生成研报；其中数字不代表最新行情。\n");
  console.log(data.contentText);
  console.log("\n来源链接索引：");
  for (const source of data.sources) console.log(source.kind + " | " + source.label + " | " + source.url);
}

async function main() {
  const parsed = parse(process.argv.slice(2));
  if (parsed.help || !parsed.command) { usage(); if (!parsed.help) process.exitCode = 1; return; }
  const { command, positional, options } = parsed;
  const platform = validate(command, positional, options);
  const base = baseUrl(options.base);

  if (command === "platforms") {
    const data = { version: VERSION, baseUrl: base, platforms: PLATFORM_IDS.map((id) => ({ platform: id, ...PLATFORMS[id] })) };
    if (options.json) console.log(JSON.stringify(data, null, 2));
    else for (const entry of data.platforms) console.log(entry.name + " (" + entry.platform + ") — " + entry.cadence + "\n标识：" + entry.identity + "\n指标：" + entry.metrics + "\n来源：" + entry.sourceUrl + "\n");
  } else if (command === "report") {
    const detail = await query("detail", platform, positional, options, base);
    const data = await loadReport(platform, positional[0], detail, base, { timeoutMs: Number(options["timeout-ms"] || 15000) });
    if (data.status === "error") process.exitCode = 1;
    if (options.json) console.log(JSON.stringify(data, null, 2));
    else printReport(data);
  } else if (platform === "all") {
    const results = await Promise.all(PLATFORM_IDS.map(async (id) => {
      try { return { platform: id, status: "success", data: await query(command, id, positional, options, base) }; }
      catch (error) { return { platform: id, status: "error", error: error.message }; }
    }));
    const partial = results.some((entry) => entry.status === "error");
    if (partial) process.exitCode = 1;
    const payload = { scope: "all", command, partial, results };
    if (options.json) console.log(JSON.stringify(payload, null, 2));
    else {
      console.log("五个平台分别查询；默认状态和指标口径不同，不合并排名或金额。");
      for (const result of results) {
        console.log("\n=== " + PLATFORMS[result.platform].name + " ===");
        if (result.status === "error") console.log("查询失败：" + result.error + "（不代表无标的）");
        else await printData(command, result.platform, result.data, base);
      }
    }
  } else {
    const data = await query(command, platform, positional, options, base);
    if (options.json) console.log(JSON.stringify(data, null, 2));
    else await printData(command, platform, data, base);
  }
  if (!options.json) {
    console.log("\n仅供研究参考，不构成投资建议；来源页面与下列独立 Jarsy 访问入口用途不同。");
    console.log("访问 Jarsy：" + JARSY_REFERRAL_URL);
  }
}

main().catch((error) => {
  console.error("Error: " + error.message);
  process.exitCode = 1;
});
