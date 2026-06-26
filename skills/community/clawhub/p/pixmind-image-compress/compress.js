import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, statSync } from 'fs';
import { join, dirname, basename, extname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { homedir } from 'os';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..', '..');

// Presets
const PRESETS = {
  web: { quality: 75, format: 'webp' },
  wechat: { quality: 65, format: 'jpg' },
  email: { quality: 55, format: 'jpg' },
  quality: { quality: 95 },
  thumbnail: { quality: 60, format: 'webp' },
};

const IMAGE_EXTS = new Set(['.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.heic', '.heif', '.avif', '.tpg']);

// Load .env
function loadEnv() {
  try {
    const content = readFileSync(join(ROOT, '.env'), 'utf8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eq = trimmed.indexOf('=');
      if (eq === -1) continue;
      const key = trimmed.slice(0, eq).trim();
      const val = trimmed.slice(eq + 1).trim();
      if (!process.env[key]) process.env[key] = val;
    }
  } catch {}
}
loadEnv();

const APP_KEY = process.env.PIXMIND_APP_KEY || 'app_7867c26ab713fb03aec0774ed28f5802';
const API_KEY = process.env.PIXMIND_API_KEY;
const API_BASE = (process.env.PIXMIND_API_BASE || 'https://aihub-admin.aimix.pro').replace(/\/+$/, '');

// Parse CLI args
function parseArgs(args) {
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        opts[key] = args[++i];
      } else {
        opts[key] = true;
      }
    }
  }
  return opts;
}

function printHelp() {
  console.log(`
Usage: node compress.js <options>

Input (one of):
  --url <url>            Image URL to compress
  --file <path>          Local image file path
  --dir <path>           Directory for batch processing

Options:
  --format <fmt>         Output format: webp, jpg, png, avif, heif, tpg
  --quality <1-100>      Compression quality (default: 75)
  --width <px>           Target width (maintain aspect ratio)
  --height <px>          Target height (maintain aspect ratio)
  --preset <name>        Preset: web, wechat, email, quality, thumbnail
  --output <dir>         Output directory (default: ~/Downloads/compressed-images/<date>)
  --recursive            Process subdirectories
  --mode <type>          Response type: url or base64 (default: url)

Presets:
  web        quality=75, format=webp    — Web display
  wechat     quality=65, format=jpg     — WeChat/social media
  email      quality=55, format=jpg     — Email attachments
  quality    quality=95                 — High-quality archiving
  thumbnail  quality=60, format=webp    — Thumbnails/previews

Examples:
  node compress.js --file photo.png --preset web
  node compress.js --url https://example.com/img.jpg --quality 80 --format webp
  node compress.js --file photo.jpg --width 1920 --quality 75
  node compress.js --dir ~/Pictures/ --preset web --recursive
`);
}

function fileToBase64(filePath) {
  const ext = extname(filePath).toLowerCase().replace('.jpeg', '.jpg').slice(1);
  const mimeMap = { jpg: 'jpeg', png: 'png', webp: 'webp', gif: 'gif', bmp: 'bmp', heic: 'heic', heif: 'heif', avif: 'avif', tpg: 'tpg' };
  const mime = `image/${mimeMap[ext] || 'jpeg'}`;
  const data = readFileSync(filePath);
  return `data:${mime};base64,${data.toString('base64')}`;
}

function getOutputDir(customDir) {
  if (customDir) return resolve(customDir);
  const date = new Date().toISOString().slice(0, 10);
  return join(homedir(), 'Downloads', 'compressed-images', date);
}

function getOutputPath(outputDir, originalName, format) {
  const base = basename(originalName, extname(originalName));
  const ext = format ? `.${format}` : extname(originalName);
  let candidate = join(outputDir, `${base}${ext}`);
  let i = 1;
  while (existsSync(candidate)) {
    candidate = join(outputDir, `${base}_${String(i).padStart(3, '0')}${ext}`);
    i++;
  }
  return candidate;
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

async function compressImage(body) {
  if (!API_KEY) {
    console.error('Error: PIXMIND_API_KEY not set. Create .env file with PIXMIND_API_KEY=xxx');
    process.exit(1);
  }

  const url = `${API_BASE}/open/cos/image/compress`;
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-App-Key': APP_KEY,
      'X-API-Key': API_KEY,
    },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  if (data.code !== 1000) {
    throw new Error(`API Error: ${data.message || JSON.stringify(data)}`);
  }
  return data.data;
}

