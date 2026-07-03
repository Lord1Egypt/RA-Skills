/**
 * scrape_sofifa.mjs — scrapes EA FC 26 national team ratings + individual player OVRs.
 * Uses playwright-extra + stealth plugin to bypass Cloudflare without needing real Chrome.
 * Chrome does NOT need to be closed.
 *
 * Run:   node scripts/scrape_sofifa.mjs
 * Then:  python3 scripts/merge_sofifa.py
 *
 * Output: sofifa_wc2026.json (in skill root)
 */

import { chromium } from 'playwright-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import { writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

chromium.use(StealthPlugin());

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT_PATH = join(__dirname, '..', 'sofifa_wc2026.json');

// All 48 WC 2026 teams — cast a wide net with alternate spellings
const WC2026 = [
  'Canada', 'Mexico', 'United States',
  'Austria', 'Belgium', 'Bosnia and Herzegovina', 'Bosnia & Herzegovina',
  'Croatia', 'Czech Republic', 'Czechia',
  'England', 'France', 'Germany', 'Netherlands', 'Norway', 'Portugal',
  'Scotland', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'Türkiye',
  'Argentina', 'Brazil', 'Colombia', 'Ecuador', 'Paraguay', 'Uruguay',
  'Algeria', 'Cabo Verde', 'Cape Verde', 'Congo DR', 'DR Congo',
  "Côte d'Ivoire", "Cote d'Ivoire", 'Ivory Coast',
  'Egypt', 'Ghana', 'Morocco', 'Senegal', 'South Africa', 'Tunisia',
  'Australia', 'Iran', 'Iraq', 'Japan', 'Jordan',
  'South Korea', 'Korea Republic', 'Qatar', 'Saudi Arabia', 'Uzbekistan',
  'Curaçao', 'Curacao', 'Haiti', 'Panama',
  'New Zealand',
];
const WC_SET = new Set(WC2026.map(n => n.toLowerCase()));

const CANON = {
  'united states': 'USA',
  'turkey': 'Turkey', 'türkiye': 'Turkey',
  'czech republic': 'Czech Republic', 'czechia': 'Czech Republic',
  'dr congo': 'Congo DR', 'congo dr': 'Congo DR',
  "côte d'ivoire": 'Ivory Coast', "cote d'ivoire": 'Ivory Coast', 'ivory coast': 'Ivory Coast',
  'korea republic': 'South Korea',
  'curaçao': 'Curaçao', 'curacao': 'Curaçao',
  'cape verde': 'Cabo Verde',
  'bosnia and herzegovina': 'Bosnia and Herzegovina',
  'bosnia & herzegovina': 'Bosnia and Herzegovina',
};

function canonName(n) { return CANON[n.toLowerCase()] || n; }
function isWC(n) { return WC_SET.has(n.toLowerCase()) || WC_SET.has(canonName(n).toLowerCase()); }
async function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

async function waitForTable(page, maxWaitMs = 20000) {
  const start = Date.now();
  while (Date.now() - start < maxWaitMs) {
    const hasTable = await page.$('table tbody tr').catch(() => null);
    const title = await page.title().catch(() => '');
    const isCF = title.includes('moment') || title.includes('Cloudflare') || title.includes('Just a');
    if (hasTable && !isCF) return true;
    if (isCF) process.stdout.write('⏳ CF...');
    await delay(1500);
  }
  return false;
}

async function scrapeSquad(page, teamHref, teamName) {
  const url = `https://sofifa.com${teamHref}?col=oa&sort=desc`;
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    const ok = await waitForTable(page, 15000);
    if (!ok) {
      console.log(`    ⚠  No table for ${teamName}`);
      return [];
    }

    const players = await page.evaluate(() => {
      const rows = [...document.querySelectorAll('table tbody tr')];
      return rows.flatMap(row => {
        const nameA = row.querySelector('td[data-col="pi"] a, a[href*="/player/"]');
        const name = nameA?.textContent?.trim();
        if (!name) return [];

        const posEl = row.querySelector('span.pos, .pos');
        const pos = posEl?.textContent?.trim() || null;

        const oaCell = row.querySelector('td[data-col="oa"]');
        const oaEl = oaCell?.querySelector('em, .bp3-tag, span') || oaCell;
        const ovr = oaEl ? parseInt(oaEl.textContent.trim()) : null;

        const ageCell = row.querySelector('td[data-col="ae"]');
        const age = ageCell ? parseInt(ageCell.textContent.trim()) : null;

        if (!ovr || ovr < 40 || ovr > 100) return [];
        return [{ name, pos, ovr, age }];
      });
    });

    return players;
  } catch (e) {
    console.log(`    ⚠  Squad scrape failed for ${teamName}: ${e.message.slice(0, 80)}`);
    return [];
  }
}

