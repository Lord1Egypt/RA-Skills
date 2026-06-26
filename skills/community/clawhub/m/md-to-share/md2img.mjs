#!/usr/bin/env node
import { marked } from 'marked';
import { chromium } from 'playwright';
import { readFileSync, writeFileSync, existsSync, statSync, mkdirSync, unlinkSync } from 'fs';
import { resolve, dirname, extname, basename } from 'path';

// ============================================================================
// Exit Codes - For AI Agent error understanding
// ============================================================================
const EXIT_CODES = {
  SUCCESS: 0,
  INVALID_ARGS: 1,
  FILE_NOT_FOUND: 2,
  FILE_READ_ERROR: 3,
  CHROME_NOT_FOUND: 4,   // kept for backward compat; now means Playwright browser unavailable
  BROWSER_LAUNCH_ERROR: 5,
  RENDER_ERROR: 6,
  SCREENSHOT_ERROR: 7,
  OUTPUT_WRITE_ERROR: 8
};

// ============================================================================
// Configuration Presets - Environment-specific settings
// ============================================================================
const PRESETS = {
  openclaw: {
    width: 600,              // CSS pixels
    deviceScaleFactor: 2,    // Actual output: 1200px (matches OpenClaw Agent limit)
    maxFileSizeMB: 5,        // Matches OpenClaw Agent 5MB limit
    maxHeightPx: 99999,      // No height splitting by default (channel flag overrides this)
    jpegQuality: 85,
    description: 'Optimized for OpenClaw (1200px wide, 5MB limit)'
  },
  generic: {
    width: 800,              // CSS pixels
    deviceScaleFactor: 2,    // Actual output: 1600px
    maxFileSizeMB: 8,
    maxHeightPx: 99999,      // No height splitting by default
    jpegQuality: 85,
    description: 'High resolution for Claude Code / local (1600px wide, 8MB)'
  }
};

// ============================================================================
// Channel-specific overrides - Applied AFTER preset, controls splitting behavior
// ============================================================================
const CHANNELS = {
  discord: {
    maxHeightPx: 1800,       // Under OpenClaw's imageMaxDimensionPx=2000 limit
    maxFileSizeMB: 5,        // Discord + OpenClaw file size limit
    description: 'Discord: auto-split for readability (max 1200×1800px per image)'
  },
  wechat: {
    maxHeightPx: 99999,      // WeChat handles long images natively
    description: 'WeChat: long image preserved (no splitting)'
  },
  imessage: {
    maxHeightPx: 99999,      // iMessage handles long images well
    description: 'iMessage: long image preserved (no splitting)'
  },
  local: {
    maxHeightPx: 99999,      // Local use, no platform constraints
    description: 'Local: original long image (no splitting)'
  }
};

// ============================================================================
// Configuration
// ============================================================================
const CONFIG = {
  // Default output width in CSS pixels (actual pixels = width * deviceScaleFactor)
  width: 800,
  // Device scale factor for high-DPI output (2 = 1600px actual width)
  deviceScaleFactor: 2,
  // JPEG quality (1-100)
  jpegQuality: 85,
  // Maximum file size in bytes before splitting (8MB for Discord)
  maxFileSizeMB: 8,
  // Maximum actual pixel height per image before splitting
  // Default: no splitting. Use --channel=discord to enable height-based splitting.
  maxHeightPx: 99999,
  // Target channel (null = not specified, agents should ask user)
  channel: null,
  // Browser operation timeout (30 seconds default, configurable via --timeout or MD2IMG_TIMEOUT)
  timeout: parseInt(process.env.MD2IMG_TIMEOUT, 10) || 30000,
  // Default output format
  defaultFormat: 'jpeg',
  // Auto theme: day hours (6:00-18:00 = light, 18:00-6:00 = dark)
  dayHourStart: 6,
  dayHourEnd: 18,
  // Current preset name
  preset: 'generic',
  // Force theme (optional: 'light' or 'dark')
  forceTheme: null
};

// ============================================================================
// Environment Detection - Auto-detect OpenClaw vs generic
// ============================================================================
function detectEnvironment() {
  // OpenClaw environment characteristics
  if (process.env.OPENCLAW_CHANNEL ||
      process.env.OPENCLAW_SKILLS_DIR ||
      process.cwd().includes('.openclaw/skills') ||
      process.cwd().includes('.openclaw\\skills')) {
    return 'openclaw';
  }
  return 'generic';
}

