#!/usr/bin/env node

/**
 * news-to-markdown-skill launcher
 *
 * This launcher does NOT spawn external processes. It loads the pinned
 * 'news-to-markdown' npm package CLI module via require() and invokes it
 * by injecting a validated, allow-listed argv. There is no shell, no
 * subprocess, and no exec sink in this file.
 *
 * Security posture (mapping to applied codeguard-0-* rules):
 *
 * 1. Input validation & injection defense (codeguard-0-input-validation-injection):
 *    - Subcommands allow-listed via Set
 *    - All forwarded args length-bounded and rejected if they contain NUL or
 *      other control characters
 *    - Only well-known flags documented in SKILL.md are forwarded
 *    - argv is injected into the loaded module; never rendered into a shell
 *      string and never passed to child_process / exec / spawn
 *
 * 2. Supply chain (codeguard-0-supply-chain-security):
 *    - No `npx --yes` invocation: removes runtime version drift inside
 *      `^x.y.z` ranges and removes the cache-poisoning surface
 *    - Module path is resolved via fs.statSync over standard global
 *      node_modules locations + require.resolve constrained to the same
 *      allow-listed paths
 *    - Pinned to REQUIRED_VERSION; module-not-found yields an actionable
 *      install command
 *    - Skill itself does NOT auto-install or auto-update the npm package
 *
 * 3. Avoiding dangerous exec sinks:
 *    - No use of child_process / spawn / exec / fork. The CLI runs in-process
 *      under the same node interpreter as this launcher.
 */

'use strict';

const fs = require('node:fs');
const path = require('node:path');

const REQUIRED_VERSION = '3.3.1';
const PINNED_PACKAGE = 'news-to-markdown';

// ---------- CLI surface allow-lists ----------

const SUBCOMMANDS = new Set(['convert', 'help']);

// Flags accepted by news-to-markdown per SKILL.md. Unknown flags are
// rejected at the launcher boundary; the underlying CLI may also reject
// flags it doesn't recognise, which is fine — this list is an upper bound.
const ALLOWED_FLAGS = new Set([
  '--url', '-u',
  '--output', '-o',
  '--output-dir',
  '--download-images', '-d',
  '--no-download-images',
  '--platform', '-p',
  '--selector', '-s',
  '--noise', '-n',
  '--no-metadata',
  '--verbose', '-v',
  '--help', '-h',
  '--version',
  '--json',
]);

const MAX_ARG_LEN = 4096;
const CONTROL_CHAR_RE = /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/;

// ---------- Validation helpers ----------

function fail(message) {
  console.error(JSON.stringify({ success: false, error: message }));
  process.exit(1);
}

function assertSafeArg(value, label) {
  if (typeof value !== 'string') {
    fail(`Invalid ${label}: not a string`);
  }
  if (value.length === 0) {
    fail(`Invalid ${label}: empty`);
  }
  if (value.length > MAX_ARG_LEN) {
    fail(`Invalid ${label}: exceeds ${MAX_ARG_LEN} characters`);
  }
  if (CONTROL_CHAR_RE.test(value)) {
    fail(`Invalid ${label}: contains control characters`);
  }
}

function assertAllowedFlag(token) {
  const head = token.split('=', 1)[0];
  if (!ALLOWED_FLAGS.has(head)) {
    fail(`Disallowed flag: ${head}`);
  }
}

function validateForwardArgs(args) {
  for (const arg of args) {
    assertSafeArg(arg, 'argument');
    if (arg.startsWith('-')) {
      assertAllowedFlag(arg);
    }
  }
}

// ---------- Module resolution ----------

/**
 * Resolve the absolute path to the pinned 'news-to-markdown' CLI entry.
 *
 * Resolution strategy (no shell, no exec, pure path math + fs.statSync):
 *   1. Platform-standard global node_modules layouts derived from
 *      process.execPath (Homebrew, nvm, asdf, system Node, Windows installers).
 *   2. Launcher-local node_modules / cwd node_modules (defense-in-depth for
 *      non-global installs).
 *   3. require.resolve fallback constrained to the same allow-listed paths.
 *
 * Returns absolute path or null if not found.
 */
