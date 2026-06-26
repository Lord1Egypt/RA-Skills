// src/cli.ts
import { Command } from "commander";
import { readFileSync as readFileSync4 } from "fs";
import { fileURLToPath as fileURLToPath2 } from "url";
import { dirname as dirname2, resolve as resolve4 } from "path";

// src/lib/api.ts
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";
var pkg = { version: "1.0.0", name: "seap-shopping-tools" };
try {
  const __dirname2 = dirname(fileURLToPath(import.meta.url));
  pkg = JSON.parse(readFileSync(resolve(__dirname2, "../../package.json"), "utf-8"));
} catch {
}
function getServer() {
  return "https://with-ai.cn:38080";
}
function getVersion() {
  return pkg.version.replace("-", ".");
}
async function post(url, data) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 3e4);
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { ts: Date.now().toString(), "x-trace-id": Math.random().toString(36).substring(2, 9), "Content-Type": "application/json" },
      body: JSON.stringify({ version: getVersion(), pkgName: pkg.name, data }),
      signal: controller.signal
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    return await res.json();
  } finally {
    clearTimeout(timeout);
  }
}
async function queryGoods(intent, authCode) {
  const url = `${getServer()}/hubagent/intention/goods/query`;
  const data = { queryGoodsIntention: intent, authCode };
  const result = await post(url, data);
  if (result.code !== "0000000000") {
    throw new Error(result.desc ?? `API error: ${result.code}`);
  }
  return result;
}
async function placeOrder(data) {
  const url = `${getServer()}/hubagent/intention/order/schedule`;
  const result = await post(url, data);
  if (result.code !== "0000000000") {
    throw new Error(result.desc ?? `API error: ${result.code}`);
  }
  return result;
}

// src/lib/config.ts
import * as fs from "fs";
import * as path from "path";
var CONFIG_PATH = path.resolve(process.cwd(), "seap.config.json");
function readConfig() {
  if (!fs.existsSync(CONFIG_PATH)) return {};
  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, "utf-8"));
  } catch {
    return {};
  }
}
function resolveAuthCode() {
  const envCode = process.env.SEAP_SHOPPING_AUTH_CODE;
  if (envCode) return envCode;
  const cfg = readConfig();
  return cfg.authCode ?? null;
}
function resolveAddress() {
  const cfg = readConfig();
  return cfg.addresses?.[0] ?? null;
}

// src/lib/cache.ts
import * as fs2 from "fs";
import * as path2 from "path";
function cachePath(sessionId) {
  return path2.resolve(process.cwd(), "seap-cache", `${sessionId}.json`);
}
function writeCache(sessionId, data) {
  const dir = path2.resolve(process.cwd(), "seap-cache");
  try {
    fs2.mkdirSync(dir, { recursive: true });
    fs2.writeFileSync(cachePath(sessionId), JSON.stringify(data, null, 2));
  } catch (err) {
    throw new Error(`Failed to write cache for sessionId ${sessionId}: ${err instanceof Error ? err.message : String(err)}`);
  }
}
function readCache(sessionId) {
  const p = cachePath(sessionId);
  if (!fs2.existsSync(p)) return null;
  try {
    const parsed = JSON.parse(fs2.readFileSync(p, "utf-8"));
    if (typeof parsed !== "object" || parsed === null || !("searchResult" in parsed)) return null;
    return parsed;
  } catch {
    return null;
  }
}
function findSkuInCache(cache, skuId) {
  const goods = cache.searchResult.data?.goods ?? [];
  for (const good of goods) {
    for (const spu of good.goods) {
      for (const sku of spu.skuList) {
        if (sku.skuId === skuId) {
          return { sku, mercInfoId: good.mercInfo.id };
        }
      }
    }
  }
  return null;
}