function applyPreset(presetName) {
  const preset = PRESETS[presetName];
  if (!preset) {
    console.error(`[WARN] Unknown preset: ${presetName}, using generic`);
    presetName = 'generic';
  }
  const actualPreset = PRESETS[presetName];
  CONFIG.width = actualPreset.width;
  CONFIG.deviceScaleFactor = actualPreset.deviceScaleFactor;
  CONFIG.maxFileSizeMB = actualPreset.maxFileSizeMB;
  CONFIG.maxHeightPx = actualPreset.maxHeightPx;
  CONFIG.jpegQuality = actualPreset.jpegQuality;
  CONFIG.preset = presetName;
  console.log(`[INFO] Applied preset: ${presetName} (${actualPreset.description})`);
}

// ============================================================================
// Theme Detection - Light/Dark mode based on time
// ============================================================================
function getThemeByTime() {
  // Support forced theme override
  if (CONFIG.forceTheme) {
    return CONFIG.forceTheme;
  }
  const hour = new Date().getHours();
  const isDayTime = hour >= CONFIG.dayHourStart && hour < CONFIG.dayHourEnd;
  return isDayTime ? 'light' : 'dark';
}

// ============================================================================
// Theme Styles - Light and Dark mode CSS
// ============================================================================
const THEMES = {
  light: {
    bg: '#ffffff',
    text: '#333333',
    h1Text: '#2c3e50',
    h1Border: '#ff6b6b',
    h2Text: '#34495e',
    h2Border: '#3498db',
    h3Text: '#7f8c8d',
    tableBorder: '#e0e0e0',
    thBg: '#f8f9fa',
    thText: '#2c3e50',
    trEvenBg: '#fafafa',
    trHoverBg: '#f5f5f5',
    inlineCodeBg: '#f4f4f4',
    inlineCodeText: '#e74c3c',
    preBg: '#2d2d2d',
    preText: '#f8f8f2',
    blockquoteBg: '#f9f9f9',
    blockquoteText: '#666666',
    blockquoteBorder: '#3498db',
    hrBorder: '#eeeeee',
    link: '#3498db',
    strongText: '#2c3e50',
    emText: '#7f8c8d'
  },
  dark: {
    bg: '#1a1a2e',
    text: '#e0e0e0',
    h1Text: '#eaeaea',
    h1Border: '#ff6b6b',
    h2Text: '#e8e8e8',
    h2Border: '#4fc3f7',
    h3Text: '#b0b0b0',
    tableBorder: '#3a3a5a',
    thBg: '#252540',
    thText: '#ffffff',
    trEvenBg: '#202035',
    trHoverBg: '#2a2a45',
    inlineCodeBg: '#2d2d4a',
    inlineCodeText: '#ff79c6',
    preBg: '#0d0d1a',
    preText: '#f8f8f2',
    blockquoteBg: '#202035',
    blockquoteText: '#a0a0a0',
    blockquoteBorder: '#4fc3f7',
    hrBorder: '#3a3a5a',
    link: '#4fc3f7',
    strongText: '#ffffff',
    emText: '#b0b0b0'
  }
};

