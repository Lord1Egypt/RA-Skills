#!/usr/bin/env node
// ============================================
// scripts/main.js — CLI entry point
// Usage: node scripts/main.js <command> [options]
//
// Commands:
//   price         Harga emas satu brand
//   compare       Bandingkan semua brand
//   history       Histori harga N hari
//   alert set     Buat alert
//   alert list    Lihat alert
//   alert delete  Hapus alert
//   alert check   Cron: cek semua alert
//   portfolio     Kelola portfolio
//   ai-analysis   Analisis AI dengan histori
//   health        Health check semua scraper
// ============================================

import { parseArgs } from "node:util";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = path.resolve(__dirname, "..");

const { positionals, values } = parseArgs({
  allowPositionals: true,
  options: {
    brand:     { type: "string", default: "antam" },
    userId:    { type: "string", default: "default" },
    condition: { type: "string" },
    price:     { type: "string" },
    type:      { type: "string", default: "buy" },
    id:        { type: "string" },
    tier:      { type: "string", default: "free" },
    days:      { type: "string", default: "7" },
    grams:     { type: "string" },
    buyPrice:  { type: "string" },
    buyDate:   { type: "string" },
  },
});

const [command, subcommand] = positionals;

try {
  switch (command) {
    case "price":     await runPrice(values); break;
    case "compare":   await runCompare(values); break;
    case "history":   await runHistory(values); break;
    case "alert":     await runAlert(subcommand, values); break;
    case "portfolio": await runPortfolio(subcommand, values); break;
    case "ai-analysis": await runAiAnalysis(values); break;
    case "health":    await runHealth(); break;
    default:
      console.error(`❌ Perintah tidak dikenal: "${command}"`);
      console.error(`Tersedia: price, compare, history, alert, portfolio, ai-analysis, health`);
      process.exit(1);
  }
} catch (err) {
  console.error(`❌ Error: ${err.message}`);
  process.exit(1);
}

// ---- Handlers ----

async function runPrice({ brand, tier }) {
  const { scrapeBrand } = await import("./scraper.js");
  const { getBrandById } = await import("../config/brands.js");
  const { recordPrice } = await import("./history.js");

  const brandConfig = getBrandById(brand);
  if (!brandConfig) { console.error(`❌ Brand "${brand}" tidak ditemukan`); process.exit(1); }

  const result = await scrapeBrand(brandConfig);

  if (!result.success) { console.error(`❌ Gagal: ${result.error}`); process.exit(1); }

  const { data } = result;
  await recordPrice(brand, data).catch(() => {}); // simpan ke histori, silent fail

  const fmt = (n) => `Rp ${n.toLocaleString("id-ID")}`;
  const time = new Date(data.scrapedAt).toLocaleString("id-ID");

  console.log(`💰 Harga Emas ${data.brand}`);
  console.log(`📅 ${time}`);
  console.log(``);
  console.log(`Beli  : ${fmt(data.buyPrice)}/gram`);
  console.log(`Jual  : ${fmt(data.sellPrice)}/gram`);
  console.log(`Spread: ${fmt(data.buyPrice - data.sellPrice)}`);
  if (result.staleWarning) console.log(`\n${result.staleWarning}`);
  if (data.note) console.log(`\n⚠️  ${data.note}`);
  console.log(`\n_Sumber: ${data.source}_`);
}

async function runCompare({ tier }) {
  const { scrapeAll } = await import("./scraper.js");
  const { getBrandsForTier } = await import("../config/brands.js");
  const { recordPrice } = await import("./history.js");

  const brands = getBrandsForTier(tier);
  console.log(`⏳ Mengambil harga ${brands.length} brand...\n`);

  const results = await scrapeAll(brands);
  const fmt = (n) => `Rp ${n.toLocaleString("id-ID")}`;

  console.log(`📊 Perbandingan Harga Emas — ${new Date().toLocaleString("id-ID")}`);
  console.log(`${"Brand".padEnd(25)} ${"Beli/gram".padStart(16)} ${"Jual/gram".padStart(16)}  Sumber`);
  console.log("─".repeat(75));

  for (const brand of brands) {
    const r = results.get(brand.id);
    if (r?.success && r.data) {
      await recordPrice(brand.id, r.data).catch(() => {});
      const stale = r.cacheStatus === "stale" ? " ⚠️" : "";
      console.log(
        `${brand.name.padEnd(25)} ${fmt(r.data.buyPrice).padStart(16)} ${fmt(r.data.sellPrice).padStart(16)}  [${r.sourceUsed ?? "?"}]${stale}`
      );
    } else {
      console.log(`${brand.name.padEnd(25)} ${"(gagal)".padStart(16)} ${"".padStart(16)}  ❌ ${r?.error ?? "?"}`);
    }
  }
}

async function runHistory({ brand, days }) {
  const { getPriceHistory, calcStats, formatHistorySummary } = await import("./history.js");
  const { getBrandById } = await import("../config/brands.js");

  const brandConfig = getBrandById(brand);
  const brandName = brandConfig?.name ?? brand;

  const entries = await getPriceHistory(brand, parseInt(days));
  const stats = calcStats(entries);

  console.log(formatHistorySummary(brandName, entries, stats));
}

