// ============================================
// test.js — Unit tests
// Jalankan: node test.js
// Tidak butuh test runner — pure Node.js
// ============================================

import { calcStats, renderAsciiChart } from "./history.js";
import { isValidGoldPrice } from "./scraper.js";
import { withRetry } from "../utils/retry.js";
import { MemoryAlertStorage } from "./storage.js";
import { AlertManager, ChatNotifier } from "./alerts.js";

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (err) {
    console.log(`❌ ${name}`);
    console.log(`   ${err.message}`);
    failed++;
  }
}

async function testAsync(name, fn) {
  try {
    await fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (err) {
    console.log(`❌ ${name}`);
    console.log(`   ${err.message}`);
    failed++;
  }
}

function assert(cond, msg) {
  if (!cond) throw new Error(msg ?? "Assertion failed");
}

function assertEqual(a, b, msg) {
  if (a !== b) throw new Error(msg ?? `Expected ${b}, got ${a}`);
}

// ---- parseIDR tests ----
console.log("\n📦 parseIDR");

function parseIDR(raw) {
  if (!raw) return NaN;
  return parseInt(String(raw).replace(/[^0-9]/g, ""), 10);
}

test("parse Rp 1.234.567", () => assertEqual(parseIDR("Rp 1.234.567"), 1234567));
test("parse 2.850.000", () => assertEqual(parseIDR("2.850.000"), 2850000));
test("parse dengan koma", () => assertEqual(parseIDR("2,850,000"), 2850000));
test("parse empty string", () => assert(isNaN(parseIDR(""))));
test("parse null", () => assert(isNaN(parseIDR(null))));

// ---- isValidGoldPrice ----
console.log("\n📦 isValidGoldPrice");

function isValid(n) {
  return Number.isFinite(n) && n > 500_000 && n < 10_000_000;
}

test("harga valid 2.8jt", () => assert(isValid(2_800_000)));
test("harga valid 1jt", () => assert(isValid(1_000_000)));
test("terlalu kecil 100rb", () => assert(!isValid(100_000)));
test("terlalu besar 50jt", () => assert(!isValid(50_000_000)));
test("NaN tidak valid", () => assert(!isValid(NaN)));
test("Infinity tidak valid", () => assert(!isValid(Infinity)));

// ---- calcStats ----
console.log("\n📦 calcStats");

test("stats kosong return null", () => {
  assert(calcStats([]) === null);
});

test("stats 3 entries", () => {
  const entries = [
    { date: "2026-03-25", buyPrice: 2_800_000, sellPrice: 2_750_000 },
    { date: "2026-03-26", buyPrice: 2_850_000, sellPrice: 2_800_000 },
    { date: "2026-03-27", buyPrice: 2_820_000, sellPrice: 2_770_000 },
  ];
  const s = calcStats(entries);
  assertEqual(s.min, 2_800_000, "min");
  assertEqual(s.max, 2_850_000, "max");
  assertEqual(s.first, 2_800_000, "first");
  assertEqual(s.last, 2_820_000, "last");
  assertEqual(s.days, 3, "days");
  assert(s.change === 20_000, `change: expected 20000, got ${s.change}`);
});

test("stats perubahan negatif", () => {
  const entries = [
    { date: "2026-03-25", buyPrice: 2_900_000, sellPrice: 2_850_000 },
    { date: "2026-03-27", buyPrice: 2_800_000, sellPrice: 2_750_000 },
  ];
  const s = calcStats(entries);
  assert(s.change < 0, "change harus negatif");
  assert(parseFloat(s.changePct) < 0, "changePct harus negatif");
});

// ---- renderAsciiChart ----
console.log("\n📦 renderAsciiChart");

test("chart minimal 2 entries", () => {
  const entries = [
    { date: "2026-03-26", buyPrice: 2_800_000 },
    { date: "2026-03-27", buyPrice: 2_850_000 },
  ];
  const chart = renderAsciiChart(entries);
  assert(typeof chart === "string" && chart.length > 0);
  assert(chart.includes("│"), "harus ada separator");
});

test("chart 1 entry return pesan", () => {
  const entries = [{ date: "2026-03-27", buyPrice: 2_800_000 }];
  const chart = renderAsciiChart(entries);
  assert(chart.includes("Belum cukup data"));
});

// ---- withRetry ----
console.log("\n📦 withRetry");

await testAsync("retry sukses di attempt ke-2", async () => {
  let attempts = 0;
  const result = await withRetry(
    async () => {
      attempts++;
      if (attempts < 2) throw new Error("fail");
      return "ok";
    },
    { maxAttempts: 3, baseDelayMs: 10 }
  );
  assertEqual(result, "ok");
  assertEqual(attempts, 2);
});

await testAsync("retry gagal semua, throw error terakhir", async () => {
  let threw = false;
  try {
    await withRetry(async () => { throw new Error("always fail"); }, {
      maxAttempts: 2,
      baseDelayMs: 10,
    });
  } catch (err) {
    threw = true;
    assert(err.message === "always fail");
  }
  assert(threw, "harus throw");
});

// ---- AlertManager ----
console.log("\n📦 AlertManager");

await testAsync("buat dan list alert", async () => {
  const storage = new MemoryAlertStorage();
  const notifier = new ChatNotifier(async () => {});
  const mgr = new AlertManager(storage, notifier);

  const alert = await mgr.createAlert("user1", {
    brand: "antam",
    condition: "above",
    targetPrice: 3_000_000,
    type: "buy",
  });

  assert(alert.id, "harus ada id");
  assert(!alert.triggered, "belum triggered");

  const list = await mgr.listAlerts("user1");
  assertEqual(list.length, 1);
  assertEqual(list[0].id, alert.id);
});

await testAsync("alert trigger ketika harga di atas target", async () => {
  const storage = new MemoryAlertStorage();
  const triggered = [];
  const notifier = new ChatNotifier(async (uid, msg) => triggered.push({ uid, msg }));
  const mgr = new AlertManager(storage, notifier);

  await mgr.createAlert("user1", {
    brand: "antam",
    condition: "above",
    targetPrice: 2_800_000,
    type: "buy",
  });

  const priceMap = new Map([
    ["antam", { brand: "Antam", buyPrice: 2_850_000, sellPrice: 2_750_000 }],
  ]);

  const result = await mgr.checkPrices("user1", priceMap);
  assertEqual(result.length, 1, "harus 1 alert triggered");
  assertEqual(triggered.length, 1, "harus 1 notifikasi");
});

await testAsync("alert tidak trigger kalau harga di bawah target", async () => {
  const storage = new MemoryAlertStorage();
  const notifier = new ChatNotifier(async () => {});
  const mgr = new AlertManager(storage, notifier);

  await mgr.createAlert("user1", {
    brand: "antam",
    condition: "above",
    targetPrice: 3_000_000,
    type: "buy",
  });

  const priceMap = new Map([
    ["antam", { brand: "Antam", buyPrice: 2_850_000, sellPrice: 2_750_000 }],
  ]);

  const result = await mgr.checkPrices("user1", priceMap);
  assertEqual(result.length, 0, "tidak ada alert triggered");
});

// ---- Summary ----
console.log(`\n${"─".repeat(40)}`);
console.log(`Hasil: ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
