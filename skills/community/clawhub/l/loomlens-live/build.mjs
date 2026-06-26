#!/usr/bin/env node
/**
 * LoomLens Live — Build Script
 *
 * Usage:
 *   node build.mjs              # build everything
 *   node build.mjs sidebar     # build sidebar only
 *
 * Output:
 *   dist/loomlens-clusters.js  — standalone clusters module
 *   dist/loomlens-engine.js    — standalone engine module (no TS imports)
 *   dist/loomlens-sidebar.html  — self-contained sidebar (all-in-one)
 *
 * The sidebar is the canonical deploy artifact — it includes all logic inline.
 */

import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DIST = resolve(__dirname, 'dist');

mkdirSync(DIST, { recursive: true });

// ─── Step 1: Build loomlens-clusters.js (standalone browser global) ─────────
function buildClusters() {
  let js = readFileSync(resolve(__dirname, 'loomlens-clusters.js'), 'utf8');
  // Ensure browser global is set
  if (!js.includes('window.LoomLensClusters')) {
    js += '\nif (typeof window !== "undefined") { window.LoomLensClusters = window._LL; }\n';
  }
  writeFileSync(resolve(DIST, 'loomlens-clusters.js'), js);
  console.log('✓ dist/loomlens-clusters.js');
}

// ─── Step 2: Build loomlens-engine.js (standalone, inlines cluster deps) ─────
// The engine imports from clusters.js. For standalone use, we inline the
// clusters directly into the engine so it has no external dependencies.
function buildEngine() {
  const clusters = readFileSync(resolve(__dirname, 'loomlens-clusters.js'), 'utf8');
  let engine = readFileSync(resolve(__dirname, 'loomlens-engine.ts'), 'utf8');

  // Remove TypeScript import
  engine = engine.replace(
    /import \{[\s\S]*?\} from '\.\/loomlens-clusters\.js';/,
    ''
  );

  // Inject clusters as a plain JS object before the engine code
  const clustersData = clusters
    .replace(/^export /gm, '')           // strip ES module exports
    .replace(/^import .*$/gm, '')        // strip any top-level imports
    .replace(/if \(typeof window[\s\S]*?\}\);/, '')  // strip browser global block
    .trim();

  engine = `// LoomLens Live — Engine (built)\n${clustersData}\n\n${engine}`;

  writeFileSync(resolve(DIST, 'loomlens-engine.js'), engine);
  console.log('✓ dist/loomlens-engine.js');
}

// ─── Step 3: Build loomlens-sidebar.html (all-in-one deploy artifact) ───────
// Replaces script references with inline code, creating a single-file deploy.
function buildSidebar() {
  let html = readFileSync(resolve(__dirname, 'loomlens-sidebar.html'), 'utf8');
  const clusters = readFileSync(resolve(__dirname, 'loomlens-clusters.js'), 'utf8')
    .replace(/^export /gm, '')
    .replace(/^import .*$/gm, '')
    .replace(/if \(typeof window[\s\S]*?\}\);/, '')
    .trim();

  // Remove the inline clusters/engine block from the sidebar and inject built version
  // The sidebar has its own inline version — for the build, we keep it inline as-is
  // since it's already self-contained. The dist version is identical to source.
  writeFileSync(resolve(DIST, 'loomlens-sidebar.html'), html);
  console.log('✓ dist/loomlens-sidebar.html');
}

// ─── CLI ────────────────────────────────────────────────────────────────────
const cmd = process.argv[2] || 'all';

if (cmd === 'all') {
  buildClusters();
  buildEngine();
  buildSidebar();
} else if (cmd === 'sidebar') {
  buildSidebar();
} else if (cmd === 'clusters') {
  buildClusters();
} else if (cmd === 'engine') {
  buildEngine();
} else {
  console.error(`Unknown target: ${cmd}`);
  console.error('Usage: node build.mjs [all|sidebar|clusters|engine]');
  process.exit(1);
}

console.log(`\nBuild complete → ${DIST}`);
