#!/usr/bin/env node

/**
 * HTML to Image Converter
 * Converts HTML files to images (PNG, JPEG) using Puppeteer
 *
 * Supported formats: PNG, JPEG
 *
 * Features:
 * - Auto-detect mindmap content size and adapt output dimensions
 * - Configurable PPI for output images (default: 300)
 */

import puppeteer from 'puppeteer';
import fs from 'node:fs';
import path from 'node:path';

// Supported image types
const SUPPORTED_TYPES = ['png', 'jpeg', 'jpg'];

// Default settings
const DEFAULT_QUALITY = 80;
const DEFAULT_PPI = 300;
const DEFAULT_WIDTH = 2560;
const DEFAULT_HEIGHT = 1664;
const DEFAULT_TIMEOUT = 120000;

// Measurement viewport size (large enough to render full content)
const MEASUREMENT_VIEWPORT = { width: 4096, height: 4096 };

/**
 * Display help information
 */
function showHelp() {
  console.log(`
HTML to Image Converter
=======================

Converts HTML files to images (PNG, JPEG) using Puppeteer.

Usage:
  node html-to-image.js [options] <input-html> [output-image]

Arguments:
  input-html                  Path to input HTML file
  output-image                Path to output image (optional, defaults to input name with .png)

Options:
  -t, --type <format>         Output image format: png, jpeg, jpg (default: png)
  --ppi <number>              Pixels per inch for output (default: 300)
  --auto-fit                  Auto-detect mindmap content size and adapt dimensions
  -q, --quality <0-100>       Image quality for JPEG (0-100, default: 80)
  --timeout <ms>              Timeout for rendering in milliseconds (default: 120000)
  --help                      Display this help message
  --version                   Display version information

Examples:
  node html-to-image.js --auto-fit --ppi 300 input.html output.png

Notes:
  - PNG does not support quality parameter (lossless format)
  - JPEG quality ranges from 0 (lowest) to 100 (highest)
  - Resolution is set via CSS on the body element
  - The HTML should include proper styling for best results
`);
}

/**
 * Display version information
 */
function showVersion() {
  console.log('1.1.0');
}

/**
 * Parse command line arguments
 */
function parseArgs(args) {
  const options = {
    type: 'png',
    width: DEFAULT_WIDTH,
    height: DEFAULT_HEIGHT,
    ppi: DEFAULT_PPI,
    autoFit: false,
    quality: DEFAULT_QUALITY,
    timeout: DEFAULT_TIMEOUT,
    input: null,
    output: null
  };

  const parsedArgs = args.slice(2);

  for (let i = 0; i < parsedArgs.length; i++) {
    const arg = parsedArgs[i];

    switch (arg) {
      case '--help':
      case '-h':
        showHelp();
        process.exit(0);
      case '--version':
        showVersion();
        process.exit(0);
      case '-t':
      case '--type':
        i++;
        if (parsedArgs[i]) {
          const type = parsedArgs[i].toLowerCase().replace('.', '');
          if (SUPPORTED_TYPES.includes(type)) {
            options.type = type === 'jpg' ? 'jpeg' : type;
          } else {
            console.error(
              `Error: Unsupported format '${parsedArgs[i]}'. Supported: ${SUPPORTED_TYPES.join(', ')}`
            );
            process.exit(1);
          }
        }
        break;
      case '--width':
        i++;
        options.width = parseInt(parsedArgs[i], 10);
        if (isNaN(options.width) || options.width < 1) {
          console.error('Error: Width must be a positive number');
          process.exit(1);
        }
        break;
      case '--height':
        i++;
        options.height = parseInt(parsedArgs[i], 10);
        if (isNaN(options.height) || options.height < 1) {
          console.error('Error: Height must be a positive number');
          process.exit(1);
        }
        break;
      case '-q':
      case '--quality':
        i++;
        options.quality = parseFloat(parsedArgs[i]);
        if (isNaN(options.quality) || options.quality < 0 || options.quality > 100) {
          console.error('Error: Quality must be a number between 0 and 100');
          process.exit(1);
        }
        break;
      case '--timeout':
        i++;
        options.timeout = parseInt(parsedArgs[i], 10);
        if (isNaN(options.timeout) || options.timeout < 0) {
          console.error('Error: Timeout must be a positive number (milliseconds)');
          process.exit(1);
        }
        break;
      case '--ppi':
        i++;
        options.ppi = parseFloat(parsedArgs[i]);
        if (isNaN(options.ppi) || options.ppi < 1) {
          console.error('Error: PPI must be a positive number');
          process.exit(1);
        }
        break;
      case '--auto-fit':
      case '-a':
        options.autoFit = true;
        break;
      default:
        if (!arg.startsWith('-')) {
          if (!options.input) {
            options.input = arg;
          } else if (!options.output) {
            options.output = arg;
          }
        }
        break;
    }
  }

  return options;
}

