#!/usr/bin/env node

/**
 * Jina.ai Reader - Fetch clean, AI-friendly content from any URL
 * Usage: node jina-reader.mjs "url" [--wait-ms 10000] [--with-images] [--with-links]
 */

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
  console.error('Usage: node jina-reader.mjs "url" [--wait-ms 10000] [--with-images] [--with-links]');
  console.error('');
  console.error('Options:');
  console.error('  --wait-ms N    Wait N milliseconds for JS to render (default: 0)');
  console.error('  --with-images  Include image captions in output');
  console.error('  --with-links   Include all links in output');
  console.error('');
  console.error('Examples:');
  console.error('  node jina-reader.mjs "https://example.com/article"');
  console.error('  node jina-reader.mjs "https://twitter.com/user/status/123" --with-images');
  console.error('  node jina-reader.mjs "https://every.to/article" --wait-ms 5000');
  process.exit(1);
}

const url = args.find(a => !a.startsWith('--'));
const waitMs = args.includes('--wait-ms') ? parseInt(args[args.indexOf('--wait-ms') + 1]) || 0 : 0;
const withImages = args.includes('--with-images');
const withLinks = args.includes('--with-links');

if (!url) {
  console.error('Error: URL is required');
  process.exit(1);
}

// Build Jina Reader URL
let jinaUrl = 'https://r.jina.ai/';
if (waitMs > 0) jinaUrl += `wait:${waitMs}/`;
if (withImages) jinaUrl += 'with-images/';
if (withLinks) jinaUrl += 'with-links/';
jinaUrl += url;

try {
  const response = await fetch(jinaUrl);
  if (!response.ok) {
    console.error(`Error: HTTP ${response.status} ${response.statusText}`);
    process.exit(1);
  }
  const content = await response.text();
  console.log(content);
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exit(1);
}
