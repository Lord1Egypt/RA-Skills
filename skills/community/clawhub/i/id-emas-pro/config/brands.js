// ============================================
// config/brands.js — Daftar brand emas
// ============================================

export const BRANDS = [
  // --- FREE tier (3 brand utama) ---
  {
    id: "antam",
    name: "Logam Mulia Antam",
    url: "https://emasantam.id/harga-emas-antam-harian/",
    enabled: true,
    tier: "free",
  },
  {
    id: "pegadaian",
    name: "Pegadaian (Galeri24)",
    url: "https://sahabat.pegadaian.co.id/harga-emas",
    enabled: true,
    tier: "free",
  },
  {
    id: "treasury",
    name: "Treasury",
    url: "https://www.treasury.id",
    enabled: true,
    tier: "free",
  },

  // --- PRO tier ---
  {
    id: "tamasia",
    name: "Tamasia",
    url: "https://tamasia.co.id",
    enabled: true,
    tier: "pro",
  },
  {
    id: "bbri",
    name: "BRI Mas Gold",
    url: "https://bri.co.id",
    enabled: true,
    tier: "pro",
    note: "Harga estimasi dari Antam + markup",
  },
  {
    id: "uob",
    name: "UOB Gold",
    url: "https://www.uob.co.id",
    enabled: false, // belum ada scraper — butuh login
    tier: "pro",
  },
];

const TIER_ORDER = { free: 0, pro: 1, ai: 2 };

export function getBrandsForTier(userTier) {
  return BRANDS.filter(
    (b) => b.enabled && TIER_ORDER[b.tier] <= TIER_ORDER[userTier ?? "free"]
  );
}

export function getBrandById(id) {
  return BRANDS.find((b) => b.id === id);
}
