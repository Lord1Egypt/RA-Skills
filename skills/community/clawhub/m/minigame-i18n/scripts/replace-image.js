#!/usr/bin/env node
/**
 * 图片替换脚本 v2
 * 
 * 基于 image_translations.json，将翻译后的图片复制到项目中
 * 替换原始图片或按语言目录组织。
 * 
 * v2 改进：
 * 1. 智能搜索 MCP 翻译后的图片（支持多种目录结构）
 * 2. 替换前后校验图片文件完整性（文件大小 > 0）
 * 3. 生成详细替换报告
 * 
 * 使用方法：
 *   node replace-image.js --project <projectRoot> [--mode replace|copy] [--dry-run]
 * 
 * 参数：
 *   --project      项目根目录路径
 *   --mode         替换模式：replace（直接替换原图）/ copy（复制到语言目录）
 *   --dry-run      预览模式
 *   --target-lang  目标语言代码
 *   --backup       替换前备份原始图片（默认开启）
 */

const fs = require('fs');
const path = require('path');

// ============================================================
// 配置
// ============================================================

const args = parseArgs(process.argv.slice(2));
const PROJECT_ROOT = args.project || process.cwd();
const MODE = args.mode || 'replace'; // replace | copy
const DRY_RUN = args['dry-run'] || false;
const TARGET_LANG = args['target-lang'] || 'en';
const BACKUP = args.backup !== false;

const I18N_DIR = path.join(PROJECT_ROOT, 'i18n');
const IMAGE_TRANSLATIONS_FILE = path.join(I18N_DIR, 'image_translations.json');
const TRANSLATED_ASSETS_DIR = path.join(I18N_DIR, 'assets', TARGET_LANG);
const BACKUP_DIR = path.join(I18N_DIR, 'backups', new Date().toISOString().replace(/[:.]/g, '-'), 'images');

// ============================================================
// 翻译图片查找
// ============================================================

/**
 * 智能查找 MCP 翻译后的图片路径
 * MCP 翻译结果的目录结构为：
 *   i18n/assets/{lang}/{上传时路径前缀}/files/{项目相对路径}/{文件名}
 * 或：
 *   i18n/assets/{lang}/{项目相对路径}/{文件名}
 * 
 * 我们需要在多个候选路径中查找
 */
function findTranslatedImage(sourceFile, targetFile) {
  // 候选路径列表，按优先级排序
  const candidates = [];

  // 1. 如果 targetFile 已经明确指定，优先使用
  if (targetFile) {
    candidates.push(path.join(PROJECT_ROOT, targetFile));
  }

  // 2. 标准目录：i18n/assets/{lang}/{sourceFile}
  candidates.push(path.join(TRANSLATED_ASSETS_DIR, sourceFile));

  // 3. MCP 翻译输出格式：可能带有 upload 前缀
  //    例如 i18n/assets/en/upload_image_xxx/files/assets/img/btn.png
  //    我们需要递归搜索同名文件
  const sourceBasename = path.basename(sourceFile);
  const sourceDir = path.dirname(sourceFile);

  // 4. 在 translated_output 目录中查找（MCP 下载解压的目录）
  const translatedOutputDir = path.join(I18N_DIR, 'translated_output', TARGET_LANG);
  if (fs.existsSync(translatedOutputDir)) {
    const found = findFileRecursive(translatedOutputDir, sourceBasename, sourceDir);
    if (found) candidates.push(found);
  }

  // 5. 在 assets/{lang} 中递归搜索同名文件
  if (fs.existsSync(TRANSLATED_ASSETS_DIR)) {
    const found = findFileRecursive(TRANSLATED_ASSETS_DIR, sourceBasename, sourceDir);
    if (found) candidates.push(found);
  }

  // 返回第一个存在的路径
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      const stat = fs.statSync(candidate);
      if (stat.size > 0) {
        return candidate;
      }
    }
  }

  return null;
}

/**
 * 在目录中递归查找文件
 * 优先匹配路径最相似的（考虑 sourceDir 的后缀匹配）
 */
function findFileRecursive(dir, filename, sourceDir) {
  const results = [];

  function walk(currentDir) {
    try {
      const items = fs.readdirSync(currentDir);
      for (const item of items) {
        const fullPath = path.join(currentDir, item);
        try {
          const stat = fs.statSync(fullPath);
          if (stat.isDirectory()) {
            walk(fullPath);
          } else if (item === filename) {
            results.push(fullPath);
          }
        } catch (e) { /* skip inaccessible */ }
      }
    } catch (e) { /* skip inaccessible */ }
  }

  walk(dir);

  if (results.length === 0) return null;
  if (results.length === 1) return results[0];

  // 多个匹配时，选择路径后缀最匹配 sourceDir 的
  const sourceDirParts = sourceDir.split(path.sep).filter(Boolean);
  let bestMatch = results[0];
  let bestScore = 0;

  for (const result of results) {
    const relPath = path.dirname(result);
    const parts = relPath.split(path.sep).filter(Boolean);
    let score = 0;
    // 从后往前比较路径片段
    for (let i = 1; i <= Math.min(sourceDirParts.length, parts.length); i++) {
      if (sourceDirParts[sourceDirParts.length - i] === parts[parts.length - i]) {
        score++;
      } else {
        break;
      }
    }
    if (score > bestScore) {
      bestScore = score;
      bestMatch = result;
    }
  }

  return bestMatch;
}

// ============================================================
// 主流程
// ============================================================

