#!/usr/bin/env node
// Next.js App Router auditor — zero dependencies, Node 18+.
// Static heuristic scan of an app/ directory for RSC boundary mistakes,
// request waterfalls, client/server anti-patterns and Core Web Vitals risks.
//
// Usage:
//   node scripts/audit.mjs [path-to-project-or-app-dir] [--json]
//
// Exit code: 0 if no ERROR findings, 1 otherwise (CI-friendly).

import { readdirSync, readFileSync, statSync, existsSync } from "node:fs";
import { join, basename, dirname, relative } from "node:path";

const argv = process.argv.slice(2);
const asJson = argv.includes("--json");
const target = argv.find((a) => !a.startsWith("--")) || ".";

// ── locate the app/ directory ────────────────────────────────────────────────
function resolveAppDir(root) {
  if (basename(root) === "app") return root;
  for (const c of [join(root, "app"), join(root, "src", "app")]) {
    if (existsSync(c) && statSync(c).isDirectory()) return c;
  }
  return null;
}

const appDir = resolveAppDir(target);
if (!appDir) {
  console.error(
    `No app/ directory found under "${target}". Point me at a Next.js App Router project.`,
  );
  process.exit(2);
}
const projectRoot = basename(target) === "app" ? dirname(target) : target;

// ── walk source files ────────────────────────────────────────────────────────
const SRC = /\.(tsx|ts|jsx|js)$/;
const SKIP = new Set(["node_modules", ".next", ".git", "dist", "build"]);
function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (SKIP.has(name)) continue;
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) walk(p, out);
    else if (SRC.test(name)) out.push(p);
  }
  return out;
}

// ── finding helpers ──────────────────────────────────────────────────────────
const findings = [];
function add(file, line, severity, rule, message, fix) {
  findings.push({ file, line, severity, rule, message, fix });
}
// line number of a regex match within source
function lineOf(src, index) {
  return src.slice(0, index).split("\n").length;
}
function firstMatchLine(src, re) {
  const m = re.exec(src);
  return m ? lineOf(src, m.index) : 1;
}
function allMatchLines(src, re) {
  const lines = [];
  let m;
  const g = new RegExp(re.source, re.flags.includes("g") ? re.flags : re.flags + "g");
  while ((m = g.exec(src))) lines.push(lineOf(src, m.index));
  return lines;
}