/**
 * Measure the actual rendered size of a mindmap SVG using getBBox
 */
async function measureMindmapSize(page) {
  return await page.evaluate(() => {
    const svg = document.querySelector('#mindmap');
    if (!svg) return null;

    // Try to get bounding box from first child element
    const firstChild = svg.firstElementChild;
    if (firstChild && typeof firstChild.getBBox === 'function') {
      try {
        const bbox = firstChild.getBBox();
        return {
          width: Math.ceil(bbox.width),
          height: Math.ceil(bbox.height)
        };
      } catch (e) {
        // Continue to fallback
      }
    }

    // Fallback: compute union bounding box of all children
    const children = svg.children;
    if (children.length === 0) return null;

    let minX = Infinity;
    let minY = Infinity;
    let maxX = -Infinity;
    let maxY = -Infinity;

    for (const child of children) {
      if (typeof child.getBBox === 'function') {
        try {
          const bbox = child.getBBox();
          minX = Math.min(minX, bbox.x);
          minY = Math.min(minY, bbox.y);
          maxX = Math.max(maxX, bbox.x + bbox.width);
          maxY = Math.max(maxY, bbox.y + bbox.height);
        } catch (e) {
          // Skip elements that throw on getBBox
        }
      }
    }

    if (minX === Infinity) {
      const rect = svg.getBoundingClientRect();
      return {
        width: Math.ceil(rect.width),
        height: Math.ceil(rect.height)
      };
    }

    return {
      width: Math.ceil(maxX - minX),
      height: Math.ceil(maxY - minY)
    };
  });
}

/**
 * Wait for markmap to finish rendering
 */
async function waitForMarkmapRender(page, timeout) {
  await page.waitForFunction(
    () => {
      const svg = document.querySelector('#mindmap');
      if (!svg) return false;
      const paths = svg.querySelectorAll('path');
      return paths.length > 0;
    },
    { timeout }
  );

  // Additional wait for markmap to fully settle
  await new Promise((resolve) => setTimeout(resolve, 1000));
}

/**
 * Wrap HTML content with resolution styles
 */
function wrapHtml(html, width, height) {
  let processedHtml = html
    .replace(/<meta[^>]*viewport[^>]*>/gi, '')
    .replace(/#mindmap\s*\{[^}]*width:\s*[^;]*vw[^}]*\}/gi, '#mindmap { width: 100%; height: 100%; }')
    .replace(/#mindmap\s*\{[^}]*height:\s*[^;]*vh[^}]*\}/gi, '#mindmap { width: 100%; height: 100%; }');

  // Remove SVG viewBox and explicit width/height to allow natural scaling to viewport
  // This ensures getBBox() returns CSS pixel dimensions matching the viewport
  processedHtml = processedHtml
    .replace(/<svg([^>]*)viewBox="[^"]*"([^>]*)>/gi, '<svg$1$2>')
    .replace(/<svg([^>]*)\s+viewBox="[^"]*"([^>]*)>/gi, '<svg$1$2>')
    .replace(/<svg([^>]*)(\s+)?width="[^"]*"([^>]*)>/gi, '<svg$1$3>')
    .replace(/<svg([^>]*)(\s+)?height="[^"]*"([^>]*)>/gi, '<svg$1$3>');

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=${width}, height=${height}">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      width: ${width}px;
      height: ${height}px;
      overflow: hidden;
      background-color: transparent;
    }
    #mindmap {
      width: 100%;
      height: 100%;
      display: block;
    }
    #mindmap svg {
      width: 100% !important;
      height: 100% !important;
    }
  </style>
