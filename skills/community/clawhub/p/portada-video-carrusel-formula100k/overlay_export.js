#!/usr/bin/env node
/**
 * Exporta UN elemento .slide de un HTML a PNG con FONDO TRANSPARENTE.
 * Pensado para el título de portada que se compone sobre un video.
 *
 * Uso:
 *   node overlay_export.js <ruta-al-html> [--out salida.png] [--width 1080] [--height 1350] [--scale 2]
 *
 * El HTML debe tener html,body{background:transparent} y un .slide transparente.
 */
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
if (!args[0] || args[0].startsWith('--')) {
  console.error('Uso: node overlay_export.js <html> [--out png] [--width N] [--height N] [--scale N]');
  process.exit(1);
}
const HTML = path.resolve(args[0]);
function arg(name, def){ const i = args.indexOf(name); return i>-1 && args[i+1] ? args[i+1] : def; }
const W = Number(arg('--width', 1080));
const H = Number(arg('--height', 1350));
const SCALE = Number(arg('--scale', 2));
const OUT = path.resolve(arg('--out', path.join(path.dirname(HTML), 'title-overlay.png')));

const CHROME = [
  process.env.CHROME_PATH,
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/usr/bin/google-chrome',
  '/usr/bin/google-chrome-stable',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
].find(p => fs.existsSync(p));
if (!CHROME) { console.error('No se encontró Chromium. Define CHROME_PATH con la ruta del Chromium del servidor.'); process.exit(1); }

(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage'],
    defaultViewport: { width: W, height: H, deviceScaleFactor: SCALE } });
  const p = await b.newPage();
  await p.goto('file://' + HTML, { waitUntil: 'networkidle0' });
  await p.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 1200));
  const el = await p.$('.slide');
  if (!el) { console.error('No se encontró .slide en el HTML'); await b.close(); process.exit(1); }
  await el.screenshot({ path: OUT, omitBackground: true });   // <- transparencia
  await b.close();
  console.log('✓ ' + OUT + ' (transparente)');
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