// ── detectors ────────────────────────────────────────────────────────────────
const RE = {
  useClient: /^\s*['"]use client['"]/m,
  clientHooks: /\buse(State|Effect|LayoutEffect|Reducer|Ref|Context|Callback|Memo|Transition|ImperativeHandle)\b/,
  routerHooks: /\buse(Router|Pathname|SearchParams|SelectedLayoutSegment)\b/,
  eventHandler: /\son[A-Z]\w+\s*=\s*[{(]/,
  browserApi: /\b(window|document|localStorage|sessionStorage|navigator|matchMedia)\b/,
  awaitFetch: /=\s*await\s+(fetch|[a-zA-Z_$][\w$]*\.(get|post|query|find|select))\b/,
  promiseAll: /Promise\.all\s*\(/,
  rawImg: /<img\b/,
  googleFontsLink: /<link[^>]+fonts\.(googleapis|gstatic)\.com/,
  fontImport: /@import[^;]+fonts\.(googleapis|gstatic)/,
  forceDynamic: /export\s+const\s+dynamic\s*=\s*['"]force-dynamic['"]/,
  metadataExport: /export\s+(const\s+metadata\b|async\s+function\s+generateMetadata\b)/,
  asyncDefault: /export\s+default\s+async\s+function/,
  dangerHtml: /dangerouslySetInnerHTML/,
  useEffect: /useEffect\s*\(/,
  fetchCall: /\bfetch\s*\(/,
  barrelStarReexport: /export\s+\*\s+from/,
  legacyHead: /import\s+\w+\s+from\s+['"]next\/head['"]/,
  legacyImage: /from\s+['"]next\/legacy\/image['"]/,
};

function analyze(file, src) {
  const rel = relative(projectRoot, file);
  const name = basename(file);
  const isClient = RE.useClient.test(src);
  const isPage = /^page\.(tsx|ts|jsx|js)$/.test(name);
  const isLayout = /^layout\.(tsx|ts|jsx|js)$/.test(name);

  const usesClientFeatures =
    RE.clientHooks.test(src) ||
    RE.routerHooks.test(src) ||
    RE.eventHandler.test(src) ||
    RE.browserApi.test(src);

  // 1. "use client" with no client-only features → push it down the tree
  if (isClient && !usesClientFeatures) {
    add(rel, firstMatchLine(src, RE.useClient), "WARN", "needless-use-client",
      `"use client" but no hooks, event handlers or browser APIs found — this can likely be a Server Component.`,
      `Remove the directive, or move it to the small leaf that truly needs interactivity.`);
  }

  // 2. Page/layout that is a Client Component cannot export metadata
  if ((isPage || isLayout) && isClient) {
    add(rel, firstMatchLine(src, RE.useClient), "ERROR", "client-route-no-metadata",
      `A Client Component ${isPage ? "page" : "layout"} cannot export \`metadata\` / \`generateMetadata\` — its SEO tags are silently dropped.`,
      `Keep ${name} a Server Component and isolate the interactive bits into a child marked "use client".`);
  }

  // 3. Data fetching inside useEffect in a client component
  if (isClient && RE.useEffect.test(src) && RE.fetchCall.test(src)) {
    add(rel, firstMatchLine(src, RE.useEffect), "WARN", "client-fetch-in-effect",
      `Fetching data in useEffect on the client — adds a render round-trip and hurts LCP/INP.`,
      `Fetch in a Server Component (or Server Action) and pass data down as props.`);
  }

  // 4. Request waterfall: ≥2 sequential awaited fetches, no Promise.all
  if (!isClient) {
    const awaitLines = allMatchLines(src, RE.awaitFetch);
    if (awaitLines.length >= 2 && !RE.promiseAll.test(src)) {
      add(rel, awaitLines[0], "INFO", "request-waterfall",
        `${awaitLines.length} sequential awaited fetches without Promise.all — likely a request waterfall.`,
        `Kick off independent requests together: \`const [a, b] = await Promise.all([...])\`.`);
    }
  }

  // 5. Raw <img> instead of next/image
  for (const ln of allMatchLines(src, RE.rawImg)) {
    add(rel, ln, "WARN", "raw-img",
      `Raw <img> skips automatic sizing, lazy-loading and AVIF/WebP — a common CLS/LCP regression.`,
      `Use \`next/image\` with explicit width/height (or fill).`);
  }

  // 6. Fonts loaded via <link>/@import instead of next/font
  if (RE.googleFontsLink.test(src) || RE.fontImport.test(src)) {
    add(rel, firstMatchLine(src, RE.googleFontsLink.test(src) ? RE.googleFontsLink : RE.fontImport),
      "WARN", "unoptimized-font",
      `Web font loaded over the network — render-blocking and causes layout shift.`,
      `Use \`next/font\` to self-host and preload with zero layout shift.`);
  }

  // 7. force-dynamic
  if (RE.forceDynamic.test(src)) {
    add(rel, firstMatchLine(src, RE.forceDynamic), "INFO", "force-dynamic",
      `\`dynamic = 'force-dynamic'\` opts the whole route out of static/ISR rendering.`,
      `Confirm it's needed; prefer per-request \`fetch(..., { cache })\` or \`revalidate\` for granular control.`);
  }

  // 8. Async page with no metadata export
  if (isPage && !isClient && RE.asyncDefault.test(src) && !RE.metadataExport.test(src)) {
    add(rel, firstMatchLine(src, RE.asyncDefault), "WARN", "page-missing-metadata",
      `Async page exports no \`metadata\`/\`generateMetadata\` — the route ships without title/description.`,
      `Add \`export const metadata\` or \`generateMetadata()\` for SEO and social previews.`);
  }

  // 9. Async page with no sibling loading.tsx (no streaming fallback)
  if (isPage && RE.asyncDefault.test(src)) {
    const sibling = join(dirname(file), "loading.tsx");
    const siblingJs = join(dirname(file), "loading.jsx");
    if (!existsSync(sibling) && !existsSync(siblingJs)) {
      add(rel, firstMatchLine(src, RE.asyncDefault), "INFO", "no-streaming-fallback",
        `Async page with no \`loading.tsx\` — users wait for the whole tree instead of seeing a streamed shell.`,
        `Add a \`loading.tsx\` beside this page, or wrap slow parts in \`<Suspense>\`.`);
    }
  }

  // 10. dangerouslySetInnerHTML
  for (const ln of allMatchLines(src, RE.dangerHtml)) {
    add(rel, ln, "WARN", "dangerous-html",
      `dangerouslySetInnerHTML — XSS risk if the value isn't sanitized.`,
      `Sanitize the HTML server-side, or render structured content instead.`);
  }

  // 11. Legacy next/head — does nothing in the App Router
  if (RE.legacyHead.test(src)) {
    add(rel, firstMatchLine(src, RE.legacyHead), "ERROR", "legacy-next-head",
      `\`next/head\` is a no-op in the App Router — tags rendered through it never reach the document <head>.`,
      `Move those tags into the \`metadata\` export (or \`generateMetadata\`).`);
  }

  // 12. next/legacy/image — opts out of modern image optimization
  if (RE.legacyImage.test(src)) {
    add(rel, firstMatchLine(src, RE.legacyImage), "WARN", "legacy-next-image",
      `\`next/legacy/image\` keeps the old layout-shift-prone behavior.`,
      `Migrate to \`next/image\` and set \`sizes\` (or \`fill\`) for responsive, CLS-safe images.`);
  }

  // 13. Oversized client component
  const lineCount = src.split("\n").length;
  if (isClient && lineCount > 250) {
    add(rel, 1, "INFO", "large-client-component",
      `${lineCount}-line Client Component ships entirely to the browser.`,
      `Split it: keep static markup in a Server Component, isolate the interactive island.`);
  }
}

// ── run ──────────────────────────────────────────────────────────────────────
const files = walk(appDir);
for (const f of files) {
  let src;
  try {
    src = readFileSync(f, "utf8");
  } catch {
    continue;
  }
  analyze(f, src);
}

// ── report ───────────────────────────────────────────────────────────────────
const order = { ERROR: 0, WARN: 1, INFO: 2 };
findings.sort((a, b) => order[a.severity] - order[b.severity] || a.file.localeCompare(b.file) || a.line - b.line);

const counts = { ERROR: 0, WARN: 0, INFO: 0 };
for (const f of findings) counts[f.severity]++;

if (asJson) {
  console.log(JSON.stringify({ appDir: relative(projectRoot, appDir) || "app", filesScanned: files.length, counts, findings }, null, 2));
  process.exit(counts.ERROR > 0 ? 1 : 0);
}

const C = process.stdout.isTTY
  ? { ERROR: "\x1b[31m", WARN: "\x1b[33m", INFO: "\x1b[36m", dim: "\x1b[2m", bold: "\x1b[1m", reset: "\x1b[0m" }
  : { ERROR: "", WARN: "", INFO: "", dim: "", bold: "", reset: "" };

console.log(`\n${C.bold}Next.js App Router audit${C.reset} ${C.dim}— ${files.length} files in ${relative(projectRoot, appDir) || "app"}/${C.reset}\n`);

if (!findings.length) {
  console.log(`${C.INFO}No issues found. Clean App Router code.${C.reset}\n`);
} else {
  for (const f of findings) {
    console.log(`${C[f.severity]}${f.severity}${C.reset} ${C.dim}${f.rule}${C.reset}  ${f.file}:${f.line}`);
    console.log(`  ${f.message}`);
    console.log(`  ${C.dim}fix:${C.reset} ${f.fix}\n`);
  }
}

// crude score: 100 minus weighted penalties, floored at 0
const score = Math.max(0, 100 - counts.ERROR * 15 - counts.WARN * 5 - counts.INFO * 1);
console.log(
  `${C.bold}Summary${C.reset}  ${C.ERROR}${counts.ERROR} error${C.reset}  ${C.WARN}${counts.WARN} warn${C.reset}  ${C.INFO}${counts.INFO} info${C.reset}   ${C.bold}score ${score}/100${C.reset}\n`,
);

process.exit(counts.ERROR > 0 ? 1 : 0);
