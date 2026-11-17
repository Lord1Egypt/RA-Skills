#!/usr/bin/env node
/**
 * scripts/export.mjs —— 按期刊规格导出 PNG / PDF / TIFF（本地跑、不花钱）
 *
 * 对外接口（BRIEF 5.3 冻结）：
 *   detectRasterizer() -> { name:'chrome'|'magick'|'none', path, version }
 *   exportFigure(workDir, opts) -> {
 *     ok, files:[{ path, format, widthPx, heightPx, dpi, bytes, via, degraded?, note? }],
 *     skipped:[{ format, reason, hint }], rasterizer, warnings:[]
 *   }
 *
 * 实测结论（2026-11-03，本机 macOS + Chrome 沙箱 + ImageMagick）：
 *   1. Chrome headless 在本机沙箱里必须加 --no-sandbox，还要给 --user-data-dir=<tmp> +
 *      --disable-crash-reporter --disable-breakpad --crash-dumps-dir=<tmp>，否则启动即崩。
 *      所以策略是：先按默认参数试，失败自动重试一次兼容模式，并在 stderr 说明。
 *   2. 本机 ImageMagick 没有 freetype、没有 ghostscript：magick 从 SVG 出 PNG 会丢全部文字，
 *      出 PDF 直接失败。它只能当「没有 Chrome 时的最后兜底」，而且必须如实写 degraded。
 *   3. 像素精确的 PNG 不能靠 --force-device-scale-factor 猜 DPI。做法是生成一个 HTML wrapper：
 *      <style>@page{size:89mm 60mm;margin:0}</style> + <svg width="2102px" height="1417px">，
 *      再 --window-size=2102,1417 --force-device-scale-factor=1 --screenshot=out.png。
 *   4. PDF 用同一个 wrapper 走 --no-pdf-header-footer --print-to-pdf，MediaBox 就是物理尺寸，
 *      生成后读 /MediaBox 校验（矢量文字保留）。
 *   5. TIFF Chrome 出不了，用 magick 从 PNG 转（不经过 SVG，所以没有丢字问题），LZW 压缩。
 *   6. rsvg-convert / cairosvg / gs 本机都没有；qlmanage 走沙箱会静默失败，不依赖。
 */