</head>
<body>
${processedHtml}
</body>
</html>`;
}

/**
 * Take screenshot using Puppeteer
 */
async function takeScreenshot(page, outputPath, options) {
  const screenshotOptions = {
    path: outputPath,
    fullPage: true
  };

  if (options.type === 'jpeg') {
    screenshotOptions.type = 'jpeg';
    screenshotOptions.quality = options.quality;
  } else {
    screenshotOptions.type = 'png';
  }

  await page.screenshot(screenshotOptions);
}

/**
 * Main conversion function
 */
async function convert(options) {
  // Validate input file
  if (!options.input) {
    console.error('Error: Input HTML file is required');
    console.log('Run with --help for usage information');
    process.exit(1);
  }

  if (!fs.existsSync(options.input)) {
    console.error(`Error: Input file '${options.input}' does not exist`);
    process.exit(1);
  }

  // Read input HTML
  let htmlContent = fs.readFileSync(options.input, 'utf-8');

  // Generate output filename if not provided
  if (!options.output) {
    const inputBasename = path.basename(options.input, path.extname(options.input));
    options.output = path.join(path.dirname(options.input), `${inputBasename}.${options.type}`);
  }

  // Ensure output has correct extension
  const outputExt = path.extname(options.output).toLowerCase().replace('.', '');
  if (!SUPPORTED_TYPES.includes(outputExt)) {
    options.output = options.output.replace(/\.[^/.]+$/, '') + `.${options.type}`;
  }

  // Launch browser
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();

    // Auto-fit mode: measure mindmap content size first
    if (options.autoFit) {
      console.log('Measuring mindmap content size...');

      // Measure at standard 96 PPI to get CSS pixel dimensions
      await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }]);
      await page.setViewport({
        width: MEASUREMENT_VIEWPORT.width,
        height: MEASUREMENT_VIEWPORT.height,
        deviceScaleFactor: 1,
        colorScheme: 'light'
      });

      const measurementHtml = wrapHtml(htmlContent, MEASUREMENT_VIEWPORT.width, MEASUREMENT_VIEWPORT.height);
      await page.setContent(measurementHtml, { waitUntil: 'domcontentloaded', timeout: options.timeout });

      await waitForMarkmapRender(page, options.timeout);

      const measured = await measureMindmapSize(page);
      if (!measured || measured.width === 0 || measured.height === 0) {
        throw new Error('Could not measure mindmap dimensions');
      }

      console.log(`  Measured content: ${measured.width.toFixed(0)}x${measured.height.toFixed(0)} CSS pixels`);
      console.log(`  Target PPI: ${options.ppi}`);

      // Store measured dimensions (will be used with deviceScaleFactor for final output)
      options.width = Math.ceil(measured.width);
      options.height = Math.ceil(measured.height);
      options.measuredWidth = Math.ceil(measured.width);
      options.measuredHeight = Math.ceil(measured.height);
    }

    // Set viewport for final render (light color scheme)
    await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }]);

    // Calculate deviceScaleFactor to achieve target PPI
    // deviceScaleFactor = target PPI / 96 PPI (browser default)
    const ppiScale = options.ppi / 96;
    await page.setViewport({
      width: options.measuredWidth || options.width,
      height: options.measuredHeight || options.height,
      deviceScaleFactor: ppiScale,
      colorScheme: 'light'
    });

    // Wrap HTML with resolution styles (use measured dimensions for CSS, deviceScaleFactor handles PPI)
    const cssWidth = options.measuredWidth || options.width;
    const cssHeight = options.measuredHeight || options.height;
    htmlContent = wrapHtml(htmlContent, cssWidth, cssHeight);

    console.log(`Converting HTML to ${options.type.toUpperCase()}...`);
    console.log(`  Input:  ${options.input}`);
    console.log(`  Output: ${options.output}`);
    console.log(`  CSS Size: ${cssWidth}x${cssHeight}`);
    console.log(`  Output Size: ${cssWidth * ppiScale}x${cssHeight * ppiScale} (${options.ppi} PPI)`);
    if (options.autoFit) {
      console.log(`  PPI: ${options.ppi}`);
    }
    if (options.type === 'jpeg') {
      console.log(`  Quality: ${options.quality}`);
    }
    console.log(`  Timeout: ${options.timeout}ms`);

    // Set content and wait for DOM to be ready
    // Use 'domcontentloaded' instead of 'networkidle0' or 'load' to avoid waiting
    // for external CDN resources that may be referenced but no longer accessible
    await page.setContent(htmlContent, { waitUntil: 'domcontentloaded', timeout: options.timeout });

    // Wait for markmap to render if present
    const hasMindmap = await page.evaluate(() => !!document.querySelector('#mindmap'));
    if (hasMindmap) {
      await waitForMarkmapRender(page, options.timeout);
    }

    // Take screenshot
    await takeScreenshot(page, options.output, options);

    console.log(`\nImage created successfully: ${options.output}`);
  } catch (error) {
    console.error('Error during conversion:', error.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

// Main execution
const options = parseArgs(process.argv);
await convert(options);
