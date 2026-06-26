#!/usr/bin/env node
/**
 * extract_slides.js — Phase 1 of Hybrid PPTX Pipeline
 *
 * For each HTML slide:
 *   1. Load in Puppeteer (1280x720)
 *   2. Extract ALL foreground text regions with positioning & style
 *      - Gradient text (background-clip: text) is extracted WITH gradient info
 *      - Only aria-hidden="true" / data-decorative="true" elements are skipped
 *   3. Hide all extracted text, take a clean background screenshot
 *   4. Output JSON manifest + PNG screenshots
 *
 * Key improvements over v1:
 *   - "flow-root" added to block display set (fixes .card-body detection)
 *   - Gradient text IS extracted (with gradient color stops for OOXML a:gradFill)
 *   - All inline children text aggregated into parent block region
 *
 * Usage:
 *   node extract_slides.js <html_dir_or_file> -o <output_dir>
 */

"use strict";

const fs = require("fs");
const path = require("path");

const VIEWPORT_W = 1280;
const VIEWPORT_H = 720;

function naturalSort(a, b) {
  return a.localeCompare(b, undefined, { numeric: true, sensitivity: "base" });
}

function collectHtmlFiles(input) {
  const p = path.resolve(input);
  if (!fs.existsSync(p)) {
    console.error(`Error: ${p} not found`);
    process.exit(1);
  }
  if (fs.statSync(p).isFile()) return [p];
  const files = fs
    .readdirSync(p)
    .filter((f) => f.endsWith(".html") && !f.startsWith("preview"))
    .sort(naturalSort)
    .map((f) => path.join(p, f));
  if (files.length === 0) {
    console.error("Error: no HTML files found in " + p);
    process.exit(1);
  }
  return files;
}

