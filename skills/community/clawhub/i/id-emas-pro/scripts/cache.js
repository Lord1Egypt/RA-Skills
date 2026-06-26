// ============================================
// scripts/cache.js — Price cache & stale fallback
//
// Menyimpan harga terakhir per brand ke .data/cache.json
// Kalau semua scraper gagal, return data stale dengan warning
// ============================================

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const CACHE_FILE = path.join(__dirname, "../.data/cache.json");

// Harga dianggap "fresh" kalau < 4 jam
const FRESH_TTL_MS = 4 * 60 * 60 * 1000;

// Harga dianggap "usable stale" kalau < 7 hari
const STALE_TTL_MS = 7 * 24 * 60 * 60 * 1000;

async function readCache() {
  try {
    const raw = await fs.readFile(CACHE_FILE, "utf-8");
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

async function writeCache(data) {
  await fs.mkdir(path.dirname(CACHE_FILE), { recursive: true });
  await fs.writeFile(CACHE_FILE, JSON.stringify(data, null, 2));
}

/**
 * Simpan hasil scrape ke cache
 */
export async function saveToCache(brandId, priceData) {
  const cache = await readCache();
  cache[brandId] = {
    ...priceData,
    cachedAt: new Date().toISOString(),
    scrapedAt: priceData.scrapedAt?.toISOString?.() ?? new Date().toISOString(),
  };
  await writeCache(cache);
}

/**
 * Ambil dari cache
 * Returns: { data, status: "fresh" | "stale" | "expired" | "miss" }
 */
export async function getFromCache(brandId) {
  const cache = await readCache();
  const entry = cache[brandId];

  if (!entry) return { data: null, status: "miss" };

  const age = Date.now() - new Date(entry.cachedAt).getTime();

  if (age < FRESH_TTL_MS) return { data: entry, status: "fresh" };
  if (age < STALE_TTL_MS) return { data: entry, status: "stale" };
  return { data: entry, status: "expired" };
}

/**
 * Wrapper untuk scraper — auto-cache hasil, fallback ke stale kalau gagal
 */
export async function scrapeWithCache(brandId, scraperFn) {
  // Coba scrape fresh
  try {
    const result = await scraperFn();
    if (result.success && result.data) {
      await saveToCache(brandId, result.data);
      return { ...result, cacheStatus: "fresh" };
    }
  } catch (err) {
    console.error(`⚠️  Scraper ${brandId} error: ${err.message}`);
  }

  // Scraper gagal — coba dari cache
  const { data, status } = await getFromCache(brandId);

  if (status === "miss") {
    return {
      success: false,
      error: `Scraper gagal dan tidak ada cache untuk ${brandId}`,
      cacheStatus: "miss",
    };
  }

  if (status === "expired") {
    return {
      success: false,
      error: `Scraper gagal dan cache sudah expired (>7 hari) untuk ${brandId}`,
      cacheStatus: "expired",
    };
  }

  // Return stale data dengan warning
  const ageHours = Math.round(
    (Date.now() - new Date(data.cachedAt).getTime()) / 3_600_000
  );

  return {
    success: true,
    data: {
      ...data,
      scrapedAt: new Date(data.scrapedAt),
    },
    cacheStatus: status,
    staleWarning: `⚠️ Data dari cache (${ageHours} jam lalu) — scraper sedang tidak bisa diakses`,
    sourceUsed: `cache:${brandId}`,
  };
}

/**
 * Info cache semua brand
 */
export async function getCacheInfo() {
  const cache = await readCache();
  const info = {};

  for (const [brandId, entry] of Object.entries(cache)) {
    const age = Date.now() - new Date(entry.cachedAt).getTime();
    const ageHours = Math.round(age / 3_600_000);
    info[brandId] = {
      brand: entry.brand,
      cachedAt: entry.cachedAt,
      ageHours,
      status: age < FRESH_TTL_MS ? "fresh" : age < STALE_TTL_MS ? "stale" : "expired",
      buyPrice: entry.buyPrice,
      sellPrice: entry.sellPrice,
    };
  }

  return info;
}