// ============================================================================
// Argument Parsing
// ============================================================================
function parseArgs() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log('MD to Share - Markdown to Long Image Converter (Playwright)');
    console.log('');
    console.log('Usage: md2img <input.md> [output] [options]');
    console.log('');
    console.log('Arguments:');
    console.log('  input.md   Input markdown file (required)');
    console.log('  output     Output image path (optional, defaults to input-长图.jpg)');
    console.log('');
    console.log('Options:');
    console.log('  --preset=<name>     Configuration preset: openclaw | generic (default: auto-detect)');
    console.log('  --channel=<name>    Target channel: discord | wechat | imessage | local');
    console.log('                      discord: auto-split tall images for readability');
    console.log('                      wechat/imessage/local: keep original long image');
    console.log('  --width=<px>        CSS width in pixels (default: preset value)');
    console.log('  --scale=<factor>    Device scale factor (default: 2)');
    console.log('  --max-size=<MB>     Max file size before splitting (default: preset value)');
    console.log('  --max-height=<px>   Max actual pixel height per image (default: channel value)');
    console.log('  --quality=<1-100>   JPEG quality (default: 85)');
    console.log('  --theme=<light|dark> Force theme (default: auto by time)');
    console.log('  --timeout=<ms>      Browser operation timeout in ms (default: 30000)');
    console.log('');
    console.log('Presets:');
    console.log('  openclaw  1200px wide, 5MB limit (for OpenClaw agents)');
    console.log('  generic   1600px wide, 8MB limit (for Claude Code/local)');
    console.log('');
    console.log('Output formats:');
    console.log('  .jpg/.jpeg  JPEG format (default, smaller file size)');
    console.log('  .png        PNG format (lossless, larger file size)');
    console.log('');
    console.log('Features:');
    console.log('  - Bundled Chromium via Playwright (no system Chrome needed)');
    console.log('  - Environment auto-detection (OpenClaw vs generic)');
    console.log('  - High resolution output with configurable scale factor');
    console.log('  - Channel-aware splitting (Discord=split, WeChat/iMessage=long image)');
    console.log('  - Auto theme: light mode (6:00-18:00), dark mode (18:00-6:00)');
    console.log('  - Browser launch retry for robustness');
    console.log('');
    console.log('Environment variables:');
    console.log('  CHROME_PATH      Override browser executable path');
    console.log('  MD2IMG_TIMEOUT   Override default timeout in ms');
    console.log('');
    console.log('Exit codes:');
    console.log('  0 - Success');
    console.log('  1 - Invalid arguments');
    console.log('  2 - Input file not found');
    console.log('  3 - File read error');
    console.log('  4 - Browser not found (run: npx playwright install chromium)');
    console.log('  5 - Browser launch error');
    console.log('  6 - Render error');
    console.log('  7 - Screenshot error');
    console.log('  8 - Output write error');
    process.exit(args.length === 0 ? EXIT_CODES.INVALID_ARGS : EXIT_CODES.SUCCESS);
  }

  // Separate flag arguments from positional arguments
  const flagArgs = args.filter(arg => arg.startsWith('--'));
  const positionalArgs = args.filter(arg => !arg.startsWith('--'));

  let preset = null;
  let channel = null;
  const customOverrides = {};

  // Parse flag arguments - track which values were explicitly set
  for (const flag of flagArgs) {
    if (flag.startsWith('--preset=')) {
      preset = flag.split('=')[1];
    } else if (flag.startsWith('--channel=')) {
      channel = flag.split('=')[1].toLowerCase();
    } else if (flag.startsWith('--width=')) {
      customOverrides.width = parseInt(flag.split('=')[1], 10);
    } else if (flag.startsWith('--scale=')) {
      customOverrides.deviceScaleFactor = parseFloat(flag.split('=')[1]);
    } else if (flag.startsWith('--max-size=')) {
      customOverrides.maxFileSizeMB = parseInt(flag.split('=')[1], 10);
    } else if (flag.startsWith('--max-height=')) {
      customOverrides.maxHeightPx = parseInt(flag.split('=')[1], 10);
    } else if (flag.startsWith('--quality=')) {
      customOverrides.jpegQuality = parseInt(flag.split('=')[1], 10);
    } else if (flag.startsWith('--timeout=')) {
      customOverrides.timeout = parseInt(flag.split('=')[1], 10);
    } else if (flag === '--theme=light') {
      CONFIG.forceTheme = 'light';
    } else if (flag === '--theme=dark') {
      CONFIG.forceTheme = 'dark';
    }
  }

  if (positionalArgs.length === 0) {
    console.error('[ERROR] Missing input file');
    process.exit(EXIT_CODES.INVALID_ARGS);
  }

  const input = positionalArgs[0];
  let output = positionalArgs[1];

  // Default output path if not provided
  if (!output) {
    output = input.replace(/\.md$/i, '-长图.jpg');
  }

  // Auto-detect preset if not specified
  if (!preset) {
    preset = detectEnvironment();
  }
  applyPreset(preset);

  // Apply channel-specific overrides (after preset, before custom overrides)
  if (channel) {
    const channelConfig = CHANNELS[channel];
    if (channelConfig) {
      if (channelConfig.maxHeightPx !== undefined) CONFIG.maxHeightPx = channelConfig.maxHeightPx;
      if (channelConfig.maxFileSizeMB !== undefined) CONFIG.maxFileSizeMB = channelConfig.maxFileSizeMB;
      CONFIG.channel = channel;
      console.log(`[INFO] Channel: ${channel} (${channelConfig.description})`);
    } else {
      console.log(`[WARN] Unknown channel "${channel}", treating as local (no splitting)`);
      CONFIG.channel = channel;
    }
  }

  // Apply custom overrides last (explicit flags take highest precedence)
  Object.assign(CONFIG, customOverrides);
  if (Object.keys(customOverrides).length > 0) {
    console.log(`[INFO] Custom overrides applied: ${Object.keys(customOverrides).join(', ')}`);
  }

  return { input, output };
}

