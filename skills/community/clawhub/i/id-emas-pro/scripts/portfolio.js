// ============================================
// scripts/portfolio.js — Portfolio tracker
// ============================================

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORTFOLIO_FILE = path.join(__dirname, "../.data/portfolio.json");

// ---- Storage ----

async function readPortfolios() {
  try {
    const raw = await fs.readFile(PORTFOLIO_FILE, "utf-8");
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

async function writePortfolios(data) {
  await fs.mkdir(path.dirname(PORTFOLIO_FILE), { recursive: true });
  await fs.writeFile(PORTFOLIO_FILE, JSON.stringify(data, null, 2));
}

// ---- Portfolio Manager ----

export class PortfolioManager {
  async getPortfolio(userId) {
    const all = await readPortfolios();
    return all[userId] ?? { userId, entries: [] };
  }

  /**
   * Catat pembelian emas baru
   */
  async addEntry(userId, { brand, grams, buyPrice, buyDate }) {
    const all = await readPortfolios();
    if (!all[userId]) all[userId] = { userId, entries: [] };

    const entry = {
      id: crypto.randomUUID(),
      brand,
      grams: parseFloat(grams),
      buyPrice: parseInt(buyPrice),
      buyDate: buyDate ?? new Date().toISOString().slice(0, 10),
      addedAt: new Date().toISOString(),
    };

    all[userId].entries.push(entry);
    await writePortfolios(all);
    return entry;
  }

  /**
   * Hapus entry
   */
  async removeEntry(userId, entryId) {
    const all = await readPortfolios();
    if (!all[userId]) throw new Error("Portfolio tidak ditemukan");

    const before = all[userId].entries.length;
    all[userId].entries = all[userId].entries.filter((e) => e.id !== entryId);

    if (all[userId].entries.length === before) throw new Error("Entry tidak ditemukan");
    await writePortfolios(all);
  }

  /**
   * Hitung P&L berdasarkan harga saat ini
   * currentPrices: Map<brandId, GoldPrice>
   */
  async calcSnapshot(userId, currentPrices) {
    const portfolio = await this.getPortfolio(userId);
    if (portfolio.entries.length === 0) return null;

    const snapshots = portfolio.entries.map((entry) => {
      const price = currentPrices.get(entry.brand);
      const currentPrice = price?.sellPrice ?? null; // jual balik = sellPrice

      const initialValue = entry.grams * entry.buyPrice;
      const currentValue = currentPrice ? entry.grams * currentPrice : null;
      const profitLoss = currentValue ? currentValue - initialValue : null;
      const profitLossPct = profitLoss ? ((profitLoss / initialValue) * 100).toFixed(2) : null;

      return {
        ...entry,
        currentPrice,
        initialValue,
        currentValue,
        profitLoss,
        profitLossPct,
      };
    });

    const totalInitial = snapshots.reduce((s, e) => s + e.initialValue, 0);
    const totalCurrent = snapshots
      .filter((e) => e.currentValue !== null)
      .reduce((s, e) => s + e.currentValue, 0);
    const totalPL = totalCurrent - totalInitial;
    const totalPLPct = totalInitial > 0
      ? ((totalPL / totalInitial) * 100).toFixed(2)
      : "0.00";

    return { snapshots, totalInitial, totalCurrent, totalPL, totalPLPct };
  }
}

/**
 * Format snapshot untuk dikirim ke chat
 */
export function formatPortfolioSnapshot(snapshot) {
  if (!snapshot) return "Portfolio kamu masih kosong. Tambah emas dengan `/emas portfolio add`.";

  const fmt = (n) => `Rp ${Math.round(n).toLocaleString("id-ID")}`;
  const sign = (n) => (n >= 0 ? "+" : "");
  const plEmoji = snapshot.totalPL >= 0 ? "🟢" : "🔴";

  const lines = [
    `💼 *Portfolio Emas*`,
    ``,
  ];

  for (const e of snapshot.snapshots) {
    const pl = e.profitLoss;
    const plStr = pl !== null
      ? `${sign(pl)}${fmt(pl)} (${sign(parseFloat(e.profitLossPct))}${e.profitLossPct}%)`
      : "(harga tidak tersedia)";

    lines.push(
      `• ${e.brand} — ${e.grams}g @ ${fmt(e.buyPrice)}/g`,
      `  Nilai beli : ${fmt(e.initialValue)}`,
      `  Nilai kini : ${e.currentValue ? fmt(e.currentValue) : "-"}`,
      `  P&L        : ${plStr}`,
      ``
    );
  }

  lines.push(
    `${"─".repeat(30)}`,
    `Total beli  : ${fmt(snapshot.totalInitial)}`,
    `Total kini  : ${fmt(snapshot.totalCurrent)}`,
    `${plEmoji} Total P&L  : ${sign(snapshot.totalPL)}${fmt(snapshot.totalPL)} (${sign(parseFloat(snapshot.totalPLPct))}${snapshot.totalPLPct}%)`
  );

  return lines.join("\n");
}