// src/commands/search.ts
function goodsToMarkdown(goods) {
  let md = "# \u5546\u54C1\u641C\u7D22\u7ED3\u679C\n\n";
  for (const good of goods) {
    for (const spu of good.goods) {
      for (const sku of spu.skuList) {
        md += `## ${sku.name}
`;
        md += `- **SKU**: ${sku.skuId}
`;
        md += `- **\u4EF7\u683C**: \xA5${(sku.price / 100).toFixed(2)}
`;
        md += "\n";
      }
    }
  }
  return md;
}
async function runSearch(options) {
  const authCode = resolveAuthCode();
  if (!authCode) {
    process.stderr.write("Error: SEAP_SHOPPING_AUTH_CODE not set and authCode not in config\n");
    process.exit(1);
  }
  let result;
  try {
    result = await queryGoods(options.intent, authCode);
  } catch (err) {
    console.log(err);
    process.stderr.write(`Error: ${err.message}
`);
    process.exit(1);
  }
  try {
    writeCache(options.sessionId, { searchResult: result });
  } catch (err) {
    process.stderr.write(`Error: ${err.message}
`);
    process.exit(1);
  }
  const goods = result.data?.goods ?? [];
  if (options.format === "json") {
    process.stdout.write(JSON.stringify(result, null, 2) + "\n");
  } else {
    process.stdout.write(goodsToMarkdown(goods));
  }
}

// src/commands/aipay.ts
async function runAipay(options) {
  const authCode = resolveAuthCode();
  if (!authCode) {
    process.stderr.write("Error: SEAP_SHOPPING_AUTH_CODE not set and authCode not in config\n");
    process.exit(1);
  }
  const cache = readCache(options.sessionId);
  if (!cache) {
    process.stderr.write(`Error: Run search first for sessionId: ${options.sessionId}
`);
    process.exit(1);
  }
  const found = findSkuInCache(cache, options.skuId);
  if (!found) {
    process.stderr.write(
      `Error: SKU ${options.skuId} not found in cache for sessionId: ${options.sessionId}
`
    );
    process.exit(1);
  }
  const address = resolveAddress();
  if (!address) {
    process.stderr.write("Error: Please configure addresses in seap.config.json\n");
    process.exit(1);
  }
  const mercInfoId = options.mercInfoId ?? found.mercInfoId;
  const quantity = parseInt(options.quantity, 10);
  const data = {
    scheduleBuyIntention: {
      buyIntention: {
        uid: "40086000101902819",
        mercInfo: { id: mercInfoId },
        skuId: options.skuId,
        quantity,
        paymentService: "HUAWEIPAY",
        shippingAddress: address,
        sign: "1"
      },
      paymentIntention: {
        uid: "40086000101902819",
        deviceId: "VC724E1D5DBF513D7CAA39F745A6189649BFC66FE0BACC5EBA09E3CF34B93ABC",
        amount: "1111",
        payContractId: "1111",
        sing: "1111"
        // preserved as-is from server contract (typo in API spec)
      },
      sign: "111",
      certificate: "111"
    },
    authCode
  };
  let result;
  try {
    result = await placeOrder(data);
  } catch (err) {
    process.stderr.write(`Error: ${err.message}
`);
    process.exit(1);
  }
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

// src/cli.ts
var __dirname = dirname2(fileURLToPath2(import.meta.url));
var pkg2 = JSON.parse(readFileSync4(resolve4(__dirname, "../package.json"), "utf-8"));
var program = new Command();
program.name("seap-cli").description("SEAP CLI for OpenClaw skills").version(pkg2.version);
program.command("search").description("Search for goods").requiredOption("--sessionId <sessionId>", "Session ID").requiredOption("--intent <intent>", "Search intent").option("--format <format>", "Output format (md or json)", "md").action((opts) => runSearch(opts));
program.command("aipay").description("Complete purchase for a product").requiredOption("--sessionId <sessionId>", "Session ID").requiredOption("--skuId <skuId>", "SKU ID to purchase").requiredOption("--quantity <quantity>", "Product quantity").option("--mercInfoId <mercInfoId>", "Merchant information ID (extracted from cache if omitted)").action((opts) => runAipay(opts));
program.parse();