// ============================================================================
// Input Validation
// ============================================================================
function validateInput(inputPath) {
  // Check file exists
  if (!existsSync(inputPath)) {
    console.error(`[ERROR] Input file not found: ${inputPath}`);
    process.exit(EXIT_CODES.FILE_NOT_FOUND);
  }

  // Check file is readable
  try {
    statSync(inputPath);
  } catch (e) {
    console.error(`[ERROR] Cannot read input file: ${inputPath}`);
    console.error(`  ${e.message}`);
    process.exit(EXIT_CODES.FILE_READ_ERROR);
  }

  return true;
}

function validateOutputPath(outputPath) {
  const outputDir = dirname(resolve(outputPath));

  // Create output directory if it doesn't exist
  if (!existsSync(outputDir)) {
    try {
      mkdirSync(outputDir, { recursive: true });
    } catch (e) {
      console.error(`[ERROR] Cannot create output directory: ${outputDir}`);
      console.error(`  ${e.message}`);
      process.exit(EXIT_CODES.OUTPUT_WRITE_ERROR);
    }
  }

  return true;
}

// ============================================================================
// HTML Template
// ============================================================================
function generateHtmlTemplate(content, theme = 'light') {
  const t = THEMES[theme];

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      max-width: ${CONFIG.width}px;
      margin: 0 auto;
      padding: 40px 30px;
      background: ${t.bg};
      color: ${t.text};
      line-height: 1.8;
    }
    h1 {
      font-size: 32px;
      border-bottom: 3px solid ${t.h1Border};
      padding-bottom: 12px;
      color: ${t.h1Text};
      margin-bottom: 24px;
    }
    h2 {
      font-size: 24px;
      margin-top: 32px;
      margin-bottom: 16px;
      color: ${t.h2Text};
      border-left: 4px solid ${t.h2Border};
      padding-left: 12px;
    }
    h3 {
      font-size: 20px;
      margin-top: 24px;
      margin-bottom: 12px;
      color: ${t.h3Text};
    }
    p { margin: 16px 0; }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 20px 0;
      font-size: 14px;
    }
    th, td {
      border: 1px solid ${t.tableBorder};
      padding: 12px 14px;
      text-align: left;
    }
    th {
      background: ${t.thBg};
      font-weight: 600;
      color: ${t.thText};
    }
    tr:nth-child(even) { background: ${t.trEvenBg}; }
    tr:hover { background: ${t.trHoverBg}; }
    code {
      background: ${t.inlineCodeBg};
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'SF Mono', Monaco, Consolas, monospace;
      font-size: 0.9em;
      color: ${t.inlineCodeText};
    }
    pre {
      background: ${t.preBg};
      color: ${t.preText};
      padding: 16px;
      border-radius: 8px;
      overflow-x: auto;
      margin: 16px 0;
    }
    pre code {
      background: none;
      padding: 0;
      color: inherit;
    }
    blockquote {
      border-left: 4px solid ${t.blockquoteBorder};
      margin: 20px 0;
      padding: 12px 20px;
      background: ${t.blockquoteBg};
      color: ${t.blockquoteText};
      border-radius: 0 8px 8px 0;
    }
    hr {
      border: none;
      border-top: 2px solid ${t.hrBorder};
      margin: 40px 0;
    }
    ul, ol {
      padding-left: 24px;
      margin: 16px 0;
    }
    li { margin: 8px 0; }
    a { color: ${t.link}; text-decoration: none; }
    a:hover { text-decoration: underline; }
    img { max-width: 100%; border-radius: 8px; margin: 16px 0; }
    strong { color: ${t.strongText}; }
    em { color: ${t.emText}; }
  </style>
