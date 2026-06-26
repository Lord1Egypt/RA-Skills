#!/usr/bin/env node
/**
 * Capture OpenRouter Rankings: page sections + all Categories dropdown scenarios.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_URL = 'https://openrouter.ai/rankings';
const CHROMIUM = process.env.CHROMIUM_PATH || '/snap/bin/chromium';
const OUTPUT_DIR =
  process.env.OPENROUTER_RANKINGS_DIR ||
  path.join(process.env.HOME || '/tmp', '.openclaw', 'cache', 'openrouter-rankings');
const VIEWPORT = { width: 1400, height: 900 };
const MIN_CHART_BARS = Number(process.env.MIN_CHART_BARS || 400);
const MIN_FILE_BYTES = Number(process.env.MIN_SCREENSHOT_BYTES || 28000);
const VIEWPORT_MIN_BARS = Number(process.env.VIEWPORT_MIN_BARS || 20);
const VIEWPORT_WAIT_MS = Number(process.env.VIEWPORT_WAIT_MS || 45000);

const CATEGORY_SCENARIOS = [
  'Programming',
  'Roleplay',
  'Marketing',
  'SEO',
  'Technology',
  'Science',
  'Translation',
  'Legal',
  'Finance',
  'Health',
  'Trivia',
  'Academia',
];

const SECTIONS = [
  { id: '01_top_models', heading: 'Top Models' },
  { id: '02_llm_leaderboard', heading: 'LLM Leaderboard' },
  { id: '03_market_share', heading: 'Market Share' },
  { id: '05_languages', heading: 'Languages' },
  { id: '06_programming', heading: 'Programming' },
  { id: '07_context_length', heading: 'Context Length' },
  { id: '08_tool_calls', heading: 'Tool Calls' },
  { id: '09_images', heading: 'Images' },
  { id: '10_audio_input', heading: 'Audio Input' },
  { id: '11_top_apps', heading: 'Top Apps', minBars: 0, waitForApps: true },
];

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function parseCategoryRankings(innerText) {
  const lines = innerText.split('\n').map((l) => l.trim()).filter(Boolean);
  const rankings = [];
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^(\d+)\.$/);
    if (!m) continue;
    const model = lines[i + 1];
    let j = i + 2;
    if (lines[j] === 'by') j++;
    const provider = lines[j]?.startsWith('by') ? lines[j + 1] : lines[j];
    const volume = lines[j + 1] || lines[j + 2];
    const share = lines[j + 2] || lines[j + 3];
    if (model && model !== 'Others') {
      rankings.push({
        rank: Number(m[1]),
        model,
        provider: provider && provider !== model ? provider : undefined,
        volume: volume && /[KMBT]/.test(volume) ? volume : undefined,
        share: share && share.includes('%') ? share : undefined,
      });
    }
    if (rankings.length >= 5) break;
  }
  return rankings;
}

async function getBarCount(page) {
  return page.evaluate(() =>
    document.querySelectorAll('[class*="recharts-bar"] path, [class*="recharts-bar"] rect').length,
  );
}

async function waitForCharts(page, minBars = MIN_CHART_BARS, timeoutMs = 90000) {
  const start = Date.now();
  let last = 0;
  let stable = 0;
  while (Date.now() - start < timeoutMs) {
    const count = await getBarCount(page);
    if (count >= minBars) {
      if (count === last) stable += 1;
      else stable = 0;
      last = count;
      if (stable >= 2) return count;
    } else {
      stable = 0;
      last = count;
    }
    await new Promise((r) => setTimeout(r, 800));
  }
  throw new Error(`Charts not ready after ${timeoutMs}ms (bars=${last}, need>=${minBars})`);
}

async function getViewportStats(page) {
  return page.evaluate(() => {
    const bars = [...document.querySelectorAll('[class*="recharts-bar"] path, [class*="recharts-bar"] rect')].filter(
      (el) => {
        const r = el.getBoundingClientRect();
        return r.height > 2 && r.width > 2 && r.top >= 60 && r.bottom <= window.innerHeight - 40;
      },
    ).length;
    const skeletons = [
      ...document.querySelectorAll('[class*="skeleton"], [class*="Skeleton"], [data-slot="skeleton"], .animate-pulse'),
    ].filter((el) => {
      const r = el.getBoundingClientRect();
      return r.height > 24 && r.top >= 0 && r.bottom <= window.innerHeight && r.width > 80;
    }).length;
    return { inViewBars: bars, skeletonsInView: skeletons };
  });
}

async function getCategoriesViewportStats(page) {
  return page.evaluate(() => {
    const root = document.getElementById('categories');
    if (!root) return { inViewBars: 0, skeletonsInView: 999 };
    const bars = [...root.querySelectorAll('[class*="recharts-bar"] path, [class*="recharts-bar"] rect')].filter(
      (el) => {
        const r = el.getBoundingClientRect();
        return r.height > 2 && r.width > 2;
      },
    ).length;
    const skeletons = [...root.querySelectorAll('[class*="skeleton"], .animate-pulse')].filter((el) => {
      const r = el.getBoundingClientRect();
      return r.height > 24 && r.width > 80;
    }).length;
    return { inViewBars: bars, skeletonsInView: skeletons };
  });
}

async function waitForAppsList(page, timeoutMs = 30000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const ok = await page.evaluate(() => {
      const h = [...document.querySelectorAll('h2')].find((el) => el.textContent?.trim() === 'Top Apps');
      if (!h) return false;
      const hr = h.getBoundingClientRect();
      if (hr.top < -50 || hr.top > 250) return false;
      const apps = [...document.querySelectorAll('a[href*="/apps/"]')].filter((a) => {
        const r = a.getBoundingClientRect();
        return r.top > hr.bottom && r.top < window.innerHeight;
      }).length;
      return apps >= 5;
    });
    if (ok) {
      await new Promise((r) => setTimeout(r, 800));
      return { inViewBars: 0, skeletonsInView: 0 };
    }
    await new Promise((r) => setTimeout(r, 500));
  }
  throw new Error(`Top Apps list not ready after ${timeoutMs}ms`);
}

async function waitViewportCharts(page, minBars = VIEWPORT_MIN_BARS, timeoutMs = VIEWPORT_WAIT_MS) {
  if (minBars <= 0) return { inViewBars: 0, skeletonsInView: 0 };
  const start = Date.now();
  let last = { inViewBars: 0, skeletonsInView: 999 };
  let stable = 0;
  while (Date.now() - start < timeoutMs) {
    const stats = await getViewportStats(page);
    const ready = stats.inViewBars >= minBars && stats.skeletonsInView <= 8;
    if (ready) {
      if (stats.inViewBars === last.inViewBars && stats.skeletonsInView === last.skeletonsInView) stable += 1;
      else stable = 0;
      last = stats;
      if (stable >= 2) {
        await new Promise((r) => setTimeout(r, 800));
        return stats;
      }
    } else {
      stable = 0;
      last = stats;
    }
    await new Promise((r) => setTimeout(r, 700));
  }
  throw new Error(
    `Viewport charts not ready after ${timeoutMs}ms (inViewBars=${last.inViewBars}, skeletons=${last.skeletonsInView})`,
  );
}

async function waitCategoriesCharts(page, timeoutMs = VIEWPORT_WAIT_MS) {
  const start = Date.now();
  let last = { inViewBars: 0, skeletonsInView: 999 };
  let stable = 0;
  while (Date.now() - start < timeoutMs) {
    const stats = await getCategoriesViewportStats(page);
    const ready = stats.inViewBars >= 15 && stats.skeletonsInView <= 5;
    if (ready) {
      if (stats.inViewBars === last.inViewBars && stats.skeletonsInView === last.skeletonsInView) stable += 1;
      else stable = 0;
      last = stats;
      if (stable >= 2) {
        await new Promise((r) => setTimeout(r, 1000));
        return stats;
      }
    } else {
      stable = 0;
      last = stats;
    }
    await new Promise((r) => setTimeout(r, 700));
  }
  throw new Error(`Categories charts not ready (bars=${last.inViewBars}, skeletons=${last.skeletonsInView})`);
}

async function scrollToHeading(page, headingText) {
  const found = await page.evaluate((text) => {
    const h = [...document.querySelectorAll('h2')].find((el) => el.textContent?.trim() === text);
    if (!h) return false;
    h.scrollIntoView({ block: 'start', behavior: 'instant' });
    return true;
  }, headingText);
  if (!found) throw new Error(`Heading not found: ${headingText}`);
  await new Promise((r) => setTimeout(r, 2000));
}

async function scrollToCategories(page) {
  await page.evaluate(() => document.getElementById('categories')?.scrollIntoView({ block: 'start', behavior: 'instant' }));
  await new Promise((r) => setTimeout(r, 2500));
}

async function selectCategoryScenario(page, scenario) {
  await scrollToCategories(page);
  const combo = await page.$('#categories button[role="combobox"]');
  if (!combo) throw new Error('Categories combobox not found');
  await combo.click();
  await new Promise((r) => setTimeout(r, 700));
  const options = await page.$$('[role="option"]');
  let picked = false;
  for (const opt of options) {
    const label = await opt.evaluate((el) => el.textContent?.trim());
    if (label === scenario) {
      await opt.click();
      picked = true;
      break;
    }
  }
  if (!picked) throw new Error(`Category option not found: ${scenario}`);
  // Dismiss dropdown (click chart area) and wait for label + data
  await page.mouse.click(700, 450);
  await page.waitForFunction(
    (name) =>
      document.getElementById('categories')?.querySelector('button[role="combobox"]')?.textContent?.trim() === name,
    { timeout: 20000 },
    scenario,
  );
  let lastTop = '';
  for (let i = 0; i < 24; i++) {
    const top = await page.evaluate(() => {
      const t = document.getElementById('categories')?.innerText || '';
      return t.match(/1\.\s*\n([^\n]+)/)?.[1] || '';
    });
    if (top && top === lastTop && i >= 5) break;
    lastTop = top || lastTop;
    await new Promise((r) => setTimeout(r, 500));
  }
  await new Promise((r) => setTimeout(r, 1000));
}

async function readCategoryRankings(page) {
  return page.evaluate(() => {
    const text = document.getElementById('categories')?.innerText || '';
    return text;
  });
}

function validatePng(filePath) {
  const stat = fs.statSync(filePath);
  if (stat.size < MIN_FILE_BYTES) {
    throw new Error(`${path.basename(filePath)} too small (${stat.size} bytes)`);
  }
}

async function captureCategoryScenarios(page, outDir, manifest) {
  const catDir = path.join(outDir, 'categories');
  fs.mkdirSync(catDir, { recursive: true });
  manifest.categoryScenarios = [];

  await scrollToCategories(page);
  await waitCategoriesCharts(page).catch(() => {});

  for (let i = 0; i < CATEGORY_SCENARIOS.length; i++) {
    const scenario = CATEGORY_SCENARIOS[i];
    const fileName = `04_cat_${String(i + 1).padStart(2, '0')}_${slugify(scenario)}.png`;
    const filePath = path.join(catDir, fileName);
    try {
      console.log(`📸 Categories / ${scenario} ...`);
      await selectCategoryScenario(page, scenario);
      const viewport = await waitCategoriesCharts(page);
      const innerText = await readCategoryRankings(page);
      const rankings = parseCategoryRankings(innerText);
      if (rankings.length === 0) {
        throw new Error('No rankings parsed from Categories section');
      }
      await page.screenshot({ path: filePath, type: 'png' });
      validatePng(filePath);
      const entry = {
        id: `04_cat_${slugify(scenario)}`,
        heading: `Categories — ${scenario}`,
        scenario,
        file: filePath,
        fileName,
        rankings,
        barCount: viewport.inViewBars,
        bytes: fs.statSync(filePath).size,
        ok: true,
      };
      manifest.categoryScenarios.push(entry);
      console.log(`   ✅ ${fileName} (top: ${rankings[0]?.model})`);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      manifest.errors.push({ section: `Categories/${scenario}`, error: msg });
      manifest.categoryScenarios.push({ scenario, ok: false, error: msg });
      console.error(`   ❌ ${scenario}: ${msg}`);
    }
  }
}

async function main() {
  const url = process.argv[2] || DEFAULT_URL;
  const date = new Date().toISOString().slice(0, 10);
  const outDir = path.join(OUTPUT_DIR, date);
  fs.mkdirSync(outDir, { recursive: true });

  if (!fs.existsSync(CHROMIUM)) {
    console.error(`Chromium not found at ${CHROMIUM}. Set CHROMIUM_PATH.`);
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    executablePath: CHROMIUM,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
  });

  const manifest = {
    url,
    date,
    capturedAt: new Date().toISOString(),
    outputDir: outDir,
    sections: [],
    categoryScenarios: [],
    errors: [],
  };

  try {
    const page = await browser.newPage();
    await page.setViewport(VIEWPORT);
    await page.setUserAgent(
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
    );

    console.log(`🌐 Loading ${url} ...`);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 120000 });
    await new Promise((r) => setTimeout(r, 3000));

    const initialBars = await waitForCharts(page);
    console.log(`📊 Charts ready (bars=${initialBars})`);

    console.log('⏬ Warming up lazy sections...');
    const pageHeight = await page.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y <= pageHeight; y += 500) {
      await page.evaluate((scrollY) => window.scrollTo(0, scrollY), y);
      await new Promise((r) => setTimeout(r, 350));
    }
    await page.evaluate(() => window.scrollTo(0, 0));
    await new Promise((r) => setTimeout(r, 1500));

    for (const section of SECTIONS) {
      const fileName = `${section.id}_${slugify(section.heading)}.png`;
      const filePath = path.join(outDir, fileName);
      try {
        console.log(`📸 ${section.heading} ...`);
        await scrollToHeading(page, section.heading);
        const viewport = section.waitForApps
          ? await waitForAppsList(page)
          : await waitViewportCharts(page, section.minBars ?? VIEWPORT_MIN_BARS);
        await page.screenshot({ path: filePath, type: 'png' });
        validatePng(filePath);
        manifest.sections.push({
          id: section.id,
          heading: section.heading,
          file: filePath,
          fileName,
          barCount: viewport.inViewBars,
          bytes: fs.statSync(filePath).size,
          ok: true,
        });
        console.log(`   ✅ ${fileName}`);
      } catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        manifest.errors.push({ section: section.heading, error: msg });
        manifest.sections.push({ id: section.id, heading: section.heading, ok: false, error: msg });
        console.error(`   ❌ ${section.heading}: ${msg}`);
      }
    }

    await captureCategoryScenarios(page, outDir, manifest);
  } finally {
    await browser.close();
  }

  const manifestPath = path.join(outDir, 'manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));

  // Generate summary for Feishu doc + sales message
  const summaryPath = path.join(outDir, 'summary.md');
  await import('./generate-summary.mjs').then((m) => m.writeSummary(manifest, summaryPath));
  console.log(`SUMMARY:${summaryPath}`);

  const failedSections = manifest.sections.filter((s) => !s.ok).length;
  const failedCats = manifest.categoryScenarios.filter((c) => !c.ok).length;
  if (failedSections > 0 || failedCats > 0) {
    console.error(`\n⚠️ ${failedSections + failedCats} capture(s) failed. See ${manifestPath}`);
    process.exit(2);
  }

  const total = manifest.sections.filter((s) => s.ok).length + manifest.categoryScenarios.filter((c) => c.ok).length;
  console.log(`\n✅ Done. ${total} screenshots → ${outDir}`);
  console.log(`MANIFEST:${manifestPath}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