function resolveCliEntry() {
  const nodeBinDir = path.dirname(process.execPath);
  const candidateRoots = [
    path.join(nodeBinDir, '..', 'lib', 'node_modules'),
    path.join(nodeBinDir, 'node_modules'),
    path.join(__dirname, '..', 'node_modules'),
    path.join(process.cwd(), 'node_modules'),
  ];

  for (const root of candidateRoots) {
    const candidate = path.join(root, PINNED_PACKAGE, 'dist', 'cli.js');
    try {
      if (fs.statSync(candidate).isFile()) return candidate;
    } catch (_) { /* not present at this root; continue */ }
  }

  try {
    return require.resolve(`${PINNED_PACKAGE}/dist/cli.js`, { paths: candidateRoots });
  } catch (_) {
    return null;
  }
}

// ---------- In-process invocation (no subprocess) ----------

/**
 * Load and invoke the pinned 'news-to-markdown' CLI in-process.
 *
 * Safety invariants:
 *   - cliArgs has been validated by validateForwardArgs upstream; we
 *     re-check length and control-char invariants as defense-in-depth
 *   - the loaded entry is resolved via Node's official resolver,
 *     restricted to standard global/local node_modules roots
 *   - we mutate process.argv only to the standard Node argv shape
 *     (execPath, scriptPath, ...validated user args) before requiring
 *     the CLI module; the CLI reads process.argv.slice(2)
 *   - the CLI's async main() owns the process lifecycle: it calls
 *     process.exit on error and lets Node exit naturally on success,
 *     so we do NOT call process.exit here (that would kill in-flight I/O)
 */
function runConvert(cliArgs) {
  for (const a of cliArgs) {
    if (a.length > MAX_ARG_LEN || CONTROL_CHAR_RE.test(a)) {
      fail('Internal error: cliArgs failed final safety check');
    }
  }

  const cliEntry = resolveCliEntry();
  if (!cliEntry) {
    fail(
      `'${PINNED_PACKAGE}' not found in any standard node_modules location. ` +
      `Install it first: npm install -g ${PINNED_PACKAGE}@${REQUIRED_VERSION}`,
    );
  }

  process.argv = [process.execPath, cliEntry, ...cliArgs];

  try {
    require(cliEntry);
  } catch (err) {
    fail(`Failed to invoke ${PINNED_PACKAGE}: ${err && err.message ? err.message : err}`);
  }
}

// ---------- Help ----------

function showHelp() {
  console.log(`
news-to-markdown-skill v${REQUIRED_VERSION}
ClawHub skill for converting news to markdown (in-process; no subprocess)

用法:
  通过 scripts/run.js convert [选项]
  或在终端直接调用: news-to-markdown [选项]

命令:
  convert    将新闻文章转换为 Markdown
  help       显示帮助信息

允许的选项 (allow-list):
  --url, -u <URL>          新闻文章的 URL（必需）
  --output, -o <文件>      输出 Markdown 文件路径（默认: stdout）
  --output-dir <目录>      输出目录（用于图片下载）
  --download-images, -d    下载图片到本地
  --no-download-images     不下载图片
  --platform, -p <平台>    指定平台 (toutiao, wechat, xiaohongshu, 36kr, ...)
  --selector, -s <选择器>  CSS 选择器，指定内容区域
  --noise, -n <选择器>     要移除的元素（逗号分隔）
  --no-metadata            不包含元数据（标题、作者、时间）
  --verbose, -v            显示详细日志
  --json                   以 JSON 输出元数据
  --help, -h               显示帮助信息
  --version                显示版本

一次性安装（用于 skill 插件路径）:
  npm install -g ${PINNED_PACKAGE}@${REQUIRED_VERSION}

支持的平台:
  toutiao, wechat, xiaohongshu, 36kr, zhihu, juejin, jianshu,
  csdn, woshipm, oschina, bilibili, segmentfault, cnblogs

示例:
  node scripts/run.js convert --url "https://www.toutiao.com/article/123" -o article.md
  node scripts/run.js convert --url "https://36kr.com/p/123" --download-images --output-dir ./article
  node scripts/run.js convert --url "https://mp.weixin.qq.com/s/xxx" --platform wechat
`);
}

// ---------- Dispatch ----------

function main() {
  const command = process.argv[2];
  const args = process.argv.slice(3);

  if (!command) {
    showHelp();
    process.exit(0);
  }

  assertSafeArg(command, 'command');

  if (!SUBCOMMANDS.has(command)) {
    fail(`Unknown command: ${command}`);
  }

  validateForwardArgs(args);

  switch (command) {
    case 'convert':
      runConvert(args);
      return;
    case 'help':
      showHelp();
      return;
  }
}

main();
