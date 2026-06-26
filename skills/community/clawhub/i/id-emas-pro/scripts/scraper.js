// ============================================
// scripts/scraper.js — Multi-brand scraper
// 
// Brand yang didukung:
//   antam    — 3 source fallback (emasantam.id, logammulia.com, anekalogam.co.id)
//   pegadaian — sahabat.pegadaian.co.id/harga-emas (Galeri24, UBS, Antam)
//   treasury  — treasury.id
//   tamasia   — tamasia.co.id
//   bbri      — estimasi dari Antam + markup
// ============================================

// ---- HTTP helper ----

async function fetchHTML(url, extraHeaders = {}) {
  const res = await fetch(url, {
    headers: {
      "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
      Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
      "Cache-Control": "no-cache",
      ...extraHeaders,
    },
    signal: AbortSignal.timeout(12_000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} dari ${url}`);
  return res.text();
}

export function parseIDR(raw) {
  if (!raw) return NaN;
  return parseInt(String(raw).replace(/[^0-9]/g, ""), 10);
}

export function isValidGoldPrice(n) {
  return Number.isFinite(n) && n > 500_000 && n < 10_000_000;
}

function detectCloudflare(html) {
  return (
    html.includes("cf-browser-verification") ||
    html.includes("Just a moment") ||
    html.includes("Enable JavaScript and cookies")
  );
}

// ============================================================
// ANTAM — 3-source fallback chain
// ============================================================

async function scrapeEmasAntamId() {
  const html = await fetchHTML("https://emasantam.id/harga-emas-antam-harian/");
  const matches = [...html.matchAll(/Rp\.?\s*([\d]{1,2}\.[\d]{3}\.[\d]{3})/g)]
    .map((m) => parseIDR(m[1]))
    .filter(isValidGoldPrice);

  if (matches.length === 0) throw new Error("emasantam.id: tidak ada harga");

  const buyPrice = matches[0];
  const sellPrice = Math.round(buyPrice * 0.985); // estimasi buyback ~1.5%

  return {
    brand: "Logam Mulia Antam",
    buyPrice,
    sellPrice,
    unit: "gram",
    currency: "IDR",
    scrapedAt: new Date(),
    source: "https://emasantam.id/harga-emas-antam-harian/",
    note: "Harga buyback adalah estimasi",
  };
}

async function scrapeLogamMulia() {
  const html = await fetchHTML(
    "https://www.logammulia.com/id/harga-emas-hari-ini",
    { Referer: "https://www.logammulia.com/id" }
  );
  if (detectCloudflare(html)) throw new Error("logammulia.com: diblokir Cloudflare");

  const prices = [...html.matchAll(/([\d]{1,2}[.,][\d]{3}[.,][\d]{3})/g)]
    .map((m) => parseIDR(m[1]))
    .filter(isValidGoldPrice)
    .sort((a, b) => b - a);

  if (prices.length < 2) throw new Error("logammulia.com: tidak cukup data");

  return {
    brand: "Logam Mulia Antam",
    buyPrice: prices[0],
    sellPrice: prices[1],
    unit: "gram",
    currency: "IDR",
    scrapedAt: new Date(),
    source: "https://www.logammulia.com/id/harga-emas-hari-ini",
  };
}

async function scrapeAnekaLogam() {
  const html = await fetchHTML("https://anekalogam.co.id/id");
  const prices = [...html.matchAll(/([\d]{1,2}[.,][\d]{3}[.,][\d]{3})/g)]
    .map((m) => parseIDR(m[1]))
    .filter(isValidGoldPrice)
    .sort((a, b) => b - a);

  if (prices.length < 2) throw new Error("anekalogam.co.id: tidak cukup data");

  return {
    brand: "Logam Mulia Antam",
    buyPrice: prices[0],
    sellPrice: prices[1],
    unit: "gram",
    currency: "IDR",
    scrapedAt: new Date(),
    source: "https://anekalogam.co.id/id",
  };
}

async function scrapeAntam() {
  const sources = [
    { name: "emasantam.id",     fn: scrapeEmasAntamId },
    { name: "logammulia.com",   fn: scrapeLogamMulia  },
    { name: "anekalogam.co.id", fn: scrapeAnekaLogam  },
  ];

  const errors = [];
  for (const s of sources) {
    try {
      const data = await s.fn();
      if (!isValidGoldPrice(data.buyPrice) || !isValidGoldPrice(data.sellPrice)) {
        throw new Error("Harga tidak valid");
      }
      return { success: true, data, sourceUsed: s.name };
    } catch (err) {
      const msg = `[${s.name}] ${err.message}`;
      errors.push(msg);
      console.error(`⚠️  ${msg}`);
    }
  }

  return { success: false, error: `Semua sumber gagal:\n${errors.join("\n")}` };
}

// ============================================================
// PEGADAIAN — sahabat.pegadaian.co.id
// Menjual: Galeri24, UBS, dan kadang Antam
// Target: ambil harga 1 gram Galeri24 sebagai representasi
// ============================================================

async function scrapePegadaian() {
  const html = await fetchHTML("https://sahabat.pegadaian.co.id/harga-emas", {
    Referer: "https://sahabat.pegadaian.co.id",
  });

  if (detectCloudflare(html)) throw new Error("Pegadaian: diblokir Cloudflare");

  // Cari harga Galeri24 1 gram — biasanya brand termurah di Pegadaian
  // Pattern: angka sekitar 2.7–3.2 juta untuk 1 gram
  const galeri24Match = html.match(
    /[Gg]aleri\s*24[^<]{0,200}([\d]{1,2}[.,][\d]{3}[.,][\d]{3})/
  );

  // Fallback: ambil semua harga valid, ambil yang paling rendah (biasanya Galeri24)
  const allPrices = [...html.matchAll(/([\d]{1,2}[.,][\d]{3}[.,][\d]{3})/g)]
    .map((m) => parseIDR(m[1]))
    .filter(isValidGoldPrice)
    .sort((a, b) => a - b); // ascending — ambil terendah

  if (allPrices.length === 0 && !galeri24Match) {
    throw new Error("Pegadaian: tidak ada harga ditemukan");
  }

  const buyPrice = galeri24Match
    ? parseIDR(galeri24Match[1])
    : allPrices[0];

  // Buyback Pegadaian biasanya ~94% dari harga jual
  const sellPrice = Math.round(buyPrice * 0.94);

  if (!isValidGoldPrice(buyPrice)) throw new Error("Pegadaian: harga tidak valid");

  return {
    success: true,
    data: {
      brand: "Pegadaian (Galeri24)",
      buyPrice,
      sellPrice,
      unit: "gram",
      currency: "IDR",
      scrapedAt: new Date(),
      source: "https://sahabat.pegadaian.co.id/harga-emas",
      note: "Harga buyback adalah estimasi ~94%",
    },
    sourceUsed: "sahabat.pegadaian.co.id",
  };
}

// ============================================================
// TREASURY — treasury.id
// Emas digital berbasis BAPPEBTI
// ============================================================

async function scrapeTreasury() {
  const html = await fetchHTML("https://www.treasury.id", {
    Referer: "https://www.treasury.id",
  });

  if (detectCloudflare(html)) throw new Error("Treasury: diblokir Cloudflare");

  // Treasury biasanya tampilkan harga realtime di landing page
  const prices = [...html.matchAll(/([\d]{1,2}[.,][\d]{3}[.,][\d]{3})/g)]
    .map((m) => parseIDR(m[1]))
    .filter(isValidGoldPrice)
    .sort((a, b) => b - a);

  if (prices.length < 1) throw new Error("Treasury: tidak ada harga ditemukan");

  const buyPrice = prices[0];
  const sellPrice = prices[1] ?? Math.round(buyPrice * 0.968); // spread ~3.2%

  if (!isValidGoldPrice(buyPrice)) throw new Error("Treasury: harga tidak valid");

  return {
    success: true,
    data: {
      brand: "Treasury",
      buyPrice,
      sellPrice,
      unit: "gram",
      currency: "IDR",
      scrapedAt: new Date(),
      source: "https://www.treasury.id",
    },
    sourceUsed: "treasury.id",
  };
}

// ============================================================
// TAMASIA — tamasia.co.id
// ============================================================

async function scrapeTamasia() {
  const html = await fetchHTML("https://tamasia.co.id", {
    Referer: "https://tamasia.co.id",
  });

  if (detectCloudflare(html)) throw new Error("Tamasia: diblokir Cloudflare");

  const prices = [...html.matchAll(/([\d]{1,2}[.,][\d]{3}[.,][\d]{3})/g)]
    .map((m) => parseIDR(m[1]))
    .filter(isValidGoldPrice)
    .sort((a, b) => b - a);

  if (prices.length < 1) throw new Error("Tamasia: tidak ada harga ditemukan");

  const buyPrice = prices[0];
  const sellPrice = prices[1] ?? Math.round(buyPrice * 0.97);

  return {
    success: true,
    data: {
      brand: "Tamasia",
      buyPrice,
      sellPrice,
      unit: "gram",
      currency: "IDR",
      scrapedAt: new Date(),
      source: "https://tamasia.co.id",
    },
    sourceUsed: "tamasia.co.id",
  };
}

// ============================================================
// BRI MAS GOLD — estimasi dari Antam + markup ~3.5%
// Tidak ada halaman harga publik, markup berdasarkan rata-rata pasar
// ============================================================

async function scrapeBBRI() {
  // BRI tidak punya halaman harga publik yang bisa discrape
  // Gunakan Antam sebagai base + markup rata-rata perbankan
  const antamResult = await scrapeAntam();
  if (!antamResult.success) {
    return { success: false, error: "BRI: tidak bisa dapat harga base Antam" };
  }

  const markup = 1.035; // markup BRI ~3.5% di atas Antam
  const buyPrice = Math.round(antamResult.data.buyPrice * markup);
  const sellPrice = Math.round(antamResult.data.sellPrice * 0.97);

  return {
    success: true,
    data: {
      brand: "BRI Mas Gold",
      buyPrice,
      sellPrice,
      unit: "gram",
      currency: "IDR",
      scrapedAt: new Date(),
      source: "estimasi dari Antam + markup 3.5%",
      note: "Harga BRI adalah estimasi, konfirmasi ke aplikasi BRImo",
    },
    sourceUsed: "estimasi",
  };
}

// ============================================================
// Public API
// ============================================================

const SCRAPERS = {
  antam:    scrapeAntam,
  pegadaian: scrapePegadaian,
  treasury:  scrapeTreasury,
  tamasia:   scrapeTamasia,
  bbri:      scrapeBBRI,
  uob: async () => ({
    success: false,
    error: "Scraper UOB belum tersedia — situs memerlukan login",
  }),
};

export async function scrapeBrand(brand) {
  const scraper = SCRAPERS[brand.id];
  if (!scraper) {
    return { success: false, error: `Scraper "${brand.id}" belum diimplementasi` };
  }
  try {
    return await scraper();
  } catch (err) {
    return { success: false, error: err.message };
  }
}

export async function scrapeAll(brands) {
  const results = await Promise.allSettled(brands.map((b) => scrapeBrand(b)));
  const map = new Map();
  results.forEach((result, i) => {
    map.set(
      brands[i].id,
      result.status === "fulfilled"
        ? result.value
        : { success: false, error: result.reason?.message ?? "Unknown error" }
    );
  });
  return map;
}

// ---- Debug mode: node scripts/scraper.js [brandId] ----

if (process.argv[1] && process.argv[1].endsWith("scraper.js")) {
  const target = process.argv[2] ?? "antam";
  console.log(`🔍 Testing scraper: ${target}\n`);

  const fakeBrand = { id: target };
  const result = await scrapeBrand(fakeBrand);

  if (result.success) {
    const fmt = (n) => `Rp ${n.toLocaleString("id-ID")}`;
    console.log(`✅ Sumber   : ${result.sourceUsed}`);
    console.log(`   Brand    : ${result.data.brand}`);
    console.log(`   Beli     : ${fmt(result.data.buyPrice)}/gram`);
    console.log(`   Jual     : ${fmt(result.data.sellPrice)}/gram`);
    console.log(`   Diambil  : ${result.data.scrapedAt.toLocaleString("id-ID")}`);
    if (result.data.note) console.log(`   ⚠️  ${result.data.note}`);
  } else {
    console.error(`❌ Gagal: ${result.error}`);
    process.exit(1);
  }
}
