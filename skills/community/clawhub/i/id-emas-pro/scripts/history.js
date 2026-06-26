// ============================================
// scripts/history.js — Histori harga harian
//
// Simpan snapshot harga per hari ke .data/history.json
// Query: 7 hari, 30 hari, chart ASCII
// ============================================

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const HISTORY_FILE = path.join(__dirname, "../.data/history.json");
const MAX_DAYS = 365; // simpan max 1 tahun

// ---- Storage ----

async function readHistory() {
  try {
    const raw = await fs.readFile(HISTORY_FILE, "utf-8");
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

async function writeHistory(data) {
  await fs.mkdir(path.dirname(HISTORY_FILE), { recursive: true });
  await fs.writeFile(HISTORY_FILE, JSON.stringify(data, null, 2));
}

/**
 * Simpan harga hari ini ke histori
 * Key: "antam:2026-03-27"
 */
export async function recordPrice(brandId, priceData) {
  const history = await readHistory();
  const dateKey = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  const key = `${brandId}:${dateKey}`;

  // Jangan overwrite kalau sudah ada entry hari ini (kecuali harga berubah)
  if (!history[key]) {
    history[key] = {
      brandId,
      date: dateKey,
      buyPrice: priceData.buyPrice,
      sellPrice: priceData.sellPrice,
      source: priceData.source,
      recordedAt: new Date().toISOString(),
    };

    // Prune data lama
    const keys = Object.keys(history).sort();
    if (keys.length > MAX_DAYS * 10) {
      // hapus 20% tertua
      const toDelete = Math.floor(keys.length * 0.2);
      for (let i = 0; i < toDelete; i++) delete history[keys[i]];
    }

    await writeHistory(history);
  }

  return history[key];
}

/**
 * Ambil histori N hari terakhir untuk satu brand
 */
export async function getPriceHistory(brandId, days = 7) {
  const history = await readHistory();

  const entries = Object.values(history)
    .filter((e) => e.brandId === brandId)
    .sort((a, b) => b.date.localeCompare(a.date))
    .slice(0, days)
    .reverse(); // oldest first untuk chart

  return entries;
}

/**
 * Hitung statistik dari histori
 */
export function calcStats(entries) {
  if (entries.length === 0) return null;

  const prices = entries.map((e) => e.buyPrice);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const avg = Math.round(prices.reduce((a, b) => a + b, 0) / prices.length);
  const first = prices[0];
  const last = prices[prices.length - 1];
  const change = last - first;
  const changePct = ((change / first) * 100).toFixed(2);

  return { min, max, avg, first, last, change, changePct, days: entries.length };
}

/**
 * Buat chart ASCII dari histori harga
 */
export function renderAsciiChart(entries, width = 20) {
  if (entries.length < 2) return "Belum cukup data untuk chart.";

  const prices = entries.map((e) => e.buyPrice);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const range = max - min || 1;
  const height = 6;

  const fmt = (n) => `${(n / 1_000_000).toFixed(2)}jt`;

  // Normalize ke height
  const normalized = prices.map((p) =>
    Math.round(((p - min) / range) * (height - 1))
  );

  // Build grid
  const grid = Array.from({ length: height }, () =>
    Array(prices.length).fill(" ")
  );

  normalized.forEach((y, x) => {
    grid[height - 1 - y][x] = "█";
    // fill downward untuk bar chart
    for (let i = height - 1 - y + 1; i < height; i++) {
      grid[i][x] = "▄";
    }
  });

  const lines = grid.map((row, i) => {
    const label =
      i === 0
        ? fmt(max).padStart(7)
        : i === height - 1
        ? fmt(min).padStart(7)
        : "".padStart(7);
    return `${label} │${row.join("")}`;
  });

  // X axis dates
  const dateLabels = entries
    .map((e) => e.date.slice(5)) // MM-DD
    .join(" ");

  lines.push(`        └${"─".repeat(prices.length)}`);
  lines.push(`         ${dateLabels}`);

  return lines.join("\n");
}

/**
 * Format ringkasan histori untuk dikirim ke chat
 */
export function formatHistorySummary(brandName, entries, stats) {
  if (!stats || entries.length === 0) {
    return `📊 Belum ada histori harga untuk ${brandName}.`;
  }

  const fmt = (n) => `Rp ${n.toLocaleString("id-ID")}`;
  const arrow = stats.change >= 0 ? "📈" : "📉";
  const sign = stats.change >= 0 ? "+" : "";

  return [
    `📊 *Histori ${brandName} (${stats.days} hari)*`,
    ``,
    `${arrow} Perubahan : ${sign}${fmt(stats.change)} (${sign}${stats.changePct}%)`,
    `🔼 Tertinggi : ${fmt(stats.max)}`,
    `🔽 Terendah  : ${fmt(stats.min)}`,
    `📐 Rata-rata : ${fmt(stats.avg)}`,
    ``,
    `\`\`\``,
    renderAsciiChart(entries, entries.length),
    `\`\`\``,
  ].join("\n");
}