async function main() {
  console.log('Launching stealth Chromium (no Chrome profile needed)...');
  const browser = await chromium.launch({
    headless: false,   // visible helps pass bot checks
    args: [
      '--no-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-infobars',
    ],
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.207 Safari/537.36',
    viewport: { width: 1440, height: 900 },
    locale: 'en-US',
    timezoneId: 'America/New_York',
    extraHTTPHeaders: {
      'Accept-Language': 'en-US,en;q=0.9',
      'Accept': 'text/html,application/xhtml+xml,application/xhtml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    },
  });

  const page = await context.newPage();

  // ── Teams list ──────────────────────────────────────────────────────────
  console.log('\nLoading SoFIFA national teams...');
  await page.goto('https://sofifa.com/teams?type=international&col=oa&sort=desc', {
    waitUntil: 'domcontentloaded',
    timeout: 30000,
  });

  const ok = await waitForTable(page, 25000);
  const title = await page.title();
  console.log('Page title:', title);

  if (!ok) {
    console.error('❌ Could not load teams table. Cloudflare may be blocking headless mode.');
    console.error('   Try: close Chrome, then run with STEALTH_FALLBACK=chrome node scripts/scrape_sofifa.mjs');
    await browser.close();
    process.exit(1);
  }

  const allTeams = await page.evaluate(() => {
    const rows = [...document.querySelectorAll('table tbody tr')];
    return rows.flatMap(row => {
      const nameA = row.querySelector('td[data-col="pi"] a, a[href*="/team/"]');
      const name = nameA?.textContent?.trim();
      const href = nameA?.getAttribute('href') || '';
      if (!name || !href.includes('/team/')) return [];
      const get = col => {
        const el = row.querySelector(`td[data-col="${col}"]`);
        return el ? parseInt(el.textContent.trim()) || null : null;
      };
      return [{ name, href, ovr: get('oa'), att: get('at'), mid: get('md'), def: get('df') }];
    });
  });

  console.log(`Found ${allTeams.length} total national teams on page`);
  const wcTeams = allTeams.filter(t => isWC(t.name));
  console.log(`Matched ${wcTeams.length} / 48 WC 2026 teams`);

  const matchedNames = new Set(wcTeams.map(t => canonName(t.name).toLowerCase()));
  const missing = [...new Set(WC2026)].filter(n => !matchedNames.has(canonName(n).toLowerCase()));
  if (missing.length) console.log('⚠  Not on page (unlicensed in FC26?):', missing.join(', '));

  // ── Squad pages ─────────────────────────────────────────────────────────
  console.log('\nScraping individual player OVRs for each team...');
  const results = [];

  for (const team of wcTeams) {
    const canon = canonName(team.name);
    process.stdout.write(`  [${results.length + 1}/${wcTeams.length}] ${canon.padEnd(28)}`);

    const players = await scrapeSquad(page, team.href, canon);

    // Sort by OVR desc — top 11 are the likely starters
    players.sort((a, b) => b.ovr - a.ovr);
    const top11 = players.slice(0, 11);
    const top11Avg = top11.length === 11
      ? Math.round(top11.reduce((s, p) => s + p.ovr, 0) / 11)
      : null;

    // Positional breakdowns from full squad
    const byPos = (pos) => players.filter(p => p.pos && p.pos.includes(pos));
    const posAvg = (arr) => arr.length ? Math.round(arr.reduce((s, p) => s + p.ovr, 0) / arr.length) : null;

    const gks  = byPos('GK');
    const defs = players.filter(p => p.pos && /CB|LB|RB|LWB|RWB|SW/.test(p.pos));
    const mids = players.filter(p => p.pos && /CM|CDM|CAM|LM|RM/.test(p.pos));
    const fwds = players.filter(p => p.pos && /ST|CF|LW|RW|LS|RS|LF|RF/.test(p.pos));

    process.stdout.write(
      ` OVR=${team.ovr ?? '?'} ATT=${team.att ?? '?'} MID=${team.mid ?? '?'} DEF=${team.def ?? '?'}` +
      ` | ${players.length} players, top11_avg=${top11Avg ?? '?'}\n`
    );

    results.push({
      name: canon,
      sofifa_name: team.name,
      ovr: team.ovr,
      att: team.att,
      mid: team.mid,
      def: team.def,
      top11_avg_ovr: top11Avg,
      top11: top11,
      players,
    });

    await delay(800 + Math.random() * 600);
  }

  await browser.close();

  // ── Save ────────────────────────────────────────────────────────────────
  const output = {
    scraped_at: new Date().toISOString(),
    game: 'EA FC 26',
    total_teams: results.length,
    teams: results.sort((a, b) => (b.ovr ?? 0) - (a.ovr ?? 0)),
  };

  writeFileSync(OUT_PATH, JSON.stringify(output, null, 2));
  console.log(`\n✅ Saved → ${OUT_PATH}`);
  console.log(`   Run: python3 scripts/merge_sofifa.py`);

  // Summary table
  console.log('\nTeam                     | OVR | Top11 | Players | Top striker');
  console.log('-------------------------|-----|-------|---------|------------');
  results.sort((a, b) => (b.ovr ?? 0) - (a.ovr ?? 0)).forEach(t => {
    const n = t.name.padEnd(24);
    const v = x => String(x ?? '?').padStart(4);
    const topSt = (t.players || []).find(p => p.pos && /ST|CF|LW|RW/.test(p.pos));
    const stLabel = topSt ? `${topSt.name} (${topSt.ovr})` : '-';
    console.log(`${n} | ${v(t.ovr)} | ${String(t.top11_avg_ovr ?? '?').padStart(5)} | ${String((t.players||[]).length).padStart(7)} | ${stLabel}`);
  });
}

main().catch(e => { console.error('\n❌', e.message); process.exit(1); });
