#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { JSDOM } from 'jsdom';
import { Readability } from '@mozilla/readability';
import TurndownService from 'turndown';
import { gfm } from 'turndown-plugin-gfm';

const PROFILE_PRESETS = {
  article: {
    contentMode: 'readable',
    keepSelectors: 'article,main,.post,.article,.content',
    removeSelectors: 'script,style,nav,footer,noscript,aside,.sidebar,.ad,.ads,.recommend,.related,.breadcrumb,.toc',
  },
  docs: {
    contentMode: 'full',
    keepSelectors: 'main,article,.markdown-body,.content,.doc-content',
    removeSelectors: 'script,style,noscript,.sidebar-ads,.feedback,.page-tools',
  },
  forum: {
    contentMode: 'readable',
    keepSelectors: '.topic,.post,.message,article,main,.content',
    removeSelectors: 'script,style,nav,footer,noscript,aside,.signature,.user-card,.ad,.ads,.recommend',
  },
  custom: {
    contentMode: 'readable',
    keepSelectors: '',
    removeSelectors: 'script,style,nav,footer,noscript,aside',
  },
};

function printHelp() {
  console.log(`
HTML to Markdown Converter (v4)

Usage:
  node scripts/html_to_markdown.mjs [options]

Input (choose one):
  --file <path>                   Input HTML file
  --html <string>                 Input HTML string
  --url <https://...>             Fetch HTML from URL
  --input-dir <dir>               Batch convert all .html/.htm files recursively
  --url-list <file.txt>           Batch convert URLs from text file (one URL per line)

Output:
  --out <path>                    Output markdown file (single mode)
  --output-dir <dir>              Output directory (batch mode)

Options:
  --format <gfm|commonmark>       Output format (default: gfm)
  --engine <auto|best|turndown|pandoc> Converter engine (default: auto)
  --profile <article|docs|forum|custom> preset for cleanup & structure (default: article)
  --content-mode <readable|full>  readable=正文提取, full=尽量保留全文结构
  --extract-readable <true|false> Backward compatible alias for content-mode
  --meta-frontmatter <true|false> Prepend YAML frontmatter metadata (default: false)
  --remove-selectors <csv>        Remove selectors (custom mode recommended)
  --keep-selectors <csv>          Keep only selected roots (e.g. main,article)
  --base-url <url>                Base URL for resolving relative links/images
  --image-style <inline|ref>      Image markdown style (default: inline)
  --report <path.json>            Write quality report json
  --timeout-ms <n>                URL fetch timeout ms (default: 20000)
  --dry-run                       Show what will be processed
  --help                          Show help

Examples:
  node scripts/html_to_markdown.mjs --file ./a.html --out ./a.md --profile article --meta-frontmatter true
  node scripts/html_to_markdown.mjs --url https://example.com --out ./example.md --engine best --report ./report.json
  node scripts/html_to_markdown.mjs --input-dir ./html --output-dir ./md --profile docs
  node scripts/html_to_markdown.mjs --url-list ./urls.txt --output-dir ./md --profile forum --report ./batch-report.json
`);
}

function parseArgs(argv) {
  const args = {
    format: 'gfm',
    engine: 'auto',
    contentMode: 'readable',
    removeSelectors: 'script,style,nav,footer,noscript,aside',
    keepSelectors: '',
    dryRun: false,
    imageStyle: 'inline',
    timeoutMs: 20000,
    metaFrontmatter: false,
    profile: 'article',
  };
  for (let i = 2; i < argv.length; i++) {
    const k = argv[i];
    const v = argv[i + 1];
    switch (k) {
      case '--file': args.file = v; i++; break;
      case '--html': args.html = v; i++; break;
      case '--url': args.url = v; i++; break;
      case '--out': args.out = v; i++; break;
      case '--input-dir': args.inputDir = v; i++; break;
      case '--output-dir': args.outputDir = v; i++; break;
      case '--url-list': args.urlList = v; i++; break;
      case '--format': args.format = v; i++; break;
      case '--engine': args.engine = v; i++; break;
      case '--profile': args.profile = v || 'article'; i++; break;
      case '--content-mode': args.contentMode = v || 'readable'; i++; break;
      case '--extract-readable': {
        const on = (v ?? '').toLowerCase() !== 'false';
        args.contentMode = on ? 'readable' : 'full';
        i++;
        break;
      }
      case '--meta-frontmatter': args.metaFrontmatter = (v ?? '').toLowerCase() === 'true'; i++; break;
      case '--remove-selectors': args.removeSelectors = v ?? ''; i++; break;
      case '--keep-selectors': args.keepSelectors = v ?? ''; i++; break;
      case '--base-url': args.baseUrl = v; i++; break;
      case '--image-style': args.imageStyle = v ?? 'inline'; i++; break;
      case '--report': args.report = v; i++; break;
      case '--timeout-ms': args.timeoutMs = Number(v || 20000); i++; break;
      case '--dry-run': args.dryRun = true; break;
      case '--help': args.help = true; break;
      default:
        throw new Error(`Unknown argument: ${k}`);
    }
  }
  return args;
}

