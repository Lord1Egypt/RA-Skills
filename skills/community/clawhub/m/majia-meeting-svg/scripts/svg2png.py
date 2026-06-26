#!/usr/bin/env python3
"""SVG → PNG converter for meeting minutes cards.

Uses headless Chrome (via Puppeteer) for accurate CJK font rendering.
Falls back to cairosvg if Node.js is unavailable.

Usage:
    python3 scripts/svg2png.py input.svg              # → input.png (2x)
    python3 scripts/svg2png.py input.svg output.png    # explicit output path
    python3 scripts/svg2png.py input.svg --scale 3     # 3x resolution
"""
import subprocess, sys, os, re, tempfile, shutil

_PUPPETEER_SCRIPT = r"""
import puppeteer from 'puppeteer';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const [,, svgPath, pngPath, scaleStr] = process.argv;
const scale = parseInt(scaleStr) || 2;
const svgContent = readFileSync(resolve(svgPath), 'utf-8');

const m = svgContent.match(/viewBox\s*=\s*"([^"]+)"/);
if (!m) { console.error('No viewBox'); process.exit(1); }
const parts = m[1].split(/\s+/).map(Number);
const rW = Math.round(parts[2] * scale);
const rH = Math.round(parts[3] * scale);

const cleaned = svgContent
  .replace(/width="[^"]*"/, `width="${rW}"`)
  .replace(/style="[^"]*max-width[^"]*"/, '');

const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  *{margin:0;padding:0}body{width:${rW}px}svg{display:block;width:${rW}px;height:${rH}px}
</style></head><body>${cleaned}</body></html>`;

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: rW, height: Math.min(rH, 16384), deviceScaleFactor: 1 });
await page.setContent(html, { waitUntil: 'networkidle0' });
await page.screenshot({ path: resolve(pngPath), fullPage: true });
await browser.close();
"""

def convert_puppeteer(svg_path, png_path, scale):
    tmp = tempfile.NamedTemporaryFile(suffix='.mjs', mode='w', delete=False, dir='/tmp')
    tmp.write(_PUPPETEER_SCRIPT)
    tmp.close()
    try:
        subprocess.run(
            ['node', tmp.name, os.path.abspath(svg_path), os.path.abspath(png_path), str(scale)],
            check=True, timeout=60,
            env={**os.environ, 'NODE_PATH': '/tmp/node_modules'}
        )
    finally:
        os.unlink(tmp.name)

    _, vbW, vbH = _parse_viewbox(svg_path)
    print(f"✔ {png_path}  ({vbW*scale}×{vbH*scale}px, scale={scale})")
    return png_path

def _parse_viewbox(svg_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'viewBox\s*=\s*"([^"]+)"', content)
    if not m:
        raise ValueError("No viewBox found in SVG")
    parts = m.group(1).split()
    return content, int(float(parts[2])), int(float(parts[3]))

def convert_cairosvg(svg_path, png_path, scale):
    try:
        import cairosvg
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install",
                               "--break-system-packages", "-q", "cairosvg"])
        import cairosvg
    cairosvg.svg2png(url=svg_path, write_to=png_path, scale=scale)
    print(f"✔ {png_path}  (cairosvg fallback, scale={scale})")
    print("⚠  cairosvg may render CJK fonts as boxes — install Node.js for Puppeteer rendering")
    return png_path

def convert(svg_path, png_path=None, scale=2):
    if png_path is None:
        png_path = os.path.splitext(svg_path)[0] + ".png"
    if shutil.which('node'):
        try:
            return convert_puppeteer(svg_path, png_path, scale)
        except Exception as e:
            print(f"⚠  Puppeteer failed ({e}), falling back to cairosvg")
    return convert_cairosvg(svg_path, png_path, scale)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("svg")
    p.add_argument("png", nargs="?")
    p.add_argument("--scale", type=int, default=2)
    a = p.parse_args()
    convert(a.svg, a.png, a.scale)