async function extractSlides(htmlFiles, outputDir) {
  const puppeteer = require("puppeteer");
  fs.mkdirSync(outputDir, { recursive: true });

  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu", "--font-render-hinting=none"],
  });

  const manifest = [];

  for (let i = 0; i < htmlFiles.length; i++) {
    const htmlFile = htmlFiles[i];
    const htmlContent = fs.readFileSync(htmlFile, "utf8");
    const slideName = path.basename(htmlFile, ".html");
    const bgFile = path.join(outputDir, `bg-${i}.png`);
    console.log(`  [${i + 1}/${htmlFiles.length}] ${slideName}`);

    const page = await browser.newPage();
    await page.setViewport({ width: VIEWPORT_W, height: VIEWPORT_H });
    await page.setContent(htmlContent, { waitUntil: "networkidle0", timeout: 60000 });
    await page.waitForFunction(() => document.readyState === "complete");
    await new Promise((r) => setTimeout(r, 500));

    const libDir = path.join(__dirname, "lib");
    await page.addScriptTag({ path: path.join(libDir, "constants.js") });
    await page.addScriptTag({ path: path.join(libDir, "color-utils.js") });
    await page.addScriptTag({ path: path.join(libDir, "svg-utils.js") });
    await page.addScriptTag({ path: path.join(libDir, "table-extractor.js") });
    await page.addScriptTag({ path: path.join(libDir, "text-utils.js") });
    await page.addScriptTag({ path: path.join(libDir, "dom-analyzer.js") });

    const extractResult = await page.evaluate(() => window.__extractSlideData());

    const screenshotBuffer = await page.screenshot({
      fullPage: false, type: "png",
      clip: { x: 0, y: 0, width: VIEWPORT_W, height: VIEWPORT_H },
    });
    fs.writeFileSync(bgFile, screenshotBuffer);

    const debugDir = path.join(outputDir, "debug");
    fs.mkdirSync(debugDir, { recursive: true });
    fs.writeFileSync(path.join(debugDir, `bg-only-${i}.png`), screenshotBuffer);

    await page.evaluate(() => {
      const els = document.querySelectorAll('[data-extract-icon="1"]');
      for (const d of els) d.style.removeProperty("visibility");
    });

    const iconElements = await page.$$('[data-extract-icon="1"]');
    const iconRegions = [];
    const svgExtracts = extractResult.svgExtracts || [];

    for (let ic = 0; ic < iconElements.length; ic++) {
      const iconEl = iconElements[ic];
      const iconInfo = await iconEl.evaluate(el => {
        const rect = el.getBoundingClientRect();
        return { x: rect.left, y: rect.top, w: rect.width, h: rect.height };
      });

      if (iconInfo.w < 10 || iconInfo.h < 10) continue;

      // Match via data-svg-idx attribute set by dom-analyzer.
      // Coordinate matching is unreliable because shape border removal
      // causes layout reflow that shifts deco element positions.
      const svgIdxAttr = await iconEl.evaluate(el => el.getAttribute("data-svg-idx"));
      let matchedSvg = null;
      if (svgIdxAttr !== null) {
        const idx = parseInt(svgIdxAttr, 10);
        matchedSvg = svgExtracts[idx] || null;
      }

      const hasContainer = matchedSvg && matchedSvg.containerStyle;
      let useX, useY, useW, useH;
      if (hasContainer) {
        useX = iconInfo.x;
        useY = iconInfo.y;
        useW = iconInfo.w;
        useH = iconInfo.h;
      } else if (matchedSvg) {
        const actualRect = matchedSvg.svgActualRect;
        useX = actualRect ? actualRect.x : matchedSvg.x;
        useY = actualRect ? actualRect.y : matchedSvg.y;
        useW = actualRect ? actualRect.w : matchedSvg.w;
        useH = actualRect ? actualRect.h : matchedSvg.h;
      } else {
        useX = iconInfo.x;
        useY = iconInfo.y;
        useW = iconInfo.w;
        useH = iconInfo.h;
      }

      if (useX > VIEWPORT_W || useY > VIEWPORT_H) continue;
      if (useX + useW < 0 || useY + useH < 0) continue;

      const pngFile = path.join(outputDir, `icon-${i}-${ic}.png`);
      try {
        await iconEl.screenshot({ path: pngFile, type: "png" });
        const entry = {
          image: `icon-${i}-${ic}.png`,
          x: Math.max(0, useX),
          y: Math.max(0, useY),
          w: useW,
          h: useH,
        };
        if (matchedSvg && matchedSvg.isSVG && matchedSvg.svgMarkup) {
          const svgFile = `icon-${i}-${ic}.svg`;
          let markup = matchedSvg.svgMarkup;
          if (!markup.includes('xmlns="')) {
            markup = markup.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
          }
          fs.writeFileSync(path.join(outputDir, svgFile), markup, "utf8");
          entry.svgImage = svgFile;
        }

        // Generate transparent-background fallback PNG via Puppeteer for
        // large SVG icons. CairoSVG cannot render emoji text in <svg><text>
        // elements; Puppeteer's Chromium handles them natively.
        // Ref: https://github.com/Kozea/CairoSVG/issues/434
        const isLargeSvg = matchedSvg && matchedSvg.isSVG && (useW > 120 || useH > 120);
        const hasContainer = matchedSvg && matchedSvg.containerStyle;
        if (isLargeSvg && !hasContainer) {
          const fbFile = path.join(outputDir, `icon-${i}-${ic}_fb.png`);
          try {
            const savedBgs = await page.evaluate((el) => {
              const saved = [];
              let node = el.parentElement;
              while (node && node !== document.documentElement) {
                saved.push({ bg: node.style.background, bgc: node.style.backgroundColor });
                node.style.background = "transparent";
                node.style.backgroundColor = "transparent";
                node = node.parentElement;
              }
              saved.push({
                bodyBg: document.body.style.background,
                bodyBgc: document.body.style.backgroundColor,
                htmlBg: document.documentElement.style.background,
                htmlBgc: document.documentElement.style.backgroundColor,
              });
              document.body.style.background = "transparent";
              document.body.style.backgroundColor = "transparent";
              document.documentElement.style.background = "transparent";
              document.documentElement.style.backgroundColor = "transparent";
              return saved;
            }, iconEl);

            await iconEl.screenshot({ path: fbFile, type: "png", omitBackground: true });

            await page.evaluate((el, saved) => {
              let node = el.parentElement;
              let idx = 0;
              while (node && node !== document.documentElement && idx < saved.length - 1) {
                node.style.background = saved[idx].bg;
                node.style.backgroundColor = saved[idx].bgc;
                node = node.parentElement;
                idx++;
              }
              const last = saved[saved.length - 1];
              document.body.style.background = last.bodyBg || "";
              document.body.style.backgroundColor = last.bodyBgc || "";
              document.documentElement.style.background = last.htmlBg || "";
              document.documentElement.style.backgroundColor = last.htmlBgc || "";
            }, iconEl, savedBgs);

            entry.fallbackImage = `icon-${i}-${ic}_fb.png`;
          } catch (_fbErr) { /* fallback generation is best-effort */ }
        }

        if (matchedSvg && matchedSvg.chartData) {
          entry.chartData = matchedSvg.chartData;
          if (matchedSvg.chartRect) {
            entry.x = Math.max(0, matchedSvg.chartRect.x);
            entry.y = Math.max(0, matchedSvg.chartRect.y);
            entry.w = matchedSvg.chartRect.w;
            entry.h = matchedSvg.chartRect.h;
          }
        }
        if (matchedSvg && matchedSvg.containerStyle) {
          entry.containerStyle = matchedSvg.containerStyle;
          if (matchedSvg.svgActualRect) {
            entry.svgActualRect = matchedSvg.svgActualRect;
          }
          if (matchedSvg.text && !matchedSvg.isSVG && !matchedSvg.svgMarkup) {
            entry.containerText = matchedSvg.text;
            if (matchedSvg.textStyle) {
              entry.textStyle = matchedSvg.textStyle;
            }
          }
        }
        iconRegions.push(entry);
      } catch (_) { /* element may not be screenshottable */ }
    }

    manifest.push({
      index: i, name: slideName,
      bgImage: `bg-${i}.png`,
      viewportW: extractResult.viewportW,
      viewportH: extractResult.viewportH,
      textRegions: extractResult.regions,
      shapeRegions: extractResult.shapeRegions || [],
      iconRegions,
      tableRegions: extractResult.tableRegions || [],
      cssVarPalette: extractResult.cssVarPalette || {},
    });

    const gradCount = extractResult.regions.filter(r => r.gradient).length;
    const shapeCount = (extractResult.shapeRegions || []).length;
    console.log(`    bg: ${(screenshotBuffer.length/1024).toFixed(0)}KB | texts: ${extractResult.regions.length} (${gradCount} gradient) | shapes: ${shapeCount} | icons: ${iconRegions.length}`);
    await page.close();
  }

  await browser.close();

  const manifestPath = path.join(outputDir, "manifest.json");
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
  console.log(`Manifest: ${manifestPath}`);
  return manifest;
}

function main() {
  const args = process.argv.slice(2);
  let input = null;
  let outputDir = "/tmp/slide-extract";

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "-o" || args[i] === "--output") { outputDir = args[++i]; }
    else if (!input) { input = args[i]; }
  }

  if (!input) {
    console.error("Usage: node extract_slides.js <html_dir_or_file> -o <output_dir>");
    process.exit(1);
  }

  const htmlFiles = collectHtmlFiles(input);
  console.log(`[extract] ${htmlFiles.length} HTML slides -> ${outputDir}`);
  extractSlides(htmlFiles, outputDir).catch((err) => {
    console.error("Fatal:", err);
    process.exit(1);
  });
}

main();