function applyProfile(args) {
  const p = PROFILE_PRESETS[args.profile] || PROFILE_PRESETS.article;

  const isDefaultRemove = args.removeSelectors === 'script,style,nav,footer,noscript,aside';
  const isDefaultKeep = !args.keepSelectors;
  const isDefaultMode = args.contentMode === 'readable';

  if (isDefaultMode) args.contentMode = p.contentMode;
  if (isDefaultKeep) args.keepSelectors = p.keepSelectors;
  if (isDefaultRemove) args.removeSelectors = p.removeSelectors;

  return args;
}

function ensureSingleInput(a) {
  const count = [a.file, a.html, a.url, a.inputDir, a.urlList].filter(Boolean).length;
  if (count === 0) throw new Error('Provide one input: --file/--html/--url/--input-dir/--url-list');
  if (count > 1) throw new Error('Use only one input mode at a time');
  if ((a.inputDir || a.urlList) && !a.outputDir) throw new Error('--input-dir/--url-list requires --output-dir');
  if (!(a.inputDir || a.urlList) && !a.out) throw new Error('Single mode requires --out');
  if (!['gfm', 'commonmark'].includes(a.format)) throw new Error('--format must be gfm|commonmark');
  if (!['auto', 'best', 'turndown', 'pandoc'].includes(a.engine)) throw new Error('--engine must be auto|best|turndown|pandoc');
  if (!['inline', 'ref'].includes(a.imageStyle)) throw new Error('--image-style must be inline|ref');
  if (!['readable', 'full'].includes(a.contentMode)) throw new Error('--content-mode must be readable|full');
  if (!Object.keys(PROFILE_PRESETS).includes(a.profile)) throw new Error('--profile must be article|docs|forum|custom');
}

function csvToList(v) {
  return (v || '').split(',').map(s => s.trim()).filter(Boolean);
}

async function collectHtmlFiles(dir) {
  const out = [];
  async function walk(d) {
    const items = await fs.readdir(d, { withFileTypes: true });
    for (const it of items) {
      const p = path.join(d, it.name);
      if (it.isDirectory()) await walk(p);
      else if (/\.(html?|xhtml)$/i.test(it.name)) out.push(p);
    }
  }
  await walk(dir);
  return out;
}

async function readUrlList(file) {
  const txt = await fs.readFile(file, 'utf8');
  return txt
    .split(/\r?\n/)
    .map(s => s.trim())
    .filter(Boolean)
    .filter(s => !s.startsWith('#'));
}

