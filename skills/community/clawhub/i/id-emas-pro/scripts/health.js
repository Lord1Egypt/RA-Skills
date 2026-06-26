// ============================================
// scripts/health.js — Health check semua scraper
// Jalankan: node scripts/main.js health
// ============================================

import { getBrandsForTier } from "../config/brands.js";
import { scrapeBrand } from "./scraper.js";
import { getCacheInfo } from "./cache.js";

const TIMEOUT_MS = 15_000;

/**
 * Test satu brand dengan timeout
 */
async function checkBrand(brand) {
  const start = Date.now();
  try {
    const result = await Promise.race([
      scrapeBrand(brand),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Timeout 15s")), TIMEOUT_MS)
      ),
    ]);

    const latencyMs = Date.now() - start;

    if (result.success) {
      return {
        id: brand.id,
        name: brand.name,
        status: "ok",
        latencyMs,
        buyPrice: result.data.buyPrice,
        sourceUsed: result.sourceUsed,
        cacheStatus: result.cacheStatus,
        note: result.data.note,
      };
    } else {
      return {
        id: brand.id,
        name: brand.name,
        status: "fail",
        latencyMs,
        error: result.error,
      };
    }
  } catch (err) {
    return {
      id: brand.id,
      name: brand.name,
      status: "error",
      latencyMs: Date.now() - start,
      error: err.message,
    };
  }
}

/**
 * Jalankan health check semua brand
 */
export async function runHealthCheck() {
  const brands = getBrandsForTier("ai"); // cek semua brand
  const cacheInfo = await getCacheInfo();

  console.log(`🏥 Health Check — ${new Date().toLocaleString("id-ID")}`);
  console.log(`   Mengecek ${brands.length} brand...\n`);

  const results = await Promise.all(brands.map(checkBrand));

  let ok = 0, fail = 0;
  const fmt = (n) => n ? `Rp ${n.toLocaleString("id-ID")}` : "-";

  for (const r of results) {
    if (r.status === "ok") {
      ok++;
      const cache = cacheInfo[r.id];
      const cacheAge = cache ? `cache: ${cache.ageHours}h` : "no cache";
      console.log(
        `✅ ${r.name.padEnd(25)} ${fmt(r.buyPrice).padStart(16)}  ` +
        `${r.latencyMs}ms  [${r.sourceUsed ?? "?"}]  (${cacheAge})`
      );
      if (r.note) console.log(`   ⚠️  ${r.note}`);
    } else {
      fail++;
      const cache = cacheInfo[r.id];
      const fallback = cache
        ? `fallback cache tersedia (${cache.ageHours}h lalu)`
        : "tidak ada cache";
      console.log(
        `❌ ${r.name.padEnd(25)} GAGAL  ${r.latencyMs}ms`
      );
      console.log(`   Error   : ${r.error}`);
      console.log(`   Cache   : ${fallback}`);
    }
  }

  console.log(`\n${"─".repeat(60)}`);
  console.log(`Hasil: ${ok}/${brands.length} OK, ${fail} gagal`);

  if (fail > 0) {
    console.log(`\n💡 Tips:`);
    console.log(`   - Scraper gagal masih punya stale cache sebagai fallback`);
    console.log(`   - Cek koneksi internet atau coba lagi nanti`);
    if (fail === brands.length) {
      console.log(`   - Semua scraper gagal! Cek apakah ada blokir IP/Cloudflare`);
    }
  }

  return { ok, fail, total: brands.length, results };
}
