#!/usr/bin/env node
// html-to-pdf.mjs — HTML slide deck → vector multi-page PDF via Playwright + Chromium.
//
// Usage:
//   node html-to-pdf.mjs <input.html> <output.pdf> [options]
//
// Options:
//   --width N               PDF page width in px     (default 1920)
//   --height N              PDF page height in px    (default 1080)
//   --slide-selector SEL    CSS selector for slides  (default "section.slide")
//   --channel NAME          'chrome' | 'msedge' — use system browser, skip bundled Chromium
//   --executable-path PATH  Explicit browser binary
//   --proxy URL             HTTP proxy, e.g. http://127.0.0.1:7897
//   --extra-wait MS         Extra settle time after load (default 500)
//   --debug                 Also output <out>.debug.png (full rendered deck screenshot)
//   --keep-page-num-text    Don't clear text inside .slide-number (default: cleared to fix
//                           the "101/22" bug where HTML authors hard-code "01" inside a span
//                           whose CSS uses ::before/::after to inject current/total)
//
// Design notes — why each step exists (so future-us doesn't undo them):
//
//   1. "Deck-style" HTML (every slide position:absolute; top:0; left:0) stacks all slides
//      in one spot. Without forcibly un-stacking, page.pdf() emits ONE page. Fix: nuke
//      position/top/left/right/bottom/transform at print time.
//   2. Authors sometimes hard-code text inside <span class="slide-number">01</span> whose
//      CSS rules are `::before { content: attr(data-current) }` and `::after { content:
//      " / " attr(data-total) }`. Result: "1" + "01" + " / 22" = "101 / 22". Fix: clear
//      textContent on every .slide-number before printing (unless --keep-page-num-text).
//   3. HTML authored by the html-ppt skill uses relative paths like
//      `../../.claude/skills/html-ppt/assets/...` that only exist in the author's workspace.
//      When the workspace doesn't have them, we transparently remap to the global skill
//      install under ~/.myagents/skills/html-ppt/.
//   4. Google Fonts can hang forever in constrained networks. Load with `domcontentloaded`
//      and cap font waits so we don't block indefinitely.

import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

const argv = process.argv.slice(2);
const positionals = [];
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a.startsWith('--')) {
    // Boolean flags consume no value; others consume the next token
    if (['--debug', '--keep-page-num-text'].includes(a)) continue;
    i++; // skip value
  } else {
    positionals.push(a);
  }
}
const [inputArg, outputArg] = positionals;
if (!inputArg || !outputArg) {
  console.error('Usage: node html-to-pdf.mjs <input.html> <output.pdf> [--width N] [--height N] [--slide-selector SEL] [--channel NAME] [--proxy URL] [--debug] [--keep-page-num-text]');
  process.exit(1);
}
const hasFlag = (name) => argv.includes(name);
const flag = (name, fallback) => {
  const i = argv.indexOf(name);
  return i >= 0 && i + 1 < argv.length ? argv[i + 1] : fallback;
};

const width = Number(flag('--width', '1920'));
const height = Number(flag('--height', '1080'));
const slideSelector = flag('--slide-selector', 'section.slide');
const extraWait = Number(flag('--extra-wait', '500'));
const proxy = flag('--proxy', process.env.HTTPS_PROXY || process.env.HTTP_PROXY || '');
const channel = flag('--channel', '');
const executablePath = flag('--executable-path', '');
const debug = hasFlag('--debug');
const keepPageNumText = hasFlag('--keep-page-num-text');

const inputAbs = path.resolve(inputArg);
const outputAbs = path.resolve(outputArg);
if (!fs.existsSync(inputAbs)) {
  console.error(`Input HTML not found: ${inputAbs}`);
  process.exit(1);
}
fs.mkdirSync(path.dirname(outputAbs), { recursive: true });

console.log(`[html-to-pdf] input : ${inputAbs}`);
console.log(`[html-to-pdf] output: ${outputAbs}`);
console.log(`[html-to-pdf] page  : ${width} x ${height}`);