function sanitizeFilename(name) {
  return name
    .replace(/[<>:"/\\|?*\x00-\x1F]/g, '-')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 120) || 'output';
}

function fileNameFromUrl(u) {
  try {
    const url = new URL(u);
    const host = sanitizeFilename(url.hostname);
    const p = sanitizeFilename(url.pathname.replace(/^\//, '').replace(/\//g, '-'));
    return p ? `${host}-${p}.md` : `${host}.md`;
  } catch {
    return `${sanitizeFilename(u)}.md`;
  }
}

async function fetchWithTimeout(url, timeoutMs = 20000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { redirect: 'follow', signal: controller.signal });
    if (!res.ok) throw new Error(`Fetch failed: ${res.status} ${res.statusText}`);
    return await res.text();
  } finally {
    clearTimeout(timer);
  }
}

async function readInput(args) {
  if (args.file) return fs.readFile(args.file, 'utf8');
  if (args.html) return args.html;
  if (args.url) return fetchWithTimeout(args.url, args.timeoutMs);
  throw new Error('No input');
}

function absolutizeUrl(ref, baseUrl) {
  if (!ref) return '';
  try {
    return new URL(ref, baseUrl).toString();
  } catch {
    return ref;
  }
}

function textOrNull(v) {
  const s = (v || '').trim();
  return s.length ? s : null;
}

function metaBy(document, selector, attr = 'content') {
  const n = document.querySelector(selector);
  if (!n) return null;
  return textOrNull(n.getAttribute(attr));
}

function extractMetadata(document, sourceUrl) {
  const title = textOrNull(document.querySelector('title')?.textContent)
    || metaBy(document, 'meta[property="og:title"]')
    || metaBy(document, 'meta[name="twitter:title"]');

  const description = metaBy(document, 'meta[name="description"]')
    || metaBy(document, 'meta[property="og:description"]')
    || metaBy(document, 'meta[name="twitter:description"]');

  const author = metaBy(document, 'meta[name="author"]')
    || metaBy(document, 'meta[property="article:author"]')
    || textOrNull(document.querySelector('[rel="author"]')?.textContent);

  const published = metaBy(document, 'meta[property="article:published_time"]')
    || metaBy(document, 'meta[name="pubdate"]')
    || textOrNull(document.querySelector('time[datetime]')?.getAttribute('datetime'));

  return {
    title,
    description,
    author,
    published,
    source: textOrNull(sourceUrl),
    extractedAt: new Date().toISOString(),
  };
}

function yamlEscape(v) {
  return String(v).replace(/"/g, '\\"');
}

function buildFrontmatter(meta) {
  const lines = ['---'];
  for (const k of ['title', 'description', 'author', 'published', 'source', 'extractedAt']) {
    if (meta[k]) lines.push(`${k}: "${yamlEscape(meta[k])}"`);
  }
  lines.push('---', '');
  return lines.join('\n');
}

function cleanupDom(document, keepSelectors, removeSelectors, baseUrl) {
  if (keepSelectors.length) {
    const keepNodes = keepSelectors.flatMap(sel => Array.from(document.querySelectorAll(sel)));
    if (keepNodes.length > 0) {
      const wrapper = document.createElement('div');
      for (const n of keepNodes) wrapper.appendChild(n.cloneNode(true));
      document.body.innerHTML = '';
      document.body.appendChild(wrapper);
    }
  }

  for (const sel of removeSelectors) {
    for (const n of document.querySelectorAll(sel)) n.remove();
  }

  for (const a of document.querySelectorAll('a[href]')) {
    a.setAttribute('href', absolutizeUrl(a.getAttribute('href'), baseUrl));
  }
  for (const img of document.querySelectorAll('img')) {
    const src = img.getAttribute('src') || img.getAttribute('data-src') || img.getAttribute('data-original') || '';
    if (src) img.setAttribute('src', absolutizeUrl(src, baseUrl));
  }
}

function makeTurndown(format = 'gfm', imageStyle = 'inline') {
  const td = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced',
    bulletListMarker: '-',
    emDelimiter: '*',
    linkStyle: 'inlined',
  });
  if (format === 'gfm') td.use(gfm);

  td.addRule('image-fallback', {
    filter: 'img',
    replacement: function (_content, node) {
      const alt = node.getAttribute('alt') || '';
      const src = node.getAttribute('src') || '';
      const title = node.getAttribute('title') || '';
      if (!src) return '';
      if (imageStyle === 'ref') {
        const id = `img-${Math.random().toString(36).slice(2, 8)}`;
        return `![${alt}][${id}]\n\n[${id}]: ${src}${title ? ` \"${title}\"` : ''}`;
      }
      return `![${alt}](${src}${title ? ` \"${title}\"` : ''})`;
    }
  });

  return td;
}

function htmlToMdTurndown(html, format = 'gfm', imageStyle = 'inline') {
  const td = makeTurndown(format, imageStyle);
  return td.turndown(html).trim() + '\n';
}

function runPandoc(html, format = 'gfm') {
  return new Promise((resolve, reject) => {
    const to = format === 'commonmark' ? 'commonmark' : 'gfm';
    const child = spawn('pandoc', ['-f', 'html', '-t', to], { stdio: ['pipe', 'pipe', 'pipe'] });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', d => (stdout += d.toString()));
    child.stderr.on('data', d => (stderr += d.toString()));
    child.on('error', reject);
    child.on('close', code => {
      if (code === 0) resolve((stdout || '').trim() + '\n');
      else reject(new Error(`pandoc failed(${code}): ${stderr || 'unknown error'}`));
    });
    child.stdin.write(html);
    child.stdin.end();
  });
}

function extractReadableHtml(rawHtml, sourceUrl = 'https://example.com') {
  const dom = new JSDOM(rawHtml, { url: sourceUrl });
  const reader = new Readability(dom.window.document);
  const parsed = reader.parse();
  if (!parsed || !parsed.content) return rawHtml;
  return `<article><h1>${parsed.title || ''}</h1>${parsed.content}</article>`;
}

function qualityScore(rawHtml, markdown) {
  const rawTextLen = String(rawHtml || '').replace(/<[^>]*>/g, '').trim().length;
  const mdTextLen = String(markdown || '').replace(/[`*_#>\-\[\]\(\)|]/g, '').trim().length;
  const ratio = rawTextLen > 0 ? mdTextLen / rawTextLen : 1;

  const htmlLinks = (String(rawHtml).match(/<a\b/gi) || []).length;
  const mdLinks = (String(markdown).match(/\[[^\]]+\]\([^\)]+\)/g) || []).length;

  const htmlImgs = (String(rawHtml).match(/<img\b/gi) || []).length;
  const mdImgs = (String(markdown).match(/!\[[^\]]*\]\([^\)]+\)/g) || []).length;

  let score = 100;
  if (ratio < 0.2) score -= 25;
  if (ratio > 2.5) score -= 8;
  if (htmlLinks > 0 && mdLinks === 0) score -= 20;
  if (htmlImgs > 0 && mdImgs === 0) score -= 15;
  if (mdTextLen < 30) score -= 20;
  if (score < 0) score = 0;

  return {
    score,
    ratio: Number(ratio.toFixed(3)),
    rawTextLen,
    mdTextLen,
    htmlLinks,
    mdLinks,
    htmlImgs,
    mdImgs,
  };
}

async function convertOne(rawHtml, args, sourceUrl) {
  const effectiveBaseUrl = args.baseUrl || sourceUrl || 'https://example.com';

  const rawDom = new JSDOM(rawHtml, { url: effectiveBaseUrl });
  const metadata = extractMetadata(rawDom.window.document, effectiveBaseUrl);

  const dom = new JSDOM(rawHtml, { url: effectiveBaseUrl });
  const keepSelectors = csvToList(args.keepSelectors);
  const removeSelectors = csvToList(args.removeSelectors);

  cleanupDom(dom.window.document, keepSelectors, removeSelectors, effectiveBaseUrl);
  let htmlForConvert = dom.serialize();

  if (args.contentMode === 'readable') {
    htmlForConvert = extractReadableHtml(htmlForConvert, effectiveBaseUrl);
  }

  let markdown = '';
  let engineUsed = args.engine;
  let candidates = undefined;

  const runTurndown = async () => htmlToMdTurndown(htmlForConvert, args.format, args.imageStyle);
  const runPd = async () => runPandoc(htmlForConvert, args.format);

  if (args.engine === 'turndown') {
    markdown = await runTurndown();
  } else if (args.engine === 'pandoc') {
    markdown = await runPd();
  } else if (args.engine === 'best') {
    const result = { turndown: null, pandoc: null };
    try {
      const mdT = await runTurndown();
      result.turndown = { markdown: mdT, quality: qualityScore(htmlForConvert, mdT) };
    } catch (e) {
      result.turndown = { error: e.message };
    }
    try {
      const mdP = await runPd();
      result.pandoc = { markdown: mdP, quality: qualityScore(htmlForConvert, mdP) };
    } catch (e) {
      result.pandoc = { error: e.message };
    }

    candidates = {
      turndown: result.turndown?.quality?.score ?? null,
      pandoc: result.pandoc?.quality?.score ?? null,
    };

    const tScore = result.turndown?.quality?.score ?? -1;
    const pScore = result.pandoc?.quality?.score ?? -1;

    if (tScore >= pScore && result.turndown?.markdown) {
      markdown = result.turndown.markdown;
      engineUsed = 'best:turndown';
    } else if (result.pandoc?.markdown) {
      markdown = result.pandoc.markdown;
      engineUsed = 'best:pandoc';
    } else {
      throw new Error('best mode failed: both turndown and pandoc failed');
    }
  } else {
    // auto: turndown first, pandoc fallback
    engineUsed = 'turndown';
    try {
      markdown = await runTurndown();
    } catch {
      engineUsed = 'pandoc';
      markdown = await runPd();
    }
  }

  const quality = qualityScore(htmlForConvert, markdown);

  if (args.metaFrontmatter) {
    markdown = buildFrontmatter(metadata) + markdown;
  }

  return {
    markdown,
    engineUsed,
    quality,
    metadata,
    candidates,
  };
}

async function writeFileEnsure(outPath, content) {
  await fs.mkdir(path.dirname(outPath), { recursive: true });
  await fs.writeFile(outPath, content, 'utf8');
}

function toOutputPath(inputDir, outputDir, file) {
  const rel = path.relative(inputDir, file);
  const noExt = rel.replace(/\.(html?|xhtml)$/i, '');
  return path.join(outputDir, `${noExt}.md`);
}

async function maybeWriteReport(args, reportObj) {
  if (!args.report) return;
  await writeFileEnsure(args.report, JSON.stringify(reportObj, null, 2));
}

async function runBatchFiles(args) {
  const files = await collectHtmlFiles(args.inputDir);
  if (files.length === 0) {
    console.log('No HTML files found.');
    return;
  }
  console.log(`Found ${files.length} HTML files.`);
  if (args.dryRun) {
    for (const f of files) console.log(`- ${f}`);
    return;
  }

  let ok = 0;
  let fail = 0;
  const report = { mode: 'input-dir', profile: args.profile, total: files.length, success: 0, failed: 0, items: [] };

  for (const f of files) {
    const out = toOutputPath(args.inputDir, args.outputDir, f);
    try {
      const raw = await fs.readFile(f, 'utf8');
      const res = await convertOne(raw, args, `file://${f}`);
      await writeFileEnsure(out, res.markdown);
      ok++;
      report.items.push({
        input: f,
        output: out,
        ok: true,
        engineUsed: res.engineUsed,
        candidates: res.candidates,
        quality: res.quality,
        metadata: res.metadata,
      });
    } catch (e) {
      fail++;
      report.items.push({ input: f, output: out, ok: false, error: e.message });
      console.error(`[FAIL] ${f}: ${e.message}`);
    }
  }

  report.success = ok;
  report.failed = fail;
  await maybeWriteReport(args, report);
  console.log(`Done. success=${ok}, failed=${fail}`);
}

async function runBatchUrls(args) {
  const urls = await readUrlList(args.urlList);
  if (urls.length === 0) {
    console.log('No URLs found in url-list file.');
    return;
  }
  console.log(`Found ${urls.length} URLs.`);
  if (args.dryRun) {
    for (const u of urls) console.log(`- ${u}`);
    return;
  }

  let ok = 0;
  let fail = 0;
  const report = { mode: 'url-list', profile: args.profile, total: urls.length, success: 0, failed: 0, items: [] };

  for (const u of urls) {
    const out = path.join(args.outputDir, fileNameFromUrl(u));
    try {
      const raw = await fetchWithTimeout(u, args.timeoutMs);
      const res = await convertOne(raw, args, u);
      await writeFileEnsure(out, res.markdown);
      ok++;
      report.items.push({
        input: u,
        output: out,
        ok: true,
        engineUsed: res.engineUsed,
        candidates: res.candidates,
        quality: res.quality,
        metadata: res.metadata,
      });
    } catch (e) {
      fail++;
      report.items.push({ input: u, output: out, ok: false, error: e.message });
      console.error(`[FAIL] ${u}: ${e.message}`);
    }
  }

  report.success = ok;
  report.failed = fail;
  await maybeWriteReport(args, report);
  console.log(`Done. success=${ok}, failed=${fail}`);
}

async function runSingle(args) {
  const raw = await readInput(args);
  const sourceUrl = args.baseUrl || args.url || (args.file ? `file://${path.resolve(args.file)}` : 'https://example.com');
  const res = await convertOne(raw, args, sourceUrl);
  await writeFileEnsure(args.out, res.markdown);

  await maybeWriteReport(args, {
    mode: 'single',
    profile: args.profile,
    input: args.file || args.url || 'inline-html',
    output: args.out,
    ok: true,
    engineUsed: res.engineUsed,
    candidates: res.candidates,
    quality: res.quality,
    metadata: res.metadata,
  });

  console.log(`OK -> ${args.out} (engine=${res.engineUsed}, score=${res.quality.score})`);
}

async function main() {
  let args = parseArgs(process.argv);
  if (args.help) return printHelp();
  ensureSingleInput(args);
  args = applyProfile(args);

  if (args.inputDir) return runBatchFiles(args);
  if (args.urlList) return runBatchUrls(args);
  return runSingle(args);
}

main().catch(err => {
  console.error('[ERROR]', err.message);
  process.exit(1);
});

