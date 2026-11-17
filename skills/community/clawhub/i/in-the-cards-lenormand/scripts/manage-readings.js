/**
 * In the Cards — Reading Manager
 *
 * Manage saved readings: list, find, update index, generate products.
 *
 * Usage:
 *   node manage-readings.js list [--limit N]
 *   node manage-readings.js find <reading_id>
 *   node manage-readings.js latest
 *   node manage-readings.js record-product <reading_id> --type <product_type> --path <output_path>
 */

const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.resolve(process.cwd(), 'output');
const READINGS_DIR = path.join(OUTPUT_DIR, 'readings');
const INDEX_PATH = path.join(READINGS_DIR, 'index.json');

function loadIndex() {
  if (!fs.existsSync(INDEX_PATH)) return [];
  return JSON.parse(fs.readFileSync(INDEX_PATH, 'utf-8'));
}

function saveIndex(index) {
  fs.writeFileSync(INDEX_PATH, JSON.stringify(index, null, 2), 'utf-8');
}

function list(limit) {
  const index = loadIndex();
  const sorted = [...index].sort((a, b) => b.generated_at.localeCompare(a.generated_at));
  const items = limit ? sorted.slice(0, limit) : sorted;

  if (items.length === 0) {
    console.log('No readings found.');
    return;
  }

  console.log(`\n--- Saved Readings (${items.length} of ${index.length}) ---\n`);
  items.forEach((r, i) => {
    const date = r.date || 'unknown';
    const type = r.spread_type || '?';
    const question = r.question || '(daily fortune)';
    const products = (r.products_generated || []).join(', ') || 'none';
    console.log(`  [${i + 1}] ${r.reading_id}`);
    console.log(`      Date: ${date} | Spread: ${type} | Products: ${products}`);
    console.log(`      Q: ${question}`);
    console.log(`      Cards: ${(r.card_names || []).join(' / ')}`);
    console.log();
  });
}

function find(readingId) {
  const readingPath = path.join(READINGS_DIR, `${readingId}.json`);
  if (fs.existsSync(readingPath)) {
    console.log(JSON.stringify(JSON.parse(fs.readFileSync(readingPath, 'utf-8')), null, 2));
  } else {
    console.error(`Reading not found: ${readingId}`);
    process.exit(1);
  }
}

function getLatest() {
  const index = loadIndex();
  if (index.length === 0) {
    console.error('No readings found.');
    process.exit(1);
  }
  const sorted = [...index].sort((a, b) => b.generated_at.localeCompare(a.generated_at));
  const readingId = sorted[0].reading_id;
  const readingPath = path.join(READINGS_DIR, `${readingId}.json`);
  console.log(JSON.stringify(JSON.parse(fs.readFileSync(readingPath, 'utf-8')), null, 2));
}

function recordProduct(readingId, productType, outputPath) {
  const index = loadIndex();
  const entry = index.find(r => r.reading_id === readingId);
  if (!entry) {
    console.error(`Reading not found in index: ${readingId}`);
    process.exit(1);
  }
  if (!entry.products_generated) entry.products_generated = [];
  if (!entry.products_generated.includes(productType)) {
    entry.products_generated.push(productType);
    saveIndex(index);
    console.log(`Recorded ${productType} for ${readingId}`);
  } else {
    console.log(`${productType} already recorded for ${readingId}`);
  }
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'list': {
    const limitIdx = args.indexOf('--limit');
    const limit = limitIdx >= 0 ? parseInt(args[limitIdx + 1]) : null;
    list(limit);
    break;
  }
  case 'find': {
    const readingId = args[1];
    if (!readingId) { console.error('Usage: node manage-readings.js find <reading_id>'); process.exit(1); }
    find(readingId);
    break;
  }
  case 'latest': {
    getLatest();
    break;
  }
  case 'record-product': {
    const readingId = args[1];
    const typeIdx = args.indexOf('--type');
    const productType = typeIdx >= 0 ? args[typeIdx + 1] : null;
    const pathIdx = args.indexOf('--path');
    const outputPath = pathIdx >= 0 ? args[pathIdx + 1] : null;
    if (!readingId || !productType) {
      console.error('Usage: node manage-readings.js record-product <reading_id> --type <product_type> [--path <output_path>]');
      process.exit(1);
    }
    recordProduct(readingId, productType, outputPath);
    break;
  }
  default:
    console.error('Commands: list, find, latest, record-product');
    process.exit(1);
}