async function runAlert(subcommand, { userId, brand, condition, price, type, id }) {
  const { AlertManager, ChatNotifier, formatAlertList } = await import("./alerts.js");
  const { FileAlertStorage } = await import("./storage.js");

  const storage = new FileAlertStorage(path.join(SKILL_DIR, ".data", "alerts.json"));
  const notifier = new ChatNotifier(async (uid, msg) => {
    console.log(`[NOTIFY:${uid}]\n${msg}`);
  });
  const manager = new AlertManager(storage, notifier);

  switch (subcommand) {
    case "set": {
      if (!condition || !price) { console.error("❌ --condition dan --price wajib"); process.exit(1); }
      const alert = await manager.createAlert(userId, {
        brand,
        condition,
        targetPrice: parseInt(price.replace(/[^0-9]/g, ""), 10),
        type,
      });
      const fmt = (n) => `Rp ${n.toLocaleString("id-ID")}`;
      console.log(`✅ Alert dibuat!`);
      console.log(`ID    : ${alert.id}`);
      console.log(`Brand : ${alert.brand} — harga ${alert.type} ${alert.condition} ${fmt(alert.targetPrice)}`);
      break;
    }
    case "list": {
      const alerts = await manager.listAlerts(userId);
      console.log(formatAlertList(alerts));
      break;
    }
    case "delete": {
      if (!id) { console.error("❌ --id wajib"); process.exit(1); }
      await manager.deleteAlert(userId, id);
      console.log(`✅ Alert ${id} dihapus`);
      break;
    }
    case "check": {
      const { scrapeAll } = await import("./scraper.js");
      const { getBrandsForTier } = await import("../config/brands.js");

      const brands = getBrandsForTier("ai");
      const results = await scrapeAll(brands);
      const priceMap = new Map();
      for (const [brandId, r] of results) {
        if (r.success && r.data) priceMap.set(brandId, r.data);
      }

      const userIds = userId === "all"
        ? await storage.getAllUserIds()
        : [userId];

      let totalTriggered = 0;
      for (const uid of userIds) {
        const triggered = await manager.checkPrices(uid, priceMap);
        totalTriggered += triggered.length;
      }

      console.log(`✅ Cron check: ${userIds.length} user, ${priceMap.size} brand, ${totalTriggered} alert triggered.`);
      break;
    }
    default:
      console.error(`❌ Subcommand alert tidak dikenal: "${subcommand}"`);
      process.exit(1);
  }
}

async function runPortfolio(subcommand, { userId, brand, grams, buyPrice, buyDate, id, tier }) {
  const { PortfolioManager, formatPortfolioSnapshot } = await import("./portfolio.js");
  const { scrapeAll } = await import("./scraper.js");
  const { getBrandsForTier } = await import("../config/brands.js");

  const pm = new PortfolioManager();

  switch (subcommand) {
    case "add": {
      if (!brand || !grams || !buyPrice) {
        console.error("❌ --brand, --grams, --buyPrice wajib");
        process.exit(1);
      }
      const entry = await pm.addEntry(userId, { brand, grams, buyPrice, buyDate });
      console.log(`✅ Emas ditambahkan ke portfolio!`);
      console.log(`   ${entry.grams}g ${entry.brand} @ Rp ${entry.buyPrice.toLocaleString("id-ID")}/g`);
      console.log(`   Total nilai beli: Rp ${(entry.grams * entry.buyPrice).toLocaleString("id-ID")}`);
      break;
    }
    case "remove": {
      if (!id) { console.error("❌ --id wajib"); process.exit(1); }
      await pm.removeEntry(userId, id);
      console.log(`✅ Entry dihapus`);
      break;
    }
    case "show":
    default: {
      const brands = getBrandsForTier(tier);
      const results = await scrapeAll(brands);
      const priceMap = new Map();
      for (const [brandId, r] of results) {
        if (r.success && r.data) priceMap.set(brandId, r.data);
      }
      const snapshot = await pm.calcSnapshot(userId, priceMap);
      console.log(formatPortfolioSnapshot(snapshot));
      break;
    }
  }
}

async function runAiAnalysis({ userId, tier, brand, days }) {
  if (tier !== "ai") {
    console.log(`🔒 Fitur analisis AI membutuhkan tier AI ($49/bulan).`);
    process.exit(0);
  }

  const kimiKey = process.env.KIMI_API_KEY;
  if (!kimiKey) { console.error("❌ KIMI_API_KEY tidak ditemukan"); process.exit(1); }

  const { analyzeWithHistory } = await import("./ai-analysis.js");
  const { GoldAIAnalyst } = await import("./ai-analysis.js");
  const { scrapeAll } = await import("./scraper.js");
  const { getBrandsForTier } = await import("../config/brands.js");
  const { getPriceHistory } = await import("./history.js");

  const brands = getBrandsForTier("free");
  const results = await scrapeAll(brands);
  const prices = [...results.values()].filter((r) => r.success && r.data).map((r) => r.data);

  if (prices.length === 0) { console.error("❌ Tidak bisa ambil harga"); process.exit(1); }

  // Ambil histori 30 hari untuk konteks AI
  const history = await getPriceHistory(brand ?? "antam", parseInt(days ?? "30"));

  console.log(`🤖 Menganalisis dengan Kimi 2.5 (konteks ${history.length} hari histori)...`);
  const result = await analyzeWithHistory(prices, history);
  console.log(GoldAIAnalyst.formatAnalysis(result));
}

async function runHealth() {
  const { runHealthCheck } = await import("./health.js");
  await runHealthCheck();
}