async function main() {
  console.log('🖼️  图片替换工具 v2');
  console.log(`   项目路径: ${PROJECT_ROOT}`);
  console.log(`   目标语言: ${TARGET_LANG}`);
  console.log(`   替换模式: ${MODE === 'replace' ? '直接替换' : '复制到语言目录'}`);
  console.log(`   预览模式: ${DRY_RUN ? '是' : '否'}`);
  console.log('');

  // 1. 读取图片翻译表
  if (!fs.existsSync(IMAGE_TRANSLATIONS_FILE)) {
    console.error(`❌ 图片翻译表不存在: ${IMAGE_TRANSLATIONS_FILE}`);
    process.exit(1);
  }
  const imageTranslations = JSON.parse(fs.readFileSync(IMAGE_TRANSLATIONS_FILE, 'utf8'));
  const entries = imageTranslations.translations.filter(e => e.status === 'completed');
  console.log(`✅ 读取图片翻译表: ${entries.length} 张已完成翻译`);
  console.log('');

  // 2. 逐张替换
  let totalReplaced = 0;
  let totalFailed = 0;
  const results = [];

  for (const entry of entries) {
    const { sourceFile, targetFile, key } = entry;

    // 智能查找翻译后的图片
    const translatedPath = findTranslatedImage(sourceFile, targetFile);

    // 检查翻译后的图片是否存在
    if (!translatedPath) {
      console.warn(`⚠️  翻译后图片不存在: ${sourceFile}`);
      console.warn(`   已搜索路径:`);
      console.warn(`   - ${targetFile ? path.join(PROJECT_ROOT, targetFile) : '(无指定)'}`);
      console.warn(`   - ${path.join(TRANSLATED_ASSETS_DIR, sourceFile)}`);
      console.warn(`   - ${path.join(I18N_DIR, 'translated_output', TARGET_LANG)} (递归)`);
      totalFailed++;
      results.push({ key, sourceFile, status: 'missing_target', searchPaths: [
        targetFile, path.join('i18n/assets', TARGET_LANG, sourceFile)
      ]});
      continue;
    }

    const sourcePath = path.join(PROJECT_ROOT, sourceFile);

    if (MODE === 'replace') {
      // 直接替换模式
      if (!fs.existsSync(sourcePath)) {
        console.warn(`⚠️  源图片不存在: ${sourceFile}`);
        totalFailed++;
        results.push({ key, sourceFile, status: 'missing_source' });
        continue;
      }

      // 校验翻译后的图片文件大小
      const translatedStat = fs.statSync(translatedPath);
      if (translatedStat.size === 0) {
        console.warn(`⚠️  翻译后图片为空文件: ${translatedPath}`);
        totalFailed++;
        results.push({ key, sourceFile, status: 'empty_target' });
        continue;
      }

      if (BACKUP && !DRY_RUN) {
        backupFile(sourcePath, sourceFile);
      }

      if (!DRY_RUN) {
        fs.copyFileSync(translatedPath, sourcePath);

        // 替换后校验：确认文件已正确写入
        const replacedStat = fs.statSync(sourcePath);
        if (replacedStat.size === 0) {
          console.error(`❌ 替换后文件为空，回滚: ${sourceFile}`);
          // 从备份恢复
          const backupPath = path.join(BACKUP_DIR, sourceFile);
          if (fs.existsSync(backupPath)) {
            fs.copyFileSync(backupPath, sourcePath);
          }
          totalFailed++;
          results.push({ key, sourceFile, status: 'replace_failed', reason: '替换后文件为空' });
          continue;
        }

        console.log(`✅ 替换: ${sourceFile} (${(translatedStat.size / 1024).toFixed(1)} KB ← ${translatedPath})`);
      } else {
        console.log(`🔍 可替换: ${sourceFile}（预览模式，来源: ${translatedPath}）`);
      }

      totalReplaced++;
      results.push({ key, sourceFile, status: 'replaced', translatedFrom: translatedPath });
    } else {
      // 复制到语言目录模式
      const langDir = path.join(PROJECT_ROOT, `assets_${TARGET_LANG}`);
      const targetPath = path.join(langDir, sourceFile);
      const targetDir = path.dirname(targetPath);

      if (!DRY_RUN) {
        fs.mkdirSync(targetDir, { recursive: true });
        fs.copyFileSync(translatedPath, targetPath);
        console.log(`✅ 复制: ${sourceFile} → assets_${TARGET_LANG}/${sourceFile}`);
      } else {
        console.log(`🔍 可复制: ${sourceFile}（预览模式）`);
      }

      totalReplaced++;
      results.push({ key, sourceFile, status: 'copied', targetPath });
    }
  }

  // 3. 输出摘要
  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`📊 图片替换完成`);
  console.log(`   成功: ${totalReplaced} 张`);
  console.log(`   失败: ${totalFailed} 张`);
  if (BACKUP && !DRY_RUN && MODE === 'replace') {
    console.log(`   备份: ${BACKUP_DIR}`);
  }
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

  // 4. 保存替换报告
  if (!DRY_RUN) {
    const reportPath = path.join(I18N_DIR, 'image_replace_report.json');
    fs.writeFileSync(reportPath, JSON.stringify({
      timestamp: new Date().toISOString(),
      targetLanguage: TARGET_LANG,
      mode: MODE,
      totalReplaced,
      totalFailed,
      results
    }, null, 2), 'utf8');
    console.log(`📄 替换报告: ${reportPath}`);
  }

  if (totalFailed > 0) {
    process.exit(1);
  }
}

// ============================================================
// 工具函数
// ============================================================

function backupFile(fullPath, relativePath) {
  const backupPath = path.join(BACKUP_DIR, relativePath);
  const backupDir = path.dirname(backupPath);
  fs.mkdirSync(backupDir, { recursive: true });
  fs.copyFileSync(fullPath, backupPath);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].substring(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

// ============================================================
// 执行
// ============================================================

main().catch(err => {
  console.error('❌ 图片替换失败:', err.message);
  process.exit(1);
});
