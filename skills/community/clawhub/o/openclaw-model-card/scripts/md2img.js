#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const md = require('markdown-it')({
  html: true,
  linkify: true,
  typographer: true
}).use(require('markdown-it-emoji').full);

const inputPath = process.argv[2];
const outputPathArg = process.argv[3] || 'output.png';
const outputPath = path.resolve(outputPathArg);

if (!inputPath) {
  console.log('Usage: node md2img.js <input.md> [output.png]');
  process.exit(1);
}

const wk = spawnSync('wkhtmltoimage', ['--version'], { encoding: 'utf-8' });
if (wk.error || wk.status !== 0) {
  console.error('Error: wkhtmltoimage not found. Please install wkhtmltoimage first.');
  process.exit(2);
}

const content = fs.readFileSync(inputPath, 'utf-8');
const htmlBody = md.render(content);

const fullHtml = `
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    background: #0d1117;
    color: #c9d1d9;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    padding: 30px;
    width: 600px;
    line-height: 1.5;
  }
  table { border-collapse: collapse; width: 100%; margin: 16px 0; }
  th, td { border: 1px solid #30363d; padding: 8px 12px; text-align: left; }
  th { background: #161b22; }
  code { background: #6e768166; padding: 0.2em 0.4em; border-radius: 6px; font-size: 85%; font-family: ui-monospace,SFMono-Regular,SF Mono,Menlo,Consolas,Liberation Mono,monospace; }
  h2 { border-bottom: 1px solid #21262d; padding-bottom: 0.3em; color: #58a6ff; }
  ul { padding-left: 2em; }
  .emoji { height: 1.2em; vertical-align: middle; }
</style>
</head>
<body>${htmlBody}</body>
</html>
`;

fs.mkdirSync(path.dirname(outputPath), { recursive: true });

const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'md2img-'));
const tempHtml = path.join(tempDir, 'input.html');

try {
  fs.writeFileSync(tempHtml, fullHtml, 'utf-8');

  const run = spawnSync(
    'wkhtmltoimage',
    ['--width', '660', '--disable-smart-width', tempHtml, outputPath],
    { encoding: 'utf-8' }
  );

  if (run.status !== 0) {
    const stderr = (run.stderr || '').trim();
    const stdout = (run.stdout || '').trim();
    console.error('Error generating image:');
    if (stderr) console.error(stderr);
    if (stdout) console.error(stdout);
    process.exit(run.status || 3);
  }

  console.log(`Success: ${outputPath}`);
} finally {
  try {
    fs.rmSync(tempDir, { recursive: true, force: true });
  } catch (_) {
    // ignore cleanup failure
  }
}
