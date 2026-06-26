#!/usr/bin/env node
/**
 * Table2Image CLI
 * Usage: node table-cli.mjs --data-file data.json --dark --output table.png
 */

import { readFileSync, existsSync } from 'fs';
import { renderTable, THEMES } from './index.js';

function showHelp() {
  console.log(`
Table2Image - Convert tables to PNG images

Usage:
  node table-cli.mjs [options]

Options:
  --data-file            JSON file with data array (required)
  --columns              Comma-separated column keys
  --headers              Comma-separated header names
  --align                Comma-separated alignments (l,c,r)
  --theme                Theme: discord-light|discord-dark|finance|minimal|sweet-pink|deep-sea|wisteria|pond-blue|camellia
  --dark                 Use discord-dark theme (shortcut)
  --custom-theme         JSON string with custom theme colors
  --custom-theme-file    JSON file with custom theme colors
  --primary-color        Primary accent color (hex)
  --secondary-color      Secondary/base background color (hex)
  --title                Table title
  --max-width            Maximum table width (default: 800)
  --output               Output file path (default: table.png)
  --help                 Show this help

Custom Theme JSON format:
  {
    "background": "#1a1a1d",
    "headerBg": "#e6397c",
    "headerText": "#ffffff",
    "rowBg": "#1a1a1d",
    "rowAltBg": "#2a2a2d",
    "text": "#e6397c",
    "border": "#e6397c"
  }

Or use primary + secondary shorthand:
  node table-cli.mjs --data-file data.json --primary-color "#E6397C" --secondary-color "#1A1A1D" --output out.png

Example:
  node table-cli.mjs --data-file data.json --dark --title "My Table" --output out.png
  node table-cli.mjs --data-file data.json --theme sweet-pink --output out.png
  node table-cli.mjs --data-file data.json --custom-theme '{"background":"#000","headerBg":"#ff0","headerText":"#000","rowBg":"#000","rowAltBg":"#111","text":"#ff0","border":"#ff0"}' --output out.png
  node table-cli.mjs --data-file data.json --primary-color "#E6397C" --secondary-color "#1A1A1D" --output out.png
`);
}

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    dataFile: '',
    columns: '',
    headers: '',
    align: '',
    theme: '',
    customTheme: '',
    customThemeFile: '',
    primaryColor: '',
    secondaryColor: '',
    title: '',
    maxWidth: 800,
    output: 'table.png'
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const next = args[i + 1];

    switch (arg) {
      case '--data-file': options.dataFile = next; i++; break;
      case '--columns': options.columns = next; i++; break;
      case '--headers': options.headers = next; i++; break;
      case '--align': options.align = next; i++; break;
      case '--theme': options.theme = next; i++; break;
      case '--dark': options.theme = 'discord-dark'; break;
      case '--custom-theme': options.customTheme = next; i++; break;
      case '--custom-theme-file': options.customThemeFile = next; i++; break;
      case '--primary-color': options.primaryColor = next; i++; break;
      case '--secondary-color': options.secondaryColor = next; i++; break;
      case '--title': options.title = next; i++; break;
      case '--max-width': options.maxWidth = parseInt(next); i++; break;
      case '--output': options.output = next; i++; break;
      case '--help': showHelp(); process.exit(0); break;
    }
  }

  return options;
}

function resolveTheme(opts) {
  if (opts.customThemeFile && existsSync(opts.customThemeFile)) {
    try {
      const content = readFileSync(opts.customThemeFile, 'utf8');
      return JSON.parse(content);
    } catch (e) {
      console.error('Error: Invalid custom theme file JSON');
      process.exit(1);
    }
  }

  if (opts.customTheme) {
    try {
      return JSON.parse(opts.customTheme);
    } catch (e) {
      console.error('Error: Invalid custom theme JSON string');
      process.exit(1);
    }
  }

  if (opts.primaryColor && opts.secondaryColor) {
    return {
      primary: opts.primaryColor,
      secondary: opts.secondaryColor
    };
  }

  if (opts.theme) {
    if (!THEMES[opts.theme]) {
      console.warn(`Warning: Unknown theme "${opts.theme}", falling back to discord-light`);
    }
    return opts.theme;
  }

  return 'discord-light';
}

async function main() {
  const opts = parseArgs();

  if (!opts.dataFile || !existsSync(opts.dataFile)) {
    console.error('Error: --data-file is required and must exist');
    showHelp();
    process.exit(1);
  }

  try {
    const data = JSON.parse(readFileSync(opts.dataFile, 'utf8'));
    
    if (!Array.isArray(data)) {
      console.error('Error: Data must be an array');
      process.exit(1);
    }

    // Build column config
    const keys = opts.columns ? opts.columns.split(',').map(s => s.trim()) : Object.keys(data[0] || {});
    const headers = opts.headers ? opts.headers.split(',').map(s => s.trim()) : keys;
    const aligns = opts.align ? opts.align.split(',').map(s => s.trim()) : [];

    const columns = keys.map((key, i) => ({
      key,
      header: headers[i] || key,
      align: aligns[i] === 'r' ? 'right' : aligns[i] === 'c' ? 'center' : 'left'
    }));

    const theme = resolveTheme(opts);

    console.log(`Rendering table with ${data.length} rows...`);
    console.log(`Theme: ${typeof theme === 'string' ? theme : '(custom)'}`);

    const result = await renderTable({
      data,
      columns,
      title: opts.title,
      theme,
      maxWidth: opts.maxWidth
    });

    const { writeFileSync } = await import('fs');
    writeFileSync(opts.output, result.buffer);

    console.log(`✅ Table saved to ${opts.output}`);
    console.log(`   Size: ${result.width}x${result.height}px`);
    console.log(`   Format: ${result.format}`);

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