// ─── Launch browser ───────────────────────────────────────────────────────
// IMPORTANT: Playwright's bundled Chromium (tested on build 1208) has a paint
// pipeline bug where page.pdf() silently drops content from slides containing
// a flex-column wrapper with reveal-pattern children (inline opacity:0 +
// transform:translateY). The slide renders correctly on screen and in
// screenshots — only the PDF output is affected. System Chrome does not have
// this bug. So by default we prefer system Chrome/Edge and only fall back to
// bundled Chromium if neither is installed (and warn the user).
const launchOpts = {
  args: [
    '--font-render-hinting=none',
    '--force-color-profile=srgb',
    '--disable-dev-shm-usage',
  ],
};
if (proxy) launchOpts.proxy = { server: proxy };

let effectiveChannel = channel;
if (!effectiveChannel && !executablePath) {
  // Auto-pick system Chrome, then Edge. These are what Playwright's `channel`
  // option knows how to locate on the system.
  for (const cand of ['chrome', 'msedge']) {
    try {
      const test = await chromium.launch({ channel: cand, args: launchOpts.args });
      await test.close();
      effectiveChannel = cand;
      break;
    } catch { /* try next */ }
  }
}

if (effectiveChannel) launchOpts.channel = effectiveChannel;
if (executablePath) launchOpts.executablePath = executablePath;
if (effectiveChannel) {
  console.log(`[html-to-pdf] using system browser: ${effectiveChannel} (avoids bundled-Chromium PDF paint bug)`);
} else if (executablePath) {
  console.log(`[html-to-pdf] executable: ${executablePath}`);
} else {
  console.warn(`[html-to-pdf] WARNING — falling back to bundled Chromium.`);
  console.warn(`[html-to-pdf]   Some slides may render incorrectly in PDF (missing cards, footers, logos).`);
  console.warn(`[html-to-pdf]   Install Chrome or Edge for reliable output.`);
}

const browser = await chromium.launch(launchOpts);
const context = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 2 });
const page = await context.newPage();

// ─── Diagnostics ──────────────────────────────────────────────────────────
const missingAssets = new Set();
page.on('pageerror', (err) => console.error('[page-error]', err.message));
page.on('requestfailed', (req) => missingAssets.add(req.url()));

// ─── Auto-remap broken html-ppt asset paths to global install ─────────────
const globalHtmlPptAssets = path.join(
  process.env.USERPROFILE || process.env.HOME || '',
  '.myagents', 'skills', 'html-ppt',
);
await context.route('file://**/.claude/skills/html-ppt/**', async (route) => {
  const u = new URL(route.request().url());
  const after = u.pathname.split('.claude/skills/html-ppt/')[1];
  if (!after) return route.continue();
  const mapped = path.join(globalHtmlPptAssets, decodeURIComponent(after));
  if (fs.existsSync(mapped)) await route.fulfill({ path: mapped });
  else await route.continue();
});

// ─── Load HTML ────────────────────────────────────────────────────────────
await page.goto(pathToFileURL(inputAbs).href, { waitUntil: 'domcontentloaded', timeout: 30_000 });
await page.waitForLoadState('load', { timeout: 15_000 }).catch(() => {});
await page.waitForLoadState('networkidle', { timeout: 5_000 }).catch(() => {});

// Fonts: bounded wait so blocked Google Fonts doesn't hang us
await Promise.race([
  page.evaluate(() => document.fonts.ready),
  new Promise((r) => setTimeout(r, 10_000)),
]);

if (extraWait > 0) await page.waitForTimeout(extraWait);

// ─── Detect layout style ──────────────────────────────────────────────────
const layoutInfo = await page.evaluate((sel) => {
  const slides = [...document.querySelectorAll(sel)];
  if (!slides.length) return { count: 0, kind: 'none' };
  const first = slides[0];
  const cs = getComputedStyle(first);
  const kind = (cs.position === 'absolute' || cs.position === 'fixed') ? 'deck' : 'flow';
  return { count: slides.length, kind, position: cs.position };
}, slideSelector);

console.log(`[html-to-pdf] detected ${layoutInfo.count} slide(s), layout=${layoutInfo.kind} (slide position:${layoutInfo.position || 'n/a'})`);
if (layoutInfo.count === 0) {
  console.error(`[html-to-pdf] FATAL — no slides matched selector "${slideSelector}"`);
  await browser.close();
  process.exit(2);
}