async function processOne(input, opts, outputDir) {
  // Build request body
  const body = {};

  // Input source
  if (input.startsWith('http://') || input.startsWith('https://')) {
    body.imageUrl = input;
  } else {
    body.imageBase64 = fileToBase64(input);
  }

  // Apply preset
  if (opts.preset && PRESETS[opts.preset]) {
    const preset = PRESETS[opts.preset];
    body.quality = preset.quality;
    if (preset.format) body.format = preset.format;
  }

  // Override with explicit params
  if (opts.quality) body.quality = parseInt(opts.quality);
  if (opts.format) body.format = opts.format;
  if (opts.width) body.width = parseInt(opts.width);
  if (opts.height) body.height = parseInt(opts.height);
  if (opts.mode) body.mode = opts.mode;

  const result = await compressImage(body);

  // Determine output
  const originalName = input.startsWith('http') ? basename(new URL(input).pathname) : basename(input);
  const outputFormat = body.format || extname(originalName).slice(1) || 'jpg';
  const outputPath = getOutputPath(outputDir, originalName, outputFormat);

  // Save result
  if (result.compressedUrl && !result.base64) {
    // Download from URL
    const imgRes = await fetch(result.compressedUrl);
    const buffer = Buffer.from(await imgRes.arrayBuffer());
    writeFileSync(outputPath, buffer);
  } else if (result.base64) {
    const base64Data = result.base64.replace(/^data:image\/\w+;base64,/, '');
    writeFileSync(outputPath, Buffer.from(base64Data, 'base64'));
  }

  // Print result
  const savings = result.originalSize && result.compressedSize
    ? ((1 - result.compressedSize / result.originalSize) * 100).toFixed(1)
    : '?';
  const formatInfo = outputFormat !== extname(originalName).slice(1) ? ` → ${outputFormat}` : '';
  console.log(`  ${originalName}${formatInfo}: ${formatBytes(result.originalSize)} → ${formatBytes(result.compressedSize)} (-${savings}%)`);
  console.log(`  Saved to: ${outputPath}`);

  return { originalName, outputPath, originalSize: result.originalSize, compressedSize: result.compressedSize };
}

function collectImages(dir, recursive) {
  const images = [];
  const entries = readdirSync(dir);
  for (const entry of entries) {
    const full = join(dir, entry);
    const stat = statSync(full);
    if (stat.isDirectory() && recursive) {
      images.push(...collectImages(full, recursive));
    } else if (stat.isFile() && IMAGE_EXTS.has(extname(entry).toLowerCase())) {
      images.push(full);
    }
  }
  return images;
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    printHelp();
    process.exit(0);
  }

  const opts = parseArgs(args);

  // Validate input
  if (!opts.url && !opts.file && !opts.dir) {
    console.error('Error: specify --url, --file, or --dir');
    process.exit(1);
  }

  const outputDir = getOutputDir(opts.output);
  mkdirSync(outputDir, { recursive: true });

  // Single image via URL
  if (opts.url) {
    console.log('Compressing image from URL...\n');
    await processOne(opts.url, opts, outputDir);
    return;
  }

  // Single local file
  if (opts.file) {
    const filePath = resolve(opts.file);
    if (!existsSync(filePath)) {
      console.error(`Error: file not found: ${filePath}`);
      process.exit(1);
    }
    console.log('Compressing image...\n');
    await processOne(filePath, opts, outputDir);
    return;
  }

  // Batch directory
  if (opts.dir) {
    const dirPath = resolve(opts.dir);
    if (!existsSync(dirPath)) {
      console.error(`Error: directory not found: ${dirPath}`);
      process.exit(1);
    }

    const images = collectImages(dirPath, opts.recursive);
    if (images.length === 0) {
      console.error('No images found in directory');
      process.exit(1);
    }

    console.log(`Found ${images.length} image(s) to compress\n`);

    let totalOriginal = 0;
    let totalCompressed = 0;
    let errors = 0;

    for (let i = 0; i < images.length; i++) {
      const img = images[i];
      console.log(`[${i + 1}/${images.length}] ${basename(img)}`);
      try {
        const result = await processOne(img, opts, outputDir);
        totalOriginal += result.originalSize || 0;
        totalCompressed += result.compressedSize || 0;
      } catch (err) {
        console.error(`  Error: ${err.message}`);
        errors++;
      }
      console.log('');
    }

    // Summary
    console.log('--- Summary ---');
    console.log(`Processed: ${images.length - errors}/${images.length}`);
    if (totalOriginal > 0) {
      const saved = ((1 - totalCompressed / totalOriginal) * 100).toFixed(1);
      console.log(`Total: ${formatBytes(totalOriginal)} → ${formatBytes(totalCompressed)} (-${saved}%)`);
    }
    if (errors > 0) console.log(`Failed: ${errors}`);
    console.log(`Output: ${outputDir}`);
  }
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(1);
});