import { spawnSync } from 'node:child_process'
import {
  existsSync, mkdirSync, readFileSync, writeFileSync, statSync, rmSync, mkdtempSync, readdirSync
} from 'node:fs'
import { homedir, tmpdir } from 'node:os'
import { basename, dirname, isAbsolute, join, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const MM_PER_IN = 25.4
const PX_PER_IN = 96
const PT_PER_IN = 72
const IS_WIN = process.platform === 'win32'
const IS_MAC = process.platform === 'darwin'

export const DEFAULTS = {
  formats: ['png', 'pdf', 'tif'],
  timeoutMs: 120000,
  dpi: 300
}

/* ==========================================================================
 * 一、找工具
 * ========================================================================== */

/** 在 PATH 里找一个可执行文件（不调 which，跨平台） */
function findInPath(names) {
  const exts = IS_WIN ? (process.env.PATHEXT || '.EXE;.CMD;.BAT').split(';').filter(Boolean) : ['']
  const dirs = (process.env.PATH || '').split(IS_WIN ? ';' : ':').filter(Boolean)
  for (const name of names) {
    if (isAbsolute(name) && existsSync(name)) return name
    for (const dir of dirs) {
      for (const ext of exts) {
        const p = join(dir, name.endsWith(ext.toLowerCase()) || name.endsWith(ext) ? name : name + ext)
        try { if (existsSync(p) && statSync(p).isFile()) return p } catch { /* ignore */ }
      }
    }
  }
  return ''
}

/** Chrome / Chromium / Edge 的所有候选路径（macOS / Linux / Windows 全覆盖） */
function chromeCandidates() {
  const list = []
  if (process.env.CHROME_PATH) list.push(process.env.CHROME_PATH)
  if (process.env.CHROME_BIN) list.push(process.env.CHROME_BIN)

  if (IS_MAC) {
    const apps = [
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
      '/Applications/Chromium.app/Contents/MacOS/Chromium',
      '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
      '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    ]
    list.push(...apps)
    for (const a of apps) list.push(join(homedir(), a))
  } else if (IS_WIN) {
    const pf = process.env.ProgramFiles || 'C:\\Program Files'
    const pf86 = process.env['ProgramFiles(x86)'] || 'C:\\Program Files (x86)'
    const local = process.env.LOCALAPPDATA || join(homedir(), 'AppData', 'Local')
    list.push(
      join(pf, 'Google', 'Chrome', 'Application', 'chrome.exe'),
      join(pf86, 'Google', 'Chrome', 'Application', 'chrome.exe'),
      join(local, 'Google', 'Chrome', 'Application', 'chrome.exe'),
      join(pf, 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
      join(pf86, 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
      join(pf, 'Chromium', 'Application', 'chrome.exe')
    )
  } else {
    // Linux 等：按 PATH 找
    list.push(
      findInPath(['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser',
        'microsoft-edge', 'microsoft-edge-stable', 'brave-browser']),
      '/usr/bin/google-chrome',
      '/usr/bin/chromium',
      '/usr/bin/chromium-browser',
      '/snap/bin/chromium'
    )
  }
  return [...new Set(list.filter(Boolean))]
}

function run(cmd, args, opts = {}) {
  const started = Date.now()
  let res
  try {
    res = spawnSync(cmd, args, {
      encoding: 'utf8',
      timeout: opts.timeoutMs ?? DEFAULTS.timeoutMs,
      maxBuffer: 8 * 1024 * 1024,
      windowsHide: true,
      cwd: opts.cwd,
      env: { ...process.env, ...(opts.env || {}) }
    })
  } catch (e) {
    return { ok: false, status: -1, stdout: '', stderr: String(e && e.message || e), ms: Date.now() - started, error: e }
  }
  const out = `${res.stdout || ''}${res.stderr || ''}`.trim()
  const timedOut = res.error && res.error.code === 'ETIMEDOUT'
  return {
    ok: !res.error && res.status === 0,
    status: res.status,
    signal: res.signal,
    stdout: res.stdout || '',
    stderr: res.stderr || '',
    output: out,
    timedOut: Boolean(timedOut),
    ms: Date.now() - started,
    error: res.error || null
  }
}

let chromeProbe = null
/** 探测 Chrome 是否真的能跑（--version），结果缓存 */
function probeChrome(path) {
  if (chromeProbe && chromeProbe.path === path) return chromeProbe
  const r = run(path, ['--version'], { timeoutMs: 20000 })
  const version = (r.stdout || r.stderr || r.output || '').split('\n')[0].trim()
  chromeProbe = { path, ok: r.ok, version: version || 'unknown' }
  return chromeProbe
}

let magickProbe = null
/**
 * 探测 ImageMagick。注意：本机 magick 没有 freetype/ghostscript，能力有限，这里只判档。
 * deep=false 只跑 -version（毫秒级）；deep=true 才多跑 -list font（判断有没有字体引擎），
 * 因为 -list font 在 macOS 上要好几秒，不能每次导出都跑。
 */
function probeMagick(deep = false) {
  if (magickProbe) return magickProbe
  magickProbe = { name: 'none', path: '', version: '', hasFonts: false, formats: [] }
  const magickPath = findInPath(['magick'])
  if (magickPath) {
    const r = run(magickPath, ['-version'], { timeoutMs: 20000 })
    const version = (r.stdout || r.output || '').split('\n')[0].trim()
    if (r.ok && /ImageMagick/i.test(version + r.output)) {
      magickProbe = { name: 'magick', path: magickPath, version, hasFonts: false, formats: [] }
    }
  }
  // 没有 magick 才试 convert（Windows 自带 convert.exe 是磁盘工具，必须验明正身）
  if (magickProbe.name === 'none') {
    const convertPath = findInPath(['convert'])
    if (convertPath) {
      const r = run(convertPath, ['-version'], { timeoutMs: 20000 })
      const version = (r.stdout || r.output || '').split('\n')[0].trim()
      if (r.ok && /ImageMagick/i.test(version + r.output)) {
        magickProbe = { name: 'magick', path: convertPath, version: `convert: ${version}`, hasFonts: false, formats: [] }
      }
    }
  }
  if (magickProbe.name === 'magick' && deep && magickProbe.hasFonts === false && !magickProbe.probedFonts) {
    magickProbe.probedFonts = true
    // 没有 freetype 的 magick 读 SVG 会丢字，先记下来，导出时如实写 degraded
    const f = run(magickProbe.path, ['-list', 'font'], { timeoutMs: 20000 })
    const fonts = (f.stdout || '').match(/Font:/g)
    magickProbe.hasFonts = Boolean(fonts && fonts.length)
    const fm = run(magickProbe.path, ['-list', 'format'], { timeoutMs: 20000 })
    magickProbe.formats = (fm.stdout || '').split('\n')
      .map((l) => l.trim().split(/\s+/)[0])
      .filter((l) => l && /^[A-Z0-9]+$/i.test(l))
  }
  return magickProbe
}

/**
 * 找一个能把 SVG 转成位图的工具。
 * @returns {{name:'chrome'|'magick'|'none', path:string, version:string, ...}}
 */
export function detectRasterizer() {
  for (const cand of chromeCandidates()) {
    if (!cand) continue
    if (!existsSync(cand)) continue
    const p = probeChrome(cand)
    if (p.ok) {
      return {
        name: 'chrome',
        path: cand,
        version: p.version,
        note: 'Chrome headless 可以做到像素精确（PNG/TIFF/PDF 都行）'
      }
    }
  }
  const m = probeMagick()
  if (m.name === 'magick') {
    return {
      name: 'magick',
      path: m.path,
      version: m.version,
      hasFonts: m.hasFonts,
      note: m.hasFonts
        ? 'ImageMagick 兜底（精度不如 Chrome，但能用）'
        : 'ImageMagick 兜底，但本机 ImageMagick 没有字体渲染能力 —— 从 SVG 出图会丢文字，只能从 PNG 转格式'
    }
  }
  return {
    name: 'none',
    path: '',
    version: '',
    note: '本机没找到 Chrome 或 ImageMagick。先直接用 SVG/PDF 交稿（矢量反而更受期刊欢迎），或装 Chrome 再导出 PNG/TIFF。'
  }
}

/* ==========================================================================
 * 二、Chrome 执行（默认参数失败 → 自动兼容模式重试）
 * ========================================================================== */

let chromeCompatMode = false // 一旦兼容模式成功，后续都直接用它，省一次失败

function baseChromeArgs(userDataDir) {
  return [
    '--headless=new',
    '--disable-gpu',
    '--hide-scrollbars',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-extensions',
    '--disable-background-networking',
    '--disable-component-update',
    '--virtual-time-budget=2500',
    `--user-data-dir=${userDataDir}`
  ]
}

function compatChromeArgs(crashDir) {
  return [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-setuid-sandbox',
    '--disable-crash-reporter',
    '--disable-breakpad',
    `--crash-dumps-dir=${crashDir}`
  ]
}

/**
 * 跑一次 Chrome；失败且还没进兼容模式时，自动带 --no-sandbox 那套重试一次。
 * @returns {{ ok, output, mode:'default'|'compat', attempts:[...], ms }}
 */
function runChrome(chromePath, args, { userDataDir, crashDir, timeoutMs, label }) {
  const attempts = []
  let attemptNo = 0
  const tryOnce = (extra, mode) => {
    // 每次尝试都开一个全新 profile：上一次失败会留下 SingletonLock，
    // 复用同一个目录重试会以「profile in use」再挂一次（本机实测）。
    const profile = join(userDataDir, `a${++attemptNo}`)
    try { mkdirSync(profile, { recursive: true }) } catch { /* ignore */ }
    const full = [...baseChromeArgs(profile), ...extra, ...args]
    const r = run(chromePath, full, { timeoutMs })
    attempts.push({ mode, ok: r.ok, status: r.status, ms: r.ms, tail: r.output.slice(-400) })
    return r
  }

  if (chromeCompatMode) {
    const r = tryOnce(compatChromeArgs(crashDir), 'compat')
    return { ok: r.ok, output: r.output, mode: 'compat', attempts, ms: r.ms, timedOut: r.timedOut }
  }

  let r = tryOnce([], 'default')
  if (r.ok) return { ok: true, output: r.output, mode: 'default', attempts, ms: r.ms }

  // 默认参数失败 → 兼容模式重试
  const r2 = tryOnce(compatChromeArgs(crashDir), 'compat')
  if (r2.ok) {
    chromeCompatMode = true
    process.stderr.write(`[export] 已用兼容模式启动 Chrome（--no-sandbox 那套）${label ? ` · ${label}` : ''}\n`)
    return { ok: true, output: r2.output, mode: 'compat', attempts, ms: r.ms + r2.ms }
  }
  return {
    ok: false,
    output: `${r.output}\n${r2.output}`.trim(),
    mode: 'compat',
    attempts,
    ms: r.ms + r2.ms,
    timedOut: r.timedOut || r2.timedOut,
    error: r.error || r2.error
  }
}

/* ==========================================================================
 * 三、尺寸换算 & HTML wrapper
 * ========================================================================== */

const round = (n, d = 1) => Number(Number(n).toFixed(d))
const mmToPx = (mm, dpi) => Math.max(1, Math.round((mm / MM_PER_IN) * dpi))
const mmToPt = (mm) => (mm / MM_PER_IN) * PT_PER_IN

/** 读 SVG 根元素上的物理尺寸（mm）与 viewBox */
function readSvgSize(svgText) {
  const m = svgText.match(/<svg\b[^>]*>/i)
  if (!m) return null
  const tag = m[0]
  const attr = (name) => {
    const re = new RegExp(`\\s${name}\\s*=\\s*("([^"]*)"|'([^']*)')`, 'i')
    const r = tag.match(re)
    return r ? (r[2] !== undefined ? r[2] : r[3]) : null
  }
  const parseLen = (raw) => {
    if (!raw) return null
    const mm = String(raw).trim().match(/^(-?[\d.]+)\s*([a-z%]*)$/i)
    if (!mm) return null
    const v = Number(mm[1])
    const u = (mm[2] || '').toLowerCase()
    if (u === 'mm') return v
    if (u === 'cm') return v * 10
    if (u === 'in') return v * MM_PER_IN
    if (u === 'pt') return (v * MM_PER_IN) / PT_PER_IN
    if (u === 'px' || u === '') return (v * MM_PER_IN) / PX_PER_IN
    return null
  }
  let widthMm = parseLen(attr('width'))
  let heightMm = parseLen(attr('height'))
  let vb = null
  const vbRaw = attr('viewBox')
  if (vbRaw) {
    const n = (vbRaw.match(/-?[\d.]+(?:e[-+]?\d+)?/gi) || []).map(Number)
    if (n.length >= 4) vb = { x: n[0], y: n[1], w: n[2], h: n[3] }
  }
  if ((!widthMm || !heightMm) && vb) {
    widthMm = widthMm || (vb.w * MM_PER_IN) / PX_PER_IN
    heightMm = heightMm || (vb.h * MM_PER_IN) / PX_PER_IN
  }
  return { widthMm, heightMm, viewBox: vb, rootTag: tag }
}

/**
 * 把 SVG 根标签的 width/height 换成指定尺寸（"2102px" 或 "89mm"），并补齐 viewBox。
 * 截图用 px（窗口多大图就多大），打印用 mm（页面多大图就多大，不然会分页）。
 */
function inlineSvgWithSize(svgText, wVal, hVal) {
  const info = readSvgSize(svgText)
  if (!info) return svgText
  let body = svgText
    .replace(/<\?xml[^>]*\?>/gi, '')
    .replace(/<!DOCTYPE[^>]*>/gi, '')
    .trim()

  const rootMatch = body.match(/<svg\b[^>]*>/i)
  if (!rootMatch) return body
  let tag = rootMatch[0]
  tag = tag
    .replace(/\swidth\s*=\s*("[^"]*"|'[^']*')/i, '')
    .replace(/\sheight\s*=\s*("[^"]*"|'[^']*')/i, '')
  if (!/\sviewBox\s*=/i.test(tag) && info.viewBox) {
    tag = tag.replace(/^<svg/i, `<svg viewBox="${info.viewBox.x} ${info.viewBox.y} ${info.viewBox.w} ${info.viewBox.h}"`)
  } else if (!/\sviewBox\s*=/i.test(tag) && info.widthMm && info.heightMm) {
    const vw = (info.widthMm * PX_PER_IN) / MM_PER_IN
    const vh = (info.heightMm * PX_PER_IN) / MM_PER_IN
    tag = tag.replace(/^<svg/i, `<svg viewBox="0 0 ${vh > 0 ? vw.toFixed(3) : 1} ${vh > 0 ? vh.toFixed(3) : 1}"`)
  }
  tag = tag.replace(/^<svg/i, `<svg width="${wVal}" height="${hVal}" preserveAspectRatio="xMinYMin meet"`)
  return body.replace(rootMatch[0], tag)
}

function htmlWrapper(svgInline, widthMm, heightMm) {
  return `<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>paper-figure</title>
<style>
  @page { size: ${round(widthMm, 2)}mm ${round(heightMm, 2)}mm; margin: 0; }
  html, body { margin: 0; padding: 0; background: #ffffff; }
  svg { display: block; }
</style></head>
<body>
${svgInline}
</body></html>`
}

/* ==========================================================================
 * 四、产物校验（PNG 像素 / PDF MediaBox）
 * ========================================================================== */

function pngDims(path) {
  try {
    const fd = readFileSync(path)
    if (fd.length < 24) return null
    if (fd[0] !== 0x89 || fd[1] !== 0x50 || fd[2] !== 0x4e || fd[3] !== 0x47) return null
    return { w: fd.readUInt32BE(16), h: fd.readUInt32BE(20), bytes: fd.length }
  } catch { return null }
}

/** 读 PDF 的 MediaBox（pt）与页数。读不出来返回 null */
function pdfInfo(path) {
  try {
    const buf = readFileSync(path)
    const text = buf.toString('latin1')
    let box = null
    const m = text.match(/\/MediaBox\s*\[\s*([-\d.\s]+)\]/)
    if (m) {
      const n = m[1].trim().split(/\s+/).map(Number)
      if (n.length >= 4 && n.every(Number.isFinite)) box = { w: n[2] - n[0], h: n[3] - n[1] }
    }
    // 页数：数 /Type /Page 对象（不能取 /Count 的 max —— 书签大纲里也有 /Count）
    const pageObjs = [...text.matchAll(/\/Type\s*\/Page(?![s\w])/g)].length
    const pages = pageObjs > 0 ? pageObjs : null
    return { box, pages, bytes: buf.length }
  } catch { return null }
}

/* ==========================================================================
 * 五、各种格式的导出实现
 * ========================================================================== */

/** Chrome 截图为精确像素 PNG */
function chromeScreenshot(chrome, { htmlPath, outPath, wPx, hPx, timeoutMs }) {
  return runChrome(chrome.path, [
    `--window-size=${wPx},${hPx}`,
    '--force-device-scale-factor=1',
    `--screenshot=${outPath}`,
    pathToFileURL(htmlPath).href
  ], { userDataDir: chrome.userDataDir, crashDir: chrome.crashDir, timeoutMs, label: 'screenshot' })
}

/** Chrome 打印 PDF（保留矢量文字） */
function chromePdf(chrome, { htmlPath, outPath, timeoutMs }) {
  return runChrome(chrome.path, [
    `--print-to-pdf=${outPath}`,
    '--no-pdf-header-footer',
    '--print-to-pdf-no-header',
    '--no-margins',
    pathToFileURL(htmlPath).href
  ], { userDataDir: chrome.userDataDir, crashDir: chrome.crashDir, timeoutMs, label: 'print-to-pdf' })
}

function magickConvert(magick, args, timeoutMs) {
  const r = run(magick.path, args, { timeoutMs })
  return r
}

/* ==========================================================================
 * 六、主函数
 * ========================================================================== */

function absDir(d) {
  try { return resolve(String(d || process.cwd())) } catch { return String(d) }
}

function readJsonSafe(p) {
  try { return existsSync(p) ? JSON.parse(readFileSync(p, 'utf8')) : null } catch { return null }
}

function listFiles(dir) {
  try { return readdirSync(dir) } catch { return [] }
}

/**
 * 按期刊规格导出。
 * @param {string} workDir 工作区
 * @param {object} opts
 *   - formats: ['png','pdf','tif']（默认全导）
 *   - dpi: 数字（默认取 figure.json.dpi，再不行 300）
 *   - svgPath / name: 指定 SVG 或图名
 *   - timeoutMs、keepTemp、quiet
 */
export async function exportFigure(workDir, opts = {}) {
  const wd = absDir(workDir)
  const outDir = join(wd, 'out')
  const spec = readJsonSafe(join(wd, 'figure.json')) || {}
  // 命名：显式 --name 优先；否则用被导出的那张 SVG 的文件名（render 出 <name>-diagram.svg、
  // chart 出 <name>-chart.svg），这样结构图和数据图不会互相覆盖（Lead 联调发现的问题）。
  const nameOpt = opts.name ? String(opts.name) : ''
  const dpi = Number(opts.dpi || spec.dpi || DEFAULTS.dpi)
  const formats = normalizeFormats(opts.formats)
  const timeoutMs = Number(opts.timeoutMs || DEFAULTS.timeoutMs)

  const result = {
    ok: false,
    files: [],
    skipped: [],
    warnings: [],
    rasterizer: null,
    dpi,
    formats
  }

  const rasterizer = detectRasterizer()
  result.rasterizer = { name: rasterizer.name, path: rasterizer.path, version: rasterizer.version, note: rasterizer.note }

  /* --- 找 SVG --- */
  let svgPath = null
  if (opts.svgPath) {
    const p = isAbsolute(opts.svgPath) ? opts.svgPath : resolve(wd, opts.svgPath)
    if (existsSync(p)) svgPath = p
  } else {
    const cands = []
    if (nameOpt) cands.push(join(outDir, `${nameOpt}.svg`))
    if (spec.name) {
      cands.push(join(outDir, `${spec.name}-diagram.svg`))
      cands.push(join(outDir, `${spec.name}-chart.svg`))
      cands.push(join(outDir, `${spec.name}.svg`))
    }
    svgPath = cands.find((p) => existsSync(p)) || null
    // 有多个候选（结构图 + 数据图都在）又没指定 --svg 时，明确报错让人选，别猜。
    const existing = cands.filter((p) => existsSync(p))
    if (!svgPath || existing.length > 1) {
      const svgs = listFiles(outDir).filter((f) => f.toLowerCase().endsWith('.svg'))
      if (existing.length <= 1 && svgs.length === 1) svgPath = join(outDir, svgs[0])
      else if (existing.length > 1) {
        result.skipped.push({
          format: formats.join(','),
          reason: `out/ 里有不止一张图：${existing.map((p) => basename(p)).join('、')}。不替你猜要导哪张。`,
          hint: '显式指定：`export <dir> --svg out/<name>-chart.svg`（结构图用 -diagram，数据图用 -chart）'
        })
        return result
      } else if (svgs.length) {
        svgPath = join(outDir, svgs[svgs.length - 1])
      }
    }
  }
  if (!svgPath) {
    result.skipped.push({
      format: formats.join(','),
      reason: `out/ 里没找到 SVG（找的是 ${join(outDir, (nameOpt || spec.name || 'figure') + '*.svg')}）。没有矢量源，导不出任何格式。`,
      hint: '先跑 `node scripts/fig.mjs render <dir>` 或 `chart <dir>` 生成 out/<name>-diagram.svg / -chart.svg，再 export。'
    })
    return result
  }

  // 产物基名跟随被导出的 SVG 文件名，避免结构图/数据图互相覆盖。
  const name = nameOpt || basename(svgPath, '.svg')
  result.sourceSvg = svgPath

  const svgText = readFileSync(svgPath, 'utf8')
  const size = readSvgSize(svgText)
  if (!size || !size.widthMm || !size.heightMm) {
    result.skipped.push({
      format: formats.join(','),
      reason: `SVG 根元素上没有可识别的物理尺寸（width/height 要以 mm 为单位，或给 viewBox）。没法按期刊 mm 换算像素。`,
      hint: '让 render 输出 width="89mm" height="60mm" 这种带单位的尺寸；或者手动在 SVG 上补。'
    })
    return result
  }

  const widthMm = Number(opts.widthMm) || size.widthMm
  const heightMm = Number(opts.heightMm) || size.heightMm
  const wPx = mmToPx(widthMm, dpi)
  const hPx = mmToPx(heightMm, dpi)
  result.size = { widthMm: round(widthMm, 2), heightMm: round(heightMm, 2), widthPx: wPx, heightPx: hPx, dpi }

  if (rasterizer.name === 'none') {
    for (const f of formats) {
      result.skipped.push({
        format: f,
        reason: '本机没有 Chrome 也没有 ImageMagick：没法把 SVG 转成位图/PDF。不是你的图有问题。',
        hint: '① 直接把 out/*.svg 交给期刊（多数期刊排版系统都收矢量 SVG/EPS）；② 或者装 Chrome（Google Chrome 免费）后重跑 export。'
      })
    }
    return result
  }

  /* --- 临时目录 --- */
  const tmpRoot = mkdtempSync(join(tmpdir(), 'paper-figure-'))
  const chromeState = {
    userDataDir: join(tmpRoot, 'chrome-profile'),
    crashDir: join(tmpRoot, 'chrome-crash')
  }
  try { mkdirSync(chromeState.userDataDir, { recursive: true }) } catch { /* ignore */ }
  try { mkdirSync(chromeState.crashDir, { recursive: true }) } catch { /* ignore */ }

  // 截图版：窗口多大就截多大，像素精确
  const htmlPxPath = join(tmpRoot, 'figure-px.html')
  writeFileSync(htmlPxPath, htmlWrapper(inlineSvgWithSize(svgText, `${wPx}px`, `${hPx}px`), widthMm, heightMm), 'utf8')
  // 打印版：SVG 直接用物理 mm，正好铺满 @page，否则 Chrome 会按 2102px 宽切成好几页
  const htmlMmPath = join(tmpRoot, 'figure-mm.html')
  writeFileSync(htmlMmPath, htmlWrapper(inlineSvgWithSize(svgText, `${round(widthMm, 3)}mm`, `${round(heightMm, 3)}mm`), widthMm, heightMm), 'utf8')

  const chrome = rasterizer.name === 'chrome'
    ? { path: rasterizer.path, ...chromeState }
    : null
  // TIFF 只能靠 ImageMagick，跟上面选中的栅格化工具是不是 Chrome 无关，所以要单独探一次
  const magickProbeNow = probeMagick()
  const magick = magickProbeNow.name === 'magick' ? { path: magickProbeNow.path } : null

  let pngPath = null

  try {
    /* ---------------- PNG ---------------- */
    if (formats.includes('png')) {
      const target = join(outDir, `${name}@${dpi}dpi.png`)
      if (chrome) {
        const r = chromeScreenshot(chrome, { htmlPath: htmlPxPath, outPath: target, wPx, hPx, timeoutMs })
        if (r.ok && existsSync(target)) {
          const dims = pngDims(target)
          if (dims) {
            const effDpi = dims.w / (widthMm / MM_PER_IN)
            const deltaPct = Math.abs(dims.w - wPx) / wPx * 100
            if (deltaPct > 3) {
              result.warnings.push(`PNG 实际 ${dims.w}×${dims.h}px，目标 ${wPx}×${hPx}px（差 ${round(deltaPct)}%），有效 ${Math.round(effDpi)}dpi。`)
            }
            pngPath = target
            result.files.push({
              path: target, format: 'png',
              widthPx: dims.w, heightPx: dims.h, dpi: Math.round(effDpi),
              bytes: dims.bytes, via: `chrome${r.mode === 'compat' ? '(compat)' : ''}`,
              note: `按 ${round(widthMm)}mm × ${dpi}dpi 换算，实际 ${dims.w}px`
            })
          }
        } else {
          result.skipped.push({
            format: 'png',
            reason: `Chrome 截图失败（${r.timedOut ? '超时' : `退出码 ${r.status ?? 'unknown'}`}）。${summarizeChromeError(r)}`,
            hint: '把 CHROME_PATH 指到可用的 Chrome，或先手动在浏览器里打开 out/*.svg 另存为 PNG。'
          })
        }
      }
      if (!pngPath && magick) {
        const target2 = join(outDir, `${name}@${dpi}dpi.png`)
        const r = magickConvert(magick, ['-density', String(dpi), '-background', 'white', '-flatten', svgPath, target2], timeoutMs)
        if (r.ok && existsSync(target2)) {
          const dims = pngDims(target2)
          const m = probeMagick()
          pngPath = target2
          result.files.push({
            path: target2, format: 'png',
            widthPx: dims ? dims.w : null, heightPx: dims ? dims.h : null,
            dpi, bytes: dims ? dims.bytes : null, via: 'magick', degraded: true,
            note: m.hasFonts
              ? '走 ImageMagick 兜底，精度和字体渲染都不如 Chrome，交稿前务必肉眼看一遍'
              : '走 ImageMagick 兜底，但本机 ImageMagick 没有字体引擎 —— 图里的文字很可能是空的，别直接交稿'
          })
          result.warnings.push('本次 PNG 是 ImageMagick 转的（没有 Chrome）。' + (m.hasFonts ? '' : '本机 ImageMagick 无字体引擎，文字可能丢失。'))
        } else {
          result.skipped.push({
            format: 'png',
            reason: `ImageMagick 转 PNG 失败（退出码 ${r.status}）${r.output ? `：${r.output.slice(0, 200)}` : ''}`,
            hint: '装 Chrome 最稳（免费），或者用浏览器打开 SVG 手动另存。'
          })
        }
      }
    }

    /* ---------------- PDF ---------------- */
    if (formats.includes('pdf')) {
      const target = join(outDir, `${name}.pdf`)
      let done = false
      if (chrome) {
        const r = chromePdf(chrome, { htmlPath: htmlMmPath, outPath: target, timeoutMs })
        if (r.ok && existsSync(target)) {
          const info = pdfInfo(target)
          const wantW = mmToPt(widthMm)
          const wantH = mmToPt(heightMm)
          const boxOk = info && info.box && Math.abs(info.box.w - wantW) < 3 && Math.abs(info.box.h - wantH) < 3
          if (!boxOk) {
            result.warnings.push(`PDF 页面尺寸 ${info && info.box ? `${round(info.box.w)}×${round(info.box.h)}pt` : '读不出'}，期望 ${round(wantW)}×${round(wantH)}pt（${round(widthMm)}×${round(heightMm)}mm）。投稿前用阅读器确认下页面大小。`)
          }
          if (info && info.pages && info.pages > 1) {
            result.warnings.push(`PDF 有 ${info.pages} 页，应该是 1 页 —— 检查 SVG 是否超出页面高度。`)
          }
          result.files.push({
            path: target, format: 'pdf',
            widthPx: info && info.box ? Math.round(info.box.w) : null,
            heightPx: info && info.box ? Math.round(info.box.h) : null,
            unit: 'pt',
            dpi: null, bytes: info ? info.bytes : statSync(target).size,
            via: `chrome${r.mode === 'compat' ? '(compat)' : ''}`,
            note: `矢量 PDF，页面 ${round(widthMm)}×${round(heightMm)}mm${info && info.box ? `（MediaBox ${round(info.box.w)}×${round(info.box.h)}pt）` : ''}`
          })
          done = true
        } else {
          result.skipped.push({
            format: 'pdf',
            reason: `Chrome 打印 PDF 失败（${r.timedOut ? '超时' : `退出码 ${r.status ?? 'unknown'}`}）。${summarizeChromeError(r)}`,
            hint: '先交 SVG；或者装 Chrome 后重试。'
          })
        }
      }
      if (!done && magick) {
        const r = magickConvert(magick, [svgPath, target], timeoutMs)
        if (r.ok && existsSync(target)) {
          result.files.push({
            path: target, format: 'pdf', widthPx: null, heightPx: null, dpi: null,
            bytes: statSync(target).size, via: 'magick', degraded: true,
            note: '走 ImageMagick 兜底；本机 ImageMagick 缺 ghostscript 时这条一般会失败，成功也要肉眼验一遍'
          })
          done = true
          result.warnings.push('本次 PDF 是 ImageMagick 转的（没有 Chrome），字体/矢量保真度不保证。')
        } else if (!chrome) {
          result.skipped.push({
            format: 'pdf',
            reason: `ImageMagick 出 PDF 失败（退出码 ${r.status}）${r.output ? `：${r.output.slice(0, 160)}` : ''}。多半是缺 ghostscript。`,
            hint: 'SVG 本身就能直接投（多数期刊接受矢量），或者装 Chrome。'
          })
        }
      }
    }

    /* ---------------- TIFF ---------------- */
    if (formats.includes('tif') || formats.includes('tiff')) {
      const target = join(outDir, `${name}.tif`)
      if (!magick) {
        result.skipped.push({
          format: 'tif',
          reason: 'TIFF 只能靠 ImageMagick 从 PNG 转（Chrome 不会写 TIFF），本机没有 ImageMagick。',
          hint: '期刊大多也接受 PNG（300/600dpi）或矢量 PDF；真需要 TIFF 就 `brew install imagemagick` 后重跑。'
        })
      } else {
        // 没有 PNG 就临时生成一张（TIFF 从 PNG 转，绕开 SVG 缺字体的问题）
        let srcPng = pngPath
        let tempPng = null
        if (!srcPng && chrome) {
          tempPng = join(tmpRoot, 'for-tiff.png')
          const r = chromeScreenshot(chrome, { htmlPath: htmlPxPath, outPath: tempPng, wPx, hPx, timeoutMs })
          if (r.ok && existsSync(tempPng)) srcPng = tempPng
        }
        if (!srcPng) {
          result.skipped.push({
            format: 'tif',
            reason: '没有可用的 PNG 作为 TIFF 的输入（PNG 那步也没成），没法转。',
            hint: '先把 PNG 导出成功，再导 TIFF；或直接交 PNG/PDF。'
          })
        } else {
          const r = magickConvert(magick, [
            srcPng, '-compress', 'lzw', '-units', 'PixelsPerInch', '-density', String(dpi), target
          ], timeoutMs)
          if (r.ok && existsSync(target)) {
            const d = pngDims(srcPng)
            result.files.push({
              path: target, format: 'tif',
              widthPx: d ? d.w : null, heightPx: d ? d.h : null,
              dpi, bytes: statSync(target).size, via: 'magick(png→tif)',
              note: `LZW 压缩，${dpi}dpi 元数据；源图 ${d ? `${d.w}×${d.h}px` : 'png'}`
            })
          } else {
            result.skipped.push({
              format: 'tif',
              reason: `ImageMagick 转 TIFF 失败（退出码 ${r.status}）${r.output ? `：${r.output.slice(0, 160)}` : ''}`,
              hint: '先交 PNG（期刊普遍接受），或换一台有 ImageMagick 的机器重跑。'
            })
          }
        }
      }
    }
  } finally {
    if (!opts.keepTemp) {
      try { rmSync(tmpRoot, { recursive: true, force: true }) } catch { /* ignore */ }
    } else {
      result.tempDir = tmpRoot
    }
  }

  result.ok = result.files.length > 0
  if (!result.ok && result.skipped.length) {
    result.fix = '看 skipped 里每个格式的原因；最常见的是本机没装 Chrome。SVG 本身可以直接交稿，不一定要位图。'
  }
  return result
}

function summarizeChromeError(r) {
  const out = r && r.output ? r.output : ''
  if (/sandbox initialization failed|SUID sandbox|namespace sandbox/i.test(out)) {
    return '看起来是沙箱没起来（这个环境禁了 Chrome 的沙箱）—— 重跑一般会自动切兼容模式。'
  }
  if (/profile|user data directory|SingletonLock/i.test(out)) {
    return '看起来是 Chrome 用户目录被占用 / 冲突。'
  }
  if (/cannot find|No such file/i.test(out)) {
    return 'Chrome 路径不对。'
  }
  return out ? `Chrome 输出：${out.split('\n').slice(-3).join(' ').slice(0, 240)}` : 'Chrome 没有输出。'
}

function normalizeFormats(formats) {
  const raw = Array.isArray(formats)
    ? formats
    : String(formats || DEFAULTS.formats.join(',')).split(',')
  const out = []
  for (const f of raw) {
    const v = String(f).trim().toLowerCase().replace(/^\./, '')
    if (!v) continue
    if (v === 'tiff') { if (!out.includes('tif')) out.push('tif'); continue }
    if (!['png', 'pdf', 'tif'].includes(v)) continue
    if (!out.includes(v)) out.push(v)
  }
  return out.length ? out : ['png', 'pdf', 'tif']
}

/* ==========================================================================
 * 七、CLI
 * ========================================================================== */

async function main(argv) {
  const args = argv.slice(2)
  const flags = {}
  const rest = []
  for (let i = 0; i < args.length; i++) {
    const a = args[i]
    if (a === '--json') flags.json = true
    else if (a === '--detect') flags.detect = true
    else if (a === '--keep-temp') flags.keepTemp = true
    else if (a.startsWith('--')) { flags[a.slice(2)] = args[i + 1]; i++ }
    else rest.push(a)
  }

  if (flags.detect) {
    const r = detectRasterizer()
    process.stdout.write(JSON.stringify(r, null, 2) + '\n')
    return
  }

  const workDir = rest[0] || process.cwd()
  process.stderr.write('[export] 检查栅格化工具…\n')
  const res = await exportFigure(workDir, {
    formats: flags.formats,
    dpi: flags.dpi ? Number(flags.dpi) : undefined,
    svgPath: flags.svg,
    name: flags.name,
    keepTemp: flags.keepTemp === true
  })
  if (flags.json) {
    process.stdout.write(JSON.stringify(res, null, 2) + '\n')
  } else {
    if (res.files.length) {
      process.stdout.write(`导出了 ${res.files.length} 个文件：\n`)
      for (const f of res.files) {
        process.stdout.write(`  ${f.format.toUpperCase().padEnd(4)} ${f.path}${f.widthPx ? `  ${f.widthPx}×${f.heightPx}${f.unit === 'pt' ? 'pt' : 'px'}` : ''}${f.dpi ? `  ${f.dpi}dpi` : ''}${f.degraded ? '  [降级]' : ''}\n`)
        if (f.note) process.stdout.write(`        ${f.note}\n`)
      }
    }
    for (const s of res.skipped) process.stdout.write(`跳过 ${s.format}：${s.reason}\n  → ${s.hint}\n`)
    for (const w of res.warnings) process.stdout.write(`提醒：${w}\n`)
    if (!res.files.length) process.stdout.write(`\n一个格式都没导出来。${res.fix || ''}\n`)
  }
  process.exit(res.ok ? 0 : 1)
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  main(process.argv).catch((e) => {
    process.stderr.write(`导出器自己崩了：${e && e.stack ? e.stack : e}\n`)
    process.exit(2)
  })
}

export default exportFigure