// ─── Normalize slides for printing ────────────────────────────────────────
// For deck-style HTML, we must forcibly un-stack the slides. For flow-style HTML
// (slides already laid out sequentially), the CSS is a no-op on positioning.
await page.addStyleTag({
  content: `
    @page { size: ${width}px ${height}px; margin: 0; }
    html, body {
      width: auto !important;
      height: auto !important;
      margin: 0 !important;
      padding: 0 !important;
      overflow: visible !important;
      background: #fff !important;
    }
    /* The .deck container in html-ppt decks is position:relative; width:100vw; height:100vh
       which traps slides into one viewport. Free it up. */
    .deck, [class*="deck"] {
      position: static !important;
      width: auto !important;
      height: auto !important;
      overflow: visible !important;
    }
    ${slideSelector} {
      /* position: relative (not static) — preserves this slide as the
         containing block for its absolute-positioned children (logos,
         footers, page numbers, bg-text watermarks). position:static would
         make those children escape up to <html>, collapse onto each other,
         and the last slide's footer would overwrite every page's footer. */
      position: relative !important;
      top: auto !important;
      left: auto !important;
      right: auto !important;
      bottom: auto !important;
      transform: none !important;
      width: ${width}px !important;
      height: ${height}px !important;
      min-height: ${height}px !important;
      max-height: ${height}px !important;
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      pointer-events: auto !important;
      overflow: hidden !important;
      page-break-after: always;
      page-break-inside: avoid;
      break-after: page;
      break-inside: avoid;
      margin: 0 !important;
      float: none !important;
    }
    ${slideSelector}:last-child,
    ${slideSelector}:last-of-type {
      page-break-after: avoid !important;
      break-after: avoid !important;
    }
    /* Kill trailing whitespace after the last slide that Chromium may
       otherwise reserve as an empty 23rd page. */
    body > *:last-child {
      margin-bottom: 0 !important;
      padding-bottom: 0 !important;
    }
    /* Hide deck runtime UI that shouldn't be in a printed deck.
       Covers html-ppt (progress-bar/overview/notes/page-hint), frontend-slides
       (nav-dots/edit-toggle/edit-hotzone), and reveal.js-ish variants. */
    .progress-bar, .notes-overlay, .overview, .notes,
    .theme-indicator, .anim-indicator,
    .nav-dots, .edit-toggle, .edit-hotzone,
    .slide-nav, .slide-controls, .controls,
    .page-hint, .keyboard-hint, .nav-hint {
      display: none !important;
    }
    /* Freeze animations — capture the end state, not a mid-frame */
    *, *::before, *::after {
      animation-duration: 0s !important;
      animation-delay: 0s !important;
      transition-duration: 0s !important;
      transition-delay: 0s !important;
    }
    /* Reveal patterns: elements that start hidden and only appear after scroll
       (frontend-slides .reveal class) or click (html-ppt .reveal-card etc.).
       In a static PDF we want the final state for all of them. */
    ${slideSelector} .reveal,
    ${slideSelector}.reveal,
    ${slideSelector} .reveal-card,
    ${slideSelector} [class*="reveal"],
    ${slideSelector} [class*="fade-"],
    ${slideSelector} [class*="slide-in"],
    .reveal, .reveal-card {
      opacity: 1 !important;
      transform: none !important;
      visibility: visible !important;
    }
  `,
});

// ─── Force reveal state on every slide ───────────────────────────────────
// frontend-slides (and any deck using IntersectionObserver for scroll-triggered
// animations) only adds `.visible` to slides currently in viewport. In PDF export
// there's no scroll, so slides past the first stay invisible. Add `.visible` to
// every slide so whatever CSS the author wrote for "revealed" state kicks in.
await page.evaluate((sel) => {
  document.querySelectorAll(sel).forEach((s) => {
    s.classList.add('visible');
    // Force-reveal descendants that authors hid via inline opacity:0
    // and/or a translate transform (the universal click-to-reveal pattern).
    // We match only inline `opacity: 0` — decorative semi-transparent elements
    // (opacity: 0.95, 0.5, etc.) stay untouched.
    s.querySelectorAll('*').forEach((el) => {
      const inline = el.getAttribute('style') || '';
      let changed = false;
      if (/(^|;)\s*opacity\s*:\s*0\s*(;|$)/i.test(inline)) {
        el.style.setProperty('opacity', '1', 'important');
        changed = true;
      }
      // Strip reveal-pattern translate transforms (translateY(20px),
      // translateX(-40px), etc.). Leaves other transforms intact by just
      // setting it to 'none' only when combined with opacity:0 above.
      if (changed && /transform\s*:[^;]*translate/i.test(inline)) {
        el.style.setProperty('transform', 'none', 'important');
      }
    });
  });
}, slideSelector);

