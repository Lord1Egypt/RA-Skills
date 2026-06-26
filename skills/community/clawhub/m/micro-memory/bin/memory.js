#!/usr/bin/env node

// Micro Memory CLI Entry Point
// This file loads the compiled TypeScript from dist/

const path = require('path');
const { execSync } = require('child_process');

const distPath = path.join(__dirname, '..', 'dist', 'index.js');

// Forward all arguments to the compiled script
const args = process.argv.slice(2).map(arg => {
  // Properly escape arguments for Windows
  if (arg.includes(' ') || arg.includes('"')) {
    return `"${arg.replace(/"/g, '\\"')}"`;
  }
  return arg;
}).join(' ');

try {
  execSync(`node "${distPath}" ${args}`, {
    stdio: 'inherit',
    windowsHide: true
  });
} catch (e) {
  // Exit with same code as child process
  process.exit(e.status || 1);
}
