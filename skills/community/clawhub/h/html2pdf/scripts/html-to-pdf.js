#!/usr/bin/env node
/**
 * html-to-pdf.js — Convert an HTML file to PDF using Puppeteer (headless Chrome)
 *
 * Usage:
 *   node html-to-pdf.js <input.html> <output.pdf> [--paginated] [--format A4]
 *
 * Options:
 *   --paginated         Use A4-paginated mode (default: single-page, full-height)
 *   --format <fmt>      Page format for paginated mode: A4, A3, Letter, Legal (default: A4)
 *   --width <px>        Viewport/page width in pixels for single-page mode (default: 1440)
 *   --wait <ms>         Extra wait after networkidle0 in ms (default: 1000)
 *   --header-footer     Show page number footer in paginated mode
 *
 * Dependencies (install once):
 *   npm install
 *   # Puppeteer automatically downloads a bundled Chromium — no separate browser needed.
 */

const puppeteer = require("puppeteer");
const path = require("path");
const fs = require("fs");

// ─── Argument parsing ────────────────────────────────────────────────────────

function parseArgs() {
  const args = process.argv.slice(2);
  const flag = (name) => args.includes(name);
  const option = (name, fallback) => {
    const i = args.indexOf(name);
    return i !== -1 && args[i + 1] ? args[i + 1] : fallback;
  };

  const inputArg = args.find((a) => !a.startsWith("--") && a.endsWith(".html"));
  const outputArg = args.find((a) => !a.startsWith("--") && a.endsWith(".pdf"));

  if (!inputArg || !outputArg) {
    console.error("Usage: node html-to-pdf.js <input.html> <output.pdf> [--paginated] [--format A4]");
    process.exit(1);
  }

  const inputFile = path.resolve(inputArg);
  if (!fs.existsSync(inputFile)) {
    console.error(`Error: input file not found — ${inputFile}`);
    process.exit(1);
  }

  const outputFile = path.resolve(outputArg);
  const outDir = path.dirname(outputFile);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  return {
    inputFile,
    outputFile,
    paginated: flag("--paginated"),
    format: option("--format", "A4"),
    printWidth: parseInt(option("--width", "1440"), 10),
    waitMs: parseInt(option("--wait", "1000"), 10),
    headerFooter: flag("--header-footer"),
  };
}

// ─── HTML patching ────────────────────────────────────────────────────────────
//
// page.pdf() only embeds WEB fonts into the PDF. System fonts (PingFang SC,
// Hiragino Sans GB, Microsoft YaHei) render on screen but are NOT embedded —
// PDF readers show nothing for CJK text. Fix: load Noto Sans SC from Google
// Fonts so Chrome downloads, uses, and embeds a subset of it in the PDF.

const CJK_FONT_INJECT = `
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style id="cjk-font-fix">
    body, p, span, li, td, th, div, a, label, button, input {
      font-family: 'Inter', 'Noto Sans SC', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6 {
      font-family: 'Playfair Display', 'Noto Sans SC', serif !important;
    }
  </style>
`;

const PRINT_CSS = `
  @media print {
    * { -webkit-print-color-adjust: exact !important; color-adjust: exact !important; }
    .page-break { page-break-before: always; }
    .no-break   { page-break-inside: avoid; }
    h1, h2, h3, h4, h5, h6 { page-break-after: avoid; }
    img { page-break-inside: avoid; }
  }
`;

function patchHtml(html) {
  // Insert right before </head> so it comes after existing font declarations
  if (html.includes("</head>")) {
    return html.replace("</head>", CJK_FONT_INJECT + "\n</head>");
  }
  return CJK_FONT_INJECT + "\n" + html;
}

// ─── PDF generation ───────────────────────────────────────────────────────────

async function generateSinglePage(page, printWidth) {
  const bodyHeight = await page.evaluate(() => document.body.scrollHeight);
  await page.setViewport({ width: printWidth, height: bodyHeight, deviceScaleFactor: 1 });

  const buffer = await page.pdf({
    width: `${printWidth}px`,
    height: `${bodyHeight}px`,
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
    preferCSSPageSize: true,
  });

  return { buffer, label: `single-page ${printWidth}×${bodyHeight}px` };
}

async function generatePaginated(page, format, headerFooter) {
  await page.addStyleTag({ content: PRINT_CSS });

  const footerTemplate = headerFooter
    ? '<div style="font-size:10px;text-align:center;width:100%;margin-bottom:10px;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
    : "";
  const headerTemplate = headerFooter
    ? '<div style="font-size:10px;text-align:center;width:100%;margin-top:10px;"><span class="title"></span></div>'
    : "";

  const buffer = await page.pdf({
    format,
    printBackground: true,
    margin: {
      top:    headerFooter ? "60px" : "20px",
      right:  "20px",
      bottom: headerFooter ? "60px" : "20px",
      left:   "20px",
    },
    displayHeaderFooter: headerFooter,
    headerTemplate,
    footerTemplate,
    preferCSSPageSize: false,
  });

  return { buffer, label: `paginated ${format}` };
}

// ─── Main ─────────────────────────────────────────────────────────────────────

(async () => {
  const { inputFile, outputFile, paginated, format, printWidth, waitMs, headerFooter } = parseArgs();

  // Patch HTML and write temp file next to original so relative assets resolve
  const rawHtml = fs.readFileSync(inputFile, "utf8");
  const tmpFile = path.join(path.dirname(inputFile), `.html-to-pdf-tmp-${Date.now()}.html`);
  fs.writeFileSync(tmpFile, patchHtml(rawHtml), "utf8");

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--font-render-hinting=none",
        "--disable-font-subpixel-positioning",
      ],
    });

    const page = await browser.newPage();
    await page.setViewport({ width: printWidth, height: 800, deviceScaleFactor: 1 });

    // Stay in screen media so Tailwind CDN (screen-only CSS) applies during PDF generation.
    // Without this, page.pdf() switches to print media and Tailwind CDN styles disappear.
    await page.emulateMediaType("screen");

    // networkidle0 waits for Tailwind CDN, Google Fonts, etc. to finish loading
    await page.goto(`file://${tmpFile}`, { waitUntil: "networkidle0", timeout: 60000 });

    // Extra wait for JS-driven CSS (e.g. Tailwind CDN injects styles after network idle)
    if (waitMs > 0) await new Promise((r) => setTimeout(r, waitMs));

    const { buffer, label } = paginated
      ? await generatePaginated(page, format, headerFooter)
      : await generateSinglePage(page, printWidth);

    fs.writeFileSync(outputFile, buffer);
    console.log(`PDF created (${label}): ${outputFile}`);

  } catch (err) {
    const hint =
      err.message.includes("net::ERR_") ? " (check network access for fonts/CDN)" :
      err.message.includes("TimeoutError") ? " (page took too long to load — try --wait 3000)" :
      err.message.includes("Could not find browser") ? " (run: npx puppeteer browsers install chrome)" :
      "";
    console.error(`Error: ${err.message}${hint}`);
    process.exit(1);

  } finally {
    if (browser) await browser.close();
    try { fs.unlinkSync(tmpFile); } catch (_) {}
  }
})();