// ─── Fix slide numbers ────────────────────────────────────────────────────
// Authors often do:   <span class="slide-number" data-current="1" data-total="22">01</span>
// combined with CSS:  .slide-number::before { content: attr(data-current); }
//                     .slide-number::after  { content: " / " attr(data-total); }
// which renders as "1 01 / 22" — the infamous "101/22" bug. Clear the textContent and
// set correct data-current/data-total per slide.
const pageNumInfo = await page.evaluate(({ sel, keep }) => {
  const slides = [...document.querySelectorAll(sel)];
  const total = slides.length;
  let fixed = 0;
  let missing = 0;
  slides.forEach((slide, i) => {
    // Walk up: some decks put .slide-number as a child of the slide
    const nums = slide.querySelectorAll('.slide-number');
    if (nums.length === 0) { missing++; return; }
    nums.forEach((n) => {
      n.setAttribute('data-current', String(i + 1));
      n.setAttribute('data-total', String(total));
      if (!keep) n.textContent = '';
      fixed++;
    });
  });
  return { total, fixed, missing };
}, { sel: slideSelector, keep: keepPageNumText });
console.log(`[html-to-pdf] page numbers: fixed ${pageNumInfo.fixed} (${pageNumInfo.missing} slide(s) had none)`);

// Final font wait + a brief settle so layout reflows
await page.evaluate(() => document.fonts.ready).catch(() => {});
await page.waitForTimeout(200);

// ─── Verify slides are actually laid out sequentially now ────────────────
// This is the key regression check for "1-page PDF". After the CSS override,
// the second slide's top should be well below the first. If they still overlap,
// something in the deck's CSS is still winning.
const layoutCheck = await page.evaluate((sel) => {
  const slides = [...document.querySelectorAll(sel)];
  if (slides.length < 2) return { ok: true, reason: 'single-slide' };
  const r0 = slides[0].getBoundingClientRect();
  const r1 = slides[1].getBoundingClientRect();
  return {
    ok: r1.top >= r0.bottom - 1,      // allow 1px slop
    slide0: { top: r0.top, bottom: r0.bottom, height: r0.height },
    slide1: { top: r1.top, bottom: r1.bottom, height: r1.height },
  };
}, slideSelector);
if (!layoutCheck.ok) {
  console.error(`[html-to-pdf] FATAL — slides still overlap after CSS override:`);
  console.error(`  slide[0]: top=${layoutCheck.slide0.top}, bottom=${layoutCheck.slide0.bottom}, height=${layoutCheck.slide0.height}`);
  console.error(`  slide[1]: top=${layoutCheck.slide1.top}, bottom=${layoutCheck.slide1.bottom}, height=${layoutCheck.slide1.height}`);
  console.error(`  The source HTML has CSS that the override couldn't defeat. File an issue.`);
  await browser.close();
  process.exit(3);
}

// ─── Optional debug screenshot ────────────────────────────────────────────
if (debug) {
  const pngPath = outputAbs.replace(/\.pdf$/i, '') + '.debug.png';
  await page.screenshot({ path: pngPath, fullPage: true });
  console.log(`[html-to-pdf] debug screenshot: ${pngPath}`);
}

// ─── Emit the PDF ─────────────────────────────────────────────────────────
await page.pdf({
  path: outputAbs,
  printBackground: true,
  preferCSSPageSize: true,
});

await browser.close();

// ─── Post-flight report ──────────────────────────────────────────────────
const bytes = fs.statSync(outputAbs).size;
console.log(`[html-to-pdf] done — ${outputAbs} (${(bytes / 1024).toFixed(1)} KB)`);
console.log(`[html-to-pdf] expected pages: ${layoutInfo.count}`);

const googleFontFails = [...missingAssets].filter((u) => /fonts\.(googleapis|gstatic)\.com/.test(u));
if (googleFontFails.length > 0) {
  console.warn(`[html-to-pdf] WARNING — ${googleFontFails.length} Google Fonts request(s) failed; fonts will fall back.`);
}
const otherFails = [...missingAssets].filter((u) => !/fonts\.(googleapis|gstatic)\.com/.test(u));
if (otherFails.length > 0) {
  console.warn(`[html-to-pdf] WARNING — ${otherFails.length} other asset(s) failed to load:`);
  for (const u of otherFails) console.warn(`  - ${u}`);
}
