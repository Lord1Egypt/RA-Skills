#!/usr/bin/env node
/**
 * scan-legacy-reviews.js
 *
 * 扫描指定目录，识别可能的历史雅思阅读复盘文件，输出结构化清单。
 * Buddy 可基于该清单逐篇调用 skill 生成 JSON。
 *
 * 用法：
 *   node scan-legacy-reviews.js                       # 🔍 自动发现模式（推荐给老婆用）
 *   node scan-legacy-reviews.js --auto                # 同上，显式 auto
 *   node scan-legacy-reviews.js <目录>                # 扫描指定目录（顶层）
 *   node scan-legacy-reviews.js <目录> --deep         # 递归子目录
 *   node scan-legacy-reviews.js <目录> --out=a.json   # 写入文件
 *
 * 自动发现模式（--auto / 不传目录）：
 *   扫描常见位置：当前目录 / ~/Documents / ~/Desktop / ~/Downloads / iCloud
 *   输出各目录的候选命中数量，按命中数倒序，方便 buddy 推荐给用户确认。
 *   只做快速计数，不做详细分组（避免误扫大目录耗时）。
 *
 * 识别规则（按命中一项即算候选）：
 *   - 文件名含"剑X"、"CambridgeX"、"TestX"、"PassageX"、"Reading"、"复盘"、"阅读"、"雅思"、"IELTS"
 *   - 扩展名：.html .htm .md .txt .docx .pdf .png .jpg .jpeg
 *
 * 输出字段（精确扫描模式）：
 *   - path: 绝对路径
 *   - name: 文件名
 *   - ext:  扩展名（小写）
 *   - size: 字节大小
 *   - mtime: 最后修改时间 ISO
 *   - hints: 正则识别到的篇目提示 { book, test, passage, title }
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const args = process.argv.slice(2);
const autoMode = args.length === 0 || args.includes('--auto');
const deep = args.includes('--deep');
const outArg = args.find((a) => a.startsWith('--out='));
const outPath = outArg ? outArg.slice('--out='.length) : null;

// 精确扫描模式下的根目录
const positionalArgs = args.filter((a) => !a.startsWith('--'));
const rootDir = !autoMode && positionalArgs[0] ? path.resolve(positionalArgs[0]) : null;

const CANDIDATE_EXTS = new Set([
  '.html', '.htm', '.md', '.txt', '.docx', '.pdf',
  '.png', '.jpg', '.jpeg', '.webp',
]);

const KEYWORDS = [
  /剑\s*\d+/,
  /cambridge\s*\d+/i,
  /test\s*\d/i,
  /passage\s*\d/i,
  /reading/i,
  /复盘/,
  /阅读/,
  /错题/,
  /雅思/,
  /ielts/i,
];

const IGNORE_DIRS = new Set([
  'node_modules', '.git', '.workbuddy', '.DS_Store',
  'backup_old_v1', 'history-json', 'site', 'scripts',
  'skills', 'ielts-reading-review', 'ielts-server-sync',
  '移植包', 'cloudfunctions', 'server',
]);

/**
 * 从文件名中提取篇目提示
 */
function extractHints(filename) {
  const hints = {};
  const base = filename.replace(/\.[^.]+$/, '');

  const bookMatch = base.match(/剑\s*(\d+)|cambridge\s*(\d+)|c(\d+)/i);
  if (bookMatch) hints.book = parseInt(bookMatch[1] || bookMatch[2] || bookMatch[3], 10);

  const testMatch = base.match(/test\s*(\d)|t(\d)/i);
  if (testMatch) hints.test = parseInt(testMatch[1] || testMatch[2], 10);

  const passageMatch = base.match(/passage\s*(\d)|p(\d)/i);
  if (passageMatch) hints.passage = parseInt(passageMatch[1] || passageMatch[2], 10);

  // 剥离出中文主题（最后一段中文，例如 "剑4-Test1-Passage2-鲸鱼感官复盘" → "鲸鱼感官"）
  const themeMatch = base.match(/[-_\s]([\u4e00-\u9fa5]{2,8})(?:复盘|笔记|分析)?$/);
  if (themeMatch) hints.title = themeMatch[1];

  return hints;
}

function isCandidate(filename) {
  const ext = path.extname(filename).toLowerCase();
  if (!CANDIDATE_EXTS.has(ext)) return false;
  return KEYWORDS.some((re) => re.test(filename));
}

function scanDir(dir, results, currentDepth = 0) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (err) {
    console.error(`⚠️ 无法读取 ${dir}: ${err.message}`);
    return;
  }

  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      if (IGNORE_DIRS.has(entry.name)) continue;
      if (deep || currentDepth === 0) {
        scanDir(fullPath, results, currentDepth + 1);
      }
      continue;
    }

    if (!entry.isFile()) continue;
    if (!isCandidate(entry.name)) continue;

    try {
      const stat = fs.statSync(fullPath);
      results.push({
        path: fullPath,
        name: entry.name,
        ext: path.extname(entry.name).toLowerCase(),
        size: stat.size,
        mtime: stat.mtime.toISOString(),
        hints: extractHints(entry.name),
      });
    } catch (err) {
      console.error(`⚠️ 跳过 ${fullPath}: ${err.message}`);
    }
  }
}

function groupByPassage(items) {
  const groups = new Map();
  for (const it of items) {
    const { book, test, passage } = it.hints;
    const key = book && test && passage
      ? `C${book}-T${test}-P${passage}`
      : '__unknown__';
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(it);
  }
  return groups;
}

// ---- auto discovery ----

/**
 * 快速统计目录命中数（浅扫顶层 + 一层子目录），用于 auto 模式推荐候选
 */
