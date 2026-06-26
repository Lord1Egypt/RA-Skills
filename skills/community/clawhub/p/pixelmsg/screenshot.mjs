#!/usr/bin/env node

/**
 * Generic Widget Screenshot Tool
 *
 * Usage:
 *   node screenshot.mjs <html-file> [options]
 *
 * Options:
 *   --params key=value       URL query parameters (repeatable)
 *   --viewport <preset>      Viewport preset: mobile|tablet|desktop|all (default: all)
 *   --width <number>         Custom viewport width (overrides --viewport)
 *   --height <number>        Custom viewport height (default: 900)
 *   --selector <css>         Element to screenshot (default: #app)
 *   --out <directory>        Output directory (default: ./screenshots)
 *   --name <prefix>          Output filename prefix (default: derived from html filename)
 *   --full-page              Screenshot full page instead of element
 *   --device-scale <number>  Device scale factor for retina (default: 2)
 *
 * Examples:
 *   node screenshot.mjs index.html
 *   node screenshot.mjs index.html --params category=学习 --viewport mobile
 *   node screenshot.mjs index.html --params category=工作 --viewport all --out ./output
 *   node screenshot.mjs index.html --width 400 --height 800 --selector "#app"
 */

import { chromium } from "playwright";
import { resolve, basename } from "path";
import { mkdirSync } from "fs";

const VIEWPORTS = {
  mobile:  { width: 375,  height: 812 },
  tablet:  { width: 768,  height: 1024 },
  desktop: { width: 1440, height: 900 },
};

function parseArgs(args) {
  const opts = {
    file: null,
    params: {},
    viewports: null,
    customWidth: null,
    customHeight: 900,
    selector: "#app",
    outDir: "./screenshots",
    namePrefix: null,
    fullPage: false,
    deviceScale: 2,
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    if (arg === "--params" && args[i + 1]) {
      const [k, ...vParts] = args[++i].split("=");
      opts.params[k] = vParts.join("=");
    } else if (arg === "--viewport" && args[i + 1]) {
      opts.viewports = args[++i];
    } else if (arg === "--width" && args[i + 1]) {
      opts.customWidth = parseInt(args[++i], 10);
    } else if (arg === "--height" && args[i + 1]) {
      opts.customHeight = parseInt(args[++i], 10);
    } else if (arg === "--selector" && args[i + 1]) {
      opts.selector = args[++i];
    } else if (arg === "--out" && args[i + 1]) {
      opts.outDir = args[++i];
    } else if (arg === "--name" && args[i + 1]) {
      opts.namePrefix = args[++i];
    } else if (arg === "--full-page") {
      opts.fullPage = true;
    } else if (arg === "--device-scale" && args[i + 1]) {
      opts.deviceScale = parseFloat(args[++i]);
    } else if (!arg.startsWith("--") && !opts.file) {
      opts.file = arg;
    }
    i++;
  }

  if (!opts.file) {
    console.error("Usage: node screenshot.mjs <html-file> [options]");
    console.error("Run with --help for full usage information.");
    process.exit(1);
  }

  return opts;
}

const opts = parseArgs(process.argv.slice(2));

// Build URL
const htmlPath = resolve(opts.file);
const query = new URLSearchParams(opts.params).toString();
const url = `file://${htmlPath}${query ? "?" + query : ""}`;

// Determine viewports to use
let targets;
if (opts.customWidth) {
  targets = [{ name: `${opts.customWidth}w`, width: opts.customWidth, height: opts.customHeight }];
} else if (opts.viewports && opts.viewports !== "all") {
  const vp = VIEWPORTS[opts.viewports];
  if (!vp) {
    console.error(`Unknown viewport: ${opts.viewports}. Use: mobile, tablet, desktop, all`);
    process.exit(1);
  }
  targets = [{ name: opts.viewports, ...vp }];
} else {
  targets = Object.entries(VIEWPORTS).map(([name, vp]) => ({ name, ...vp }));
}

// Output settings
const prefix = opts.namePrefix || basename(opts.file, ".html");
const paramSuffix = Object.values(opts.params).join("-") || "default";
mkdirSync(opts.outDir, { recursive: true });

// Screenshot
const browser = await chromium.launch();

for (const vp of targets) {
  const page = await browser.newPage({
    viewport: { width: vp.width, height: vp.height },
    deviceScaleFactor: opts.deviceScale,
  });

  await page.goto(url, { waitUntil: "domcontentloaded" });

  // Wait for Alpine.js to render (look for content inside the selector)
  try {
    await page.waitForFunction(
      (sel) => {
        const el = document.querySelector(sel);
        return el && el.children.length > 0 && el.innerHTML.trim().length > 100;
      },
      opts.selector,
      { timeout: 5000 }
    );
  } catch {
    console.warn(`⚠ Timeout waiting for ${opts.selector} to render on ${vp.name}, screenshotting anyway`);
  }

  const filename = `${prefix}-${paramSuffix}-${vp.name}.png`;
  const filepath = `${opts.outDir}/${filename}`;

  if (opts.fullPage) {
    await page.screenshot({ path: filepath, fullPage: true });
  } else {
    const el = page.locator(opts.selector);
    await el.screenshot({ path: filepath });
  }

  console.log(`✓ ${vp.name} (${vp.width}×${vp.height} @${opts.deviceScale}x) → ${filepath}`);
  await page.close();
}

await browser.close();