</head>
<body>
${content}
</body>
</html>
`;
}

// ============================================================================
// Image Splitting - Semantic boundary detection
// ============================================================================
async function getContentSections(page) {
  return await page.evaluate(() => {
    const sections = [];
    const headings = document.querySelectorAll('h1, h2, h3, hr');

    headings.forEach(el => {
      const tagName = el.tagName.toLowerCase();
      const rect = el.getBoundingClientRect();
      const scrollTop = window.scrollY || document.documentElement.scrollTop;

      sections.push({
        type: tagName,
        y: Math.round(rect.top + scrollTop),
        priority: tagName === 'h1' ? 1 : tagName === 'h2' ? 2 : tagName === 'h3' ? 3 : 4
      });
    });

    return sections;
  });
}

function findSplitPoints(sections, totalHeight, targetCount) {
  if (targetCount <= 1 || sections.length === 0) {
    return [];
  }

  const idealHeight = totalHeight / targetCount;
  const splitPoints = [];

  for (let i = 1; i < targetCount; i++) {
    const targetY = i * idealHeight;

    // Find the best section near the target position
    let bestSection = null;
    let bestDistance = Infinity;

    for (const section of sections) {
      // Only consider h1, h2, or hr for splitting (priority 1, 2, 4)
      if (section.priority > 3) continue;

      const distance = Math.abs(section.y - targetY);

      // Prefer sections within 20% of ideal segment height
      if (distance < idealHeight * 0.3 && distance < bestDistance) {
        bestDistance = distance;
        bestSection = section;
      }
    }

    if (bestSection) {
      splitPoints.push(bestSection.y);
    } else {
      // Fallback: split at exact position
      splitPoints.push(Math.round(targetY));
    }
  }

  return splitPoints;
}

// ============================================================================
// Browser Launch with Retry
// ============================================================================
async function launchBrowser(maxRetries = 2) {
  const launchOptions = {
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--disable-gpu'
    ]
  };

  // Allow overriding browser executable (e.g. system Chrome)
  if (process.env.CHROME_PATH) {
    launchOptions.executablePath = process.env.CHROME_PATH;
    console.log(`[INFO] Using custom browser: ${process.env.CHROME_PATH}`);
  } else {
    console.log(`[INFO] Using Playwright bundled Chromium`);
  }

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await chromium.launch(launchOptions);
    } catch (e) {
      if (attempt === maxRetries) {
        throw e;
      }
      console.log(`[WARN] Browser launch failed (attempt ${attempt + 1}/${maxRetries + 1}), retrying in 1s...`);
      console.log(`[WARN]   ${e.message}`);
      await new Promise(r => setTimeout(r, 1000));
    }
  }
}

// ============================================================================
// Main Conversion Logic
// ============================================================================
async function convertMarkdownToImage(input, output, context) {
  const inputPath = resolve(input);
  const outputPath = resolve(output);

  // Determine output format
  const ext = extname(outputPath).toLowerCase();
  const isPng = ext === '.png';
  const format = isPng ? 'png' : 'jpeg';

  // Auto-detect theme based on time
  const theme = getThemeByTime();
  const themeName = theme === 'light' ? '浅色' : '深色';

  console.log(`[INFO] Converting: ${input}`);
  console.log(`[INFO] Output format: ${format.toUpperCase()}`);
  console.log(`[INFO] Theme: ${themeName}模式 (${theme})`);

  // Read and parse markdown
  let md, html;
  try {
    md = readFileSync(inputPath, 'utf-8');
    html = await marked(md);
  } catch (e) {
    console.error(`[ERROR] Failed to read/parse markdown: ${e.message}`);
    throw { code: EXIT_CODES.FILE_READ_ERROR, message: e.message };
  }

  const fullHtml = generateHtmlTemplate(html, theme);

  // Create page and render
  let page;
  try {
    page = await context.newPage();
    page.setDefaultTimeout(CONFIG.timeout);
    await page.setContent(fullHtml, { waitUntil: 'networkidle' });
  } catch (e) {
    console.error(`[ERROR] Failed to render page: ${e.message}`);
    if (page) await page.close().catch(() => {});
    throw { code: EXIT_CODES.RENDER_ERROR, message: e.message };
  }

  // Get content dimensions (CSS pixels)
  const cssHeight = await page.evaluate(() => document.documentElement.scrollHeight);
  const actualHeight = cssHeight * CONFIG.deviceScaleFactor;
  const actualWidth = CONFIG.width * CONFIG.deviceScaleFactor;

  // Max CSS height per split (derived from maxHeightPx in actual pixels)
  const maxCSSHeight = Math.floor(CONFIG.maxHeightPx / CONFIG.deviceScaleFactor);

  console.log(`[INFO] Content: ${actualWidth}×${actualHeight}px (CSS: ${CONFIG.width}×${cssHeight}px)`);

  // Determine if splitting is needed based on HEIGHT
  const needsHeightSplit = actualHeight > CONFIG.maxHeightPx;

  if (needsHeightSplit) {
    // --- Height-based smart splitting ---
    const heightSplitCount = Math.ceil(cssHeight / maxCSSHeight);
    console.log(`[INFO] Height ${actualHeight}px exceeds ${CONFIG.maxHeightPx}px limit`);
    console.log(`[INFO] Smart splitting into ~${heightSplitCount} segments at semantic boundaries...`);

    const sections = await getContentSections(page);
    const splitPoints = findSplitPoints(sections, cssHeight, heightSplitCount);

    // Ensure we have split points; fallback to uniform height splits
    if (splitPoints.length === 0) {
      for (let i = 1; i < heightSplitCount; i++) {
        splitPoints.push(Math.round(i * cssHeight / heightSplitCount));
      }
    }

    const outputBase = outputPath.replace(/\.[^.]+$/, '');
    const outputExt = extname(outputPath);
    const outputFiles = [];

    // Set viewport to full height so the entire content is laid out
    await page.setViewportSize({
      width: CONFIG.width,
      height: cssHeight
    });

    for (let i = 0; i <= splitPoints.length; i++) {
      const startY = i === 0 ? 0 : splitPoints[i - 1];
      const endY = i === splitPoints.length ? cssHeight : splitPoints[i];
      const segmentHeight = endY - startY;

      if (segmentHeight <= 0) continue;

      const segmentPath = `${outputBase}-${i + 1}${outputExt}`;
      const screenshotOptions = {
        path: segmentPath,
        type: format,
        clip: {
          x: 0,
          y: startY,
          width: CONFIG.width,
          height: segmentHeight
        }
      };

      if (format === 'jpeg') {
        screenshotOptions.quality = CONFIG.jpegQuality;
      }

      try {
        await page.screenshot(screenshotOptions);
      } catch (e) {
        console.error(`[ERROR] Failed to capture segment ${i + 1}: ${e.message}`);
        await page.close().catch(() => {});
        throw { code: EXIT_CODES.SCREENSHOT_ERROR, message: e.message };
      }

      const segSize = statSync(segmentPath).size / (1024 * 1024);
      outputFiles.push(segmentPath);
      const segActualH = segmentHeight * CONFIG.deviceScaleFactor;
      console.log(`[INFO] Split ${i + 1}/${splitPoints.length + 1}: ${actualWidth}×${segActualH}px, ${segSize.toFixed(2)}MB → ${segmentPath}`);
    }

    await page.close();

    console.log(`[SUCCESS] Generated ${outputFiles.length} images:`);
    outputFiles.forEach((f, idx) => console.log(`  ${idx + 1}. ${f}`));

    return outputFiles;
  }

  // --- No height split needed: single image ---
  await page.setViewportSize({
    width: CONFIG.width,
    height: Math.max(cssHeight, 100)
  });

  try {
    const screenshotOptions = {
      path: outputPath,
      fullPage: true,
      type: format
    };

    if (format === 'jpeg') {
      screenshotOptions.quality = CONFIG.jpegQuality;
    }

    await page.screenshot(screenshotOptions);
  } catch (e) {
    console.error(`[ERROR] Failed to take screenshot: ${e.message}`);
    await page.close().catch(() => {});
    throw { code: EXIT_CODES.SCREENSHOT_ERROR, message: e.message };
  }

  await page.close();

  // Post-check: if file size exceeds limit, re-split by file size
  const stats = statSync(outputPath);
  const fileSizeMB = stats.size / (1024 * 1024);

  if (fileSizeMB > CONFIG.maxFileSizeMB) {
    console.log(`[INFO] File size (${fileSizeMB.toFixed(2)}MB) exceeds ${CONFIG.maxFileSizeMB}MB limit`);
    console.log(`[INFO] Re-splitting by file size...`);

    const splitPage = await context.newPage();
    splitPage.setDefaultTimeout(CONFIG.timeout);
    await splitPage.setContent(fullHtml, { waitUntil: 'networkidle' });
    await splitPage.setViewportSize({ width: CONFIG.width, height: cssHeight });

    const sections = await getContentSections(splitPage);
    const splitCount = Math.ceil(fileSizeMB / CONFIG.maxFileSizeMB);
    const splitPoints = findSplitPoints(sections, cssHeight, splitCount);

    if (splitPoints.length > 0) {
      const outputBase = outputPath.replace(/\.[^.]+$/, '');
      const outputExt = extname(outputPath);
      const outputFiles = [];

      for (let i = 0; i <= splitPoints.length; i++) {
        const startY = i === 0 ? 0 : splitPoints[i - 1];
        const endY = i === splitPoints.length ? cssHeight : splitPoints[i];
        const segmentHeight = endY - startY;

        if (segmentHeight <= 0) continue;

        const segmentPath = `${outputBase}-${i + 1}${outputExt}`;
        const screenshotOptions = {
          path: segmentPath,
          type: format,
          clip: { x: 0, y: startY, width: CONFIG.width, height: segmentHeight }
        };

        if (format === 'jpeg') {
          screenshotOptions.quality = CONFIG.jpegQuality;
        }

        await splitPage.screenshot(screenshotOptions);
        outputFiles.push(segmentPath);
        console.log(`[INFO] Split ${i + 1}/${splitPoints.length + 1}: ${segmentPath}`);
      }

      await splitPage.close();
      unlinkSync(outputPath);

      console.log(`[SUCCESS] Generated ${outputFiles.length} images:`);
      outputFiles.forEach((f, idx) => console.log(`  ${idx + 1}. ${f}`));
      return outputFiles;
    } else {
      console.log(`[WARN] Could not find suitable split points. Output may exceed size limit.`);
      await splitPage.close();
    }
  }

  console.log(`[SUCCESS] Image saved: ${outputPath}`);
  console.log(`[INFO] Dimensions: ${actualWidth}×${actualHeight}px, Size: ${fileSizeMB.toFixed(2)}MB`);

  return [outputPath];
}

// ============================================================================
// Main Entry Point
// ============================================================================
async function main() {
  const { input, output } = parseArgs();

  // Validate inputs
  validateInput(input);
  validateOutputPath(output);

  let browser = null;

  try {
    // Launch browser with retry
    try {
      browser = await launchBrowser();
    } catch (e) {
      console.error(`[ERROR] Failed to launch browser: ${e.message}`);
      console.error('');
      console.error('Ensure Playwright Chromium is installed:');
      console.error('  npx playwright install chromium');
      process.exit(EXIT_CODES.BROWSER_LAUNCH_ERROR);
    }

    // Create browser context with deviceScaleFactor for high-DPI rendering
    const context = await browser.newContext({
      viewport: { width: CONFIG.width, height: 100 },
      deviceScaleFactor: CONFIG.deviceScaleFactor
    });

    // Convert
    await convertMarkdownToImage(input, output, context);

    // Clean up context
    await context.close();

  } catch (error) {
    if (error.code) {
      process.exit(error.code);
    } else {
      console.error(`[ERROR] Unexpected error: ${error.message}`);
      process.exit(EXIT_CODES.RENDER_ERROR);
    }
  } finally {
    // Always close browser
    if (browser) {
      await browser.close().catch(() => {});
    }
  }
}

main();