function quickCount(dir, maxDepth = 2, currentDepth = 0) {
  let hits = [];
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (err) {
    return hits;
  }

  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      if (IGNORE_DIRS.has(entry.name)) continue;
      if (currentDepth < maxDepth) {
        hits = hits.concat(quickCount(fullPath, maxDepth, currentDepth + 1));
      }
      continue;
    }

    if (!entry.isFile()) continue;
    if (!isCandidate(entry.name)) continue;

    try {
      const stat = fs.statSync(fullPath);
      hits.push({
        path: fullPath,
        name: entry.name,
        mtime: stat.mtime.toISOString(),
      });
    } catch (err) { /* skip */ }
  }
  return hits;
}

function runAutoDiscovery() {
  const home = os.homedir();
  const cwd = process.cwd();

  // 候选位置（去重）
  const candidateDirsRaw = [
    cwd,
    path.join(home, 'Documents'),
    path.join(home, 'Desktop'),
    path.join(home, 'Downloads'),
    path.join(home, 'Library/Mobile Documents/com~apple~CloudDocs'), // iCloud
    path.join(home, 'Documents/个人'),
    path.join(home, 'Documents/个人/WorkBuddy'),
    path.join(home, 'WorkBuddy'),
    path.join(home, 'WorkBuddy/Claw'),
  ];
  const seen = new Set();
  let candidateDirs = candidateDirsRaw.filter((d) => {
    if (seen.has(d)) return false;
    seen.add(d);
    return fs.existsSync(d);
  });

  // 扩展候选：从每个候选根目录，把"直接子目录中带雅思/IELTS/reading/复盘/阅读"关键词的也加进来
  const DIR_KEYWORDS = [/雅思/, /ielts/i, /reading/i, /复盘/, /阅读/, /ielts/i];
  const extendedDirs = new Set(candidateDirs);
  for (const dir of candidateDirs) {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        if (!entry.isDirectory() || entry.name.startsWith('.')) continue;
        if (IGNORE_DIRS.has(entry.name)) continue;
        if (DIR_KEYWORDS.some((re) => re.test(entry.name))) {
          extendedDirs.add(path.join(dir, entry.name));
        }
      }
    } catch (err) { /* skip */ }
  }
  candidateDirs = Array.from(extendedDirs);

  const discoveries = [];
  for (const dir of candidateDirs) {
    const hits = quickCount(dir, 3);
    if (hits.length === 0) continue;
    // 取最近一次修改时间作为活跃度信号
    hits.sort((a, b) => b.mtime.localeCompare(a.mtime));
    discoveries.push({
      dir,
      hitCount: hits.length,
      latestMtime: hits[0].mtime,
      sampleFiles: hits.slice(0, 5).map((h) => h.name),
    });
  }

  // 去除"父目录"重复：如果 A 是 B 的父目录且子目录命中数占父目录 ≥ 80%，丢弃父目录
  const filtered = discoveries.filter((d) => {
    return !discoveries.some((other) => {
      if (other.dir === d.dir) return false;
      if (!other.dir.startsWith(d.dir + path.sep)) return false;
      return other.hitCount / d.hitCount >= 0.8;
    });
  });

  // 按命中数倒序，相同时按最新修改时间
  filtered.sort((a, b) => {
    if (b.hitCount !== a.hitCount) return b.hitCount - a.hitCount;
    return b.latestMtime.localeCompare(a.latestMtime);
  });

  return {
    mode: 'auto-discovery',
    scannedAt: new Date().toISOString(),
    scannedDirs: candidateDirs,
    discoveries: filtered,
    recommended: filtered[0] ? filtered[0].dir : null,
  };
}

// ---- main ----
if (autoMode) {
  const result = runAutoDiscovery();
  if (outPath) {
    fs.writeFileSync(outPath, JSON.stringify(result, null, 2), 'utf8');
    console.log(`✅ 自动发现完成，写入 ${outPath}`);
    console.log(`   找到 ${result.discoveries.length} 个候选目录`);
    if (result.recommended) {
      console.log(`   🎯 推荐目录：${result.recommended}（${result.discoveries[0].hitCount} 个候选文件）`);
    }
  } else {
    console.log(JSON.stringify(result, null, 2));
  }
  process.exit(0);
}

if (!fs.existsSync(rootDir)) {
  console.error(`❌ 目录不存在：${rootDir}`);
  process.exit(1);
}

const results = [];
scanDir(rootDir, results);

// 按修改时间倒序，便于 buddy 优先处理最新的
results.sort((a, b) => b.mtime.localeCompare(a.mtime));

const groups = groupByPassage(results);
const grouped = [];
for (const [key, files] of groups.entries()) {
  grouped.push({
    passage: key,
    fileCount: files.length,
    files,
  });
}
// 已识别篇目在前，未识别在后
grouped.sort((a, b) => {
  if (a.passage === '__unknown__') return 1;
  if (b.passage === '__unknown__') return -1;
  return a.passage.localeCompare(b.passage);
});

const output = {
  mode: 'scan',
  scannedAt: new Date().toISOString(),
  rootDir,
  deep,
  totalFiles: results.length,
  identifiedPassages: grouped.filter((g) => g.passage !== '__unknown__').length,
  groups: grouped,
};

if (outPath) {
  fs.writeFileSync(outPath, JSON.stringify(output, null, 2), 'utf8');
  console.log(`✅ 已写入 ${outPath}（共 ${results.length} 个候选文件，${output.identifiedPassages} 篇可识别）`);
} else {
  console.log(JSON.stringify(output, null, 2));
}
