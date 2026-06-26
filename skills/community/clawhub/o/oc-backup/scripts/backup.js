#!/usr/bin/env node

/**
 * OpenClaw 关键文件备份脚本
 * 
 * 功能：备份 OpenClaw 运行所需的关键配置文件和用户数据
 * 版本：1.0.0
 * 
 * 支持的备份类型：
 * - full: 全量备份
 * - system: 系统配置
 * - workspace: 核心文件
 * - skills: 技能目录
 * - memory: 记忆数据
 * - cron: 定时任务
 * - devices: 设备配置
 */

const fs = require('fs');
const fse = require('fs-extra');
const path = require('path');
const os = require('os');
const tar = require('tar');
const { Command } = require('commander');
const dayjs = require('dayjs');

// ============================================================================
// 常量定义
// ============================================================================

const VERSION = '1.1.0';
const BACKUP_ROOT_NAME = 'openclaw-backup';

// 退出码
const EXIT_CODES = {
  SUCCESS: 0,
  PARAM_ERROR: 1,
  PERMISSION_ERROR: 2,
  DISK_SPACE_ERROR: 3,
  BACKUP_ERROR: 4
};

// 错误解决方案
const ERROR_SOLUTIONS = {
  'E001': '请检查命令行参数格式，使用 --help 查看帮助',
  'E002': '请确保对 ~/.openclaw/ 和输出目录有读写权限',
  'E003': '磁盘空间不足，请清理后重试',
  'E004': '文件被占用或已损坏，请检查文件状态',
  'E005': '临时目录权限不足，请检查 ~/.openclaw/tmp/ 权限',
  'E006': '无法写入输出目录，请检查权限或更换目录'
};

// 文件类别定义
const FILE_CATEGORIES = {
  system: {
    name: '系统配置',
    baseDir: '.openclaw',
    targetDir: 'system',
    files: [
      { name: 'openclaw.json', sensitive: false },
      { name: '.env', sensitive: true },
      { name: 'exec-approvals.json', sensitive: false }
    ]
  },
  workspace: {
    name: '核心文件',
    baseDir: '.openclaw/workspace',
    targetDir: 'workspace',
    files: [
      { name: 'AGENTS.md', sensitive: false },
      { name: 'SOUL.md', sensitive: false },
      { name: 'USER.md', sensitive: false },
      { name: 'IDENTITY.md', sensitive: false },
      { name: 'TOOLS.md', sensitive: false },
      { name: 'HEARTBEAT.md', sensitive: false },
      { name: 'MEMORY.md', sensitive: false }
    ]
  },
  skills: {
    name: '技能目录',
    baseDir: '.openclaw/workspace/skills',
    targetDir: 'skills',
    isDirectory: true
  },
  memory: {
    name: '记忆数据',
    baseDir: '.openclaw/memory',
    targetDir: 'memory',
    isDirectory: true
  },
  cron: {
    name: '定时任务',
    baseDir: '.openclaw/cron',
    targetDir: 'cron',
    isDirectory: true
  },
  devices: {
    name: '设备配置',
    baseDir: '.openclaw/devices',
    targetDir: 'devices',
    isDirectory: true
  }
};

// ============================================================================
// 工具函数
// ============================================================================

/**
 * 获取 OpenClaw 根目录
 */
function getOpenClawRoot() {
  return path.join(os.homedir(), '.openclaw');
}

/**
 * 获取默认备份输出目录
 */
function getDefaultOutputDir() {
  return path.join(os.homedir(), 'backups', 'openclaw');
}

/**
 * 格式化文件大小
 */
function formatSize(bytes) {
  if (bytes === 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${units[i]}`;
}

/**
 * 获取文件/目录大小
 */
function getFileSize(filePath) {
  try {
    const stats = fs.statSync(filePath);
    if (stats.isDirectory()) {
      let totalSize = 0;
      const files = fs.readdirSync(filePath);
      for (const file of files) {
        totalSize += getFileSize(path.join(filePath, file));
      }
      return totalSize;
    }
    return stats.size;
  } catch {
    return 0;
  }
}

/**
 * 确保目录存在
 */
async function ensureDir(dirPath) {
  try {
    await fse.ensureDir(dirPath);
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * 检查磁盘空间（简单估算）
 */
function checkDiskSpace(outputDir, estimatedSize) {
  try {
    const stats = fs.statSync(outputDir);
    return true;
  } catch {
    return true; // 目录不存在时会创建，暂时返回 true
  }
}

/**
 * 获取主机名
 */
function getHostname() {
  return os.hostname();
}

/**
 * 获取平台信息
 */
function getPlatform() {
  return process.platform;
}

/**
 * 清理旧备份
 * @param {string} outputDir - 备份输出目录
 * @param {number} retainDays - 保留天数
 * @param {boolean} dryRun - 预览模式
 * @returns {Object} 清理结果
 */
async function cleanOldBackups(outputDir, retainDays, dryRun = false) {
  const result = {
    deleted: [],
    kept: [],
    errors: []
  };

  if (!fs.existsSync(outputDir)) {
    return result;
  }

  const now = Date.now();
  const cutoffTime = now - (retainDays * 24 * 60 * 60 * 1000);

  // 读取所有备份目录
  const entries = fs.readdirSync(outputDir, { withFileTypes: true });
  const backupDirs = entries
    .filter(e => e.isDirectory() && e.name.startsWith('openclaw-backup-'))
    .map(e => {
      const fullPath = path.join(outputDir, e.name);
      const stat = fs.statSync(fullPath);
      return {
        name: e.name,
        path: fullPath,
        mtime: stat.mtime.getTime(),
        mtimeStr: dayjs(stat.mtime).format('YYYY-MM-DD HH:mm:ss')
      };
    })
    .sort((a, b) => b.mtime - a.mtime); // 按时间降序

  for (const dir of backupDirs) {
    if (dir.mtime < cutoffTime) {
      // 需要删除
      if (dryRun) {
        result.deleted.push({
          name: dir.name,
          path: dir.path,
          mtime: dir.mtimeStr,
          dryRun: true
        });
      } else {
        try {
          await fse.remove(dir.path);
          result.deleted.push({
            name: dir.name,
            path: dir.path,
            mtime: dir.mtimeStr
          });
        } catch (error) {
          result.errors.push({
            name: dir.name,
            error: error.message
          });
        }
      }
    } else {
      // 保留
      result.kept.push({
        name: dir.name,
        mtime: dir.mtimeStr
      });
    }
  }

  return result;
}

/**
 * 输出清理结果
 */
function outputCleanResult(cleanResult, retainDays, dryRun) {
  const prefix = dryRun ? '[预览] ' : '';
  
  console.log(`\n🗑️  ${prefix}备份清理结果\n`);
  console.log(`   保留策略: 最近 ${retainDays} 天`);
  console.log(`   保留数量: ${cleanResult.kept.length} 个备份`);
  console.log(`   删除数量: ${cleanResult.deleted.length} 个备份`);
  
  if (cleanResult.kept.length > 0) {
    console.log(`\n✅ 保留的备份:`);
    for (const dir of cleanResult.kept.slice(0, 5)) {
      console.log(`   ${dir.name} (${dir.mtime})`);
    }
    if (cleanResult.kept.length > 5) {
      console.log(`   ... 还有 ${cleanResult.kept.length - 5} 个备份`);
    }
  }
  
  if (cleanResult.deleted.length > 0) {
    console.log(`\n🗑️  ${prefix}将删除的备份:`);
    for (const dir of cleanResult.deleted.slice(0, 5)) {
      const dryRunTag = dir.dryRun ? ' [预览]' : '';
      console.log(`   ${dir.name} (${dir.mtime})${dryRunTag}`);
    }
    if (cleanResult.deleted.length > 5) {
      console.log(`   ... 还有 ${cleanResult.deleted.length - 5} 个备份`);
    }
  }
  
  if (cleanResult.errors.length > 0) {
    console.log(`\n❌ 删除失败的备份:`);
    for (const err of cleanResult.errors) {
      console.log(`   ${err.name}: ${err.error}`);
    }
  }
  
  console.log('');
}

// ============================================================================
// 文件收集模块
// ============================================================================

/**
 * 收集单个类别的文件
 */
async function collectCategoryFiles(category, openclawRoot) {
  const categoryInfo = FILE_CATEGORIES[category];
  if (!categoryInfo) {
    return { files: [], stats: { total: 0, existing: 0, missing: 0, totalSize: 0 } };
  }

  const result = {
    files: [],
    stats: { total: 0, existing: 0, missing: 0, totalSize: 0 }
  };

  const basePath = path.join(os.homedir(), categoryInfo.baseDir);

  if (categoryInfo.isDirectory) {
    // 目录类型
    result.stats.total = 1;
    if (fs.existsSync(basePath)) {
      try {
        const stat = fs.statSync(basePath);
        if (stat.isDirectory()) {
          const size = getFileSize(basePath);
          result.files.push({
            name: category,
            relativePath: `${categoryInfo.targetDir}/`,
            originalPath: basePath,
            size: size,
            status: 'success',
            sensitive: false,
            isDirectory: true
          });
          result.stats.existing = 1;
          result.stats.totalSize += size;
        }
      } catch (error) {
        result.files.push({
          name: category,
          relativePath: `${categoryInfo.targetDir}/`,
          originalPath: basePath,
          size: 0,
          status: 'error',
          reason: error.message,
          sensitive: false,
          isDirectory: true
        });
        result.stats.missing = 1;
      }
    } else {
      result.files.push({
        name: category,
        relativePath: `${categoryInfo.targetDir}/`,
        originalPath: basePath,
        size: 0,
        status: 'skipped',
        reason: 'not_found',
        sensitive: false,
        isDirectory: true
      });
      result.stats.missing = 1;
    }
  } else {
    // 文件类型
    for (const fileInfo of categoryInfo.files) {
      result.stats.total++;
      const filePath = path.join(basePath, fileInfo.name);
      
      if (fs.existsSync(filePath)) {
        try {
          const stat = fs.statSync(filePath);
          if (stat.isFile()) {
            result.files.push({
              name: fileInfo.name,
              relativePath: `${categoryInfo.targetDir}/${fileInfo.name}`,
              originalPath: filePath,
              size: stat.size,
              status: 'success',
              sensitive: fileInfo.sensitive
            });
            result.stats.existing++;
            result.stats.totalSize += stat.size;
          }
        } catch (error) {
          result.files.push({
            name: fileInfo.name,
            relativePath: `${categoryInfo.targetDir}/${fileInfo.name}`,
            originalPath: filePath,
            size: 0,
            status: 'error',
            reason: error.message,
            sensitive: fileInfo.sensitive
          });
          result.stats.missing++;
        }
      } else {
        result.files.push({
          name: fileInfo.name,
          relativePath: `${categoryInfo.targetDir}/${fileInfo.name}`,
          originalPath: filePath,
          size: 0,
          status: 'skipped',
          reason: 'not_found',
          sensitive: fileInfo.sensitive
        });
        result.stats.missing++;
      }
    }
  }

  return result;
}

/**
 * 收集所有需要备份的文件
 */
async function collectFiles(backupTypes, openclawRoot) {
  const result = {
    categories: {},
    stats: { total: 0, existing: 0, missing: 0, totalSize: 0 }
  };

  for (const type of backupTypes) {
    const categoryResult = await collectCategoryFiles(type, openclawRoot);
    result.categories[type] = categoryResult;
    
    result.stats.total += categoryResult.stats.total;
    result.stats.existing += categoryResult.stats.existing;
    result.stats.missing += categoryResult.stats.missing;
    result.stats.totalSize += categoryResult.stats.totalSize;
  }

  return result;
}

// ============================================================================
// 备份执行模块
// ============================================================================

/**
 * 复制文件到临时目录
 */
async function copyFilesToTemp(collectedFiles, tempDir, openclawRoot) {
  const copiedFiles = [];
  const errors = [];

  for (const [category, categoryData] of Object.entries(collectedFiles.categories)) {
    for (const fileInfo of categoryData.files) {
      if (fileInfo.status !== 'success') continue;

      const targetPath = path.join(tempDir, BACKUP_ROOT_NAME, fileInfo.relativePath);

      try {
        if (fileInfo.isDirectory) {
          // 复制目录
          await fse.copy(fileInfo.originalPath, targetPath, {
            overwrite: true,
            errorOnExist: false
          });
        } else {
          // 复制文件
          await fse.ensureDir(path.dirname(targetPath));
          await fse.copy(fileInfo.originalPath, targetPath, {
            overwrite: true,
            errorOnExist: false
          });
        }
        copiedFiles.push({
          path: fileInfo.relativePath,
          size: fileInfo.size,
          checksum: '' // 可选：计算校验和
        });
      } catch (error) {
        errors.push({
          code: 'E004',
          file: fileInfo.originalPath,
          message: error.message
        });
      }
    }
  }

  return { copiedFiles, errors };
}

/**
 * 创建备份清单
 */
function createManifest(backupType, copiedFiles) {
  return {
    version: '1.0.0',
    backupType: backupType,
    createdAt: new Date().toISOString(),
    hostname: getHostname(),
    platform: getPlatform(),
    openclawVersion: VERSION,
    generator: `openclaw-backup v${VERSION}`,
    files: copiedFiles
  };
}

/**
 * 执行压缩
 */
async function compressBackup(tempDir, outputPath) {
  const backupDir = path.join(tempDir, BACKUP_ROOT_NAME);
  
  await tar.create(
    {
      gzip: true,
      file: outputPath,
      cwd: tempDir,
      portable: true
    },
    [BACKUP_ROOT_NAME]
  );

  const stats = fs.statSync(outputPath);
  return stats.size;
}

// ============================================================================
// 清单生成模块
// ============================================================================

/**
 * 生成备份清单 JSON
 */
function generateBackupManifest(backupInfo, collectedFiles, options) {
  const manifest = {
    version: '1.0.0',
    backupType: backupInfo.type,
    timestamp: backupInfo.timestamp,
    hostname: getHostname(),
    platform: getPlatform(),
    openclawVersion: VERSION,
    backupFile: backupInfo.filename,
    backupSize: backupInfo.size,
    backupSizeHuman: formatSize(backupInfo.size),
    duration: backupInfo.duration,
    summary: collectedFiles.stats,
    categories: {},
    errors: backupInfo.errors || [],
    warnings: backupInfo.warnings || []
  };

  // 转换 categories 格式
  for (const [category, data] of Object.entries(collectedFiles.categories)) {
    manifest.categories[category] = {
      count: data.files.length,
      files: data.files.map(f => ({
        relativePath: f.relativePath,
        originalPath: f.originalPath,
        size: f.size,
        status: f.status,
        sensitive: f.sensitive,
        reason: f.reason
      }))
    };
  }

  return manifest;
}

// ============================================================================
// 恢复指导生成模块
// ============================================================================

/**
 * 生成恢复指导书
 */
function generateRecoveryGuide(backupInfo, collectedFiles, outputPath) {
  const timestamp = dayjs(backupInfo.timestamp).format('YYYY-MM-DD HH:mm:ss');
  
  let content = `# OpenClaw 备份恢复指导书

## 1. 备份信息

| 项目 | 值 |
|------|-----|
| 备份时间 | ${timestamp} |
| 备份类型 | ${backupInfo.type} |
| 备份文件 | ${backupInfo.filename} |
| 备份大小 | ${formatSize(backupInfo.size)} |
| 包含文件数 | ${collectedFiles.stats.existing} |
| 备份来源 | ${getHostname()} |
| 平台 | ${getPlatform()} |

## 2. 前置准备

### 2.1 确认环境

确保目标机器已安装：
- Node.js >= 18.0.0
- OpenClaw 已正确安装

### 2.2 创建安全备份

**⚠️ 重要：在恢复之前，请先备份当前配置！**

\`\`\`bash
# 备份当前配置（如果存在）
mv ~/.openclaw ~/.openclaw.backup.$(date +%Y%m%d%H%M%S)
\`\`\`

## 3. 解压备份文件

### 3.1 Windows (PowerShell)

\`\`\`powershell
# 创建临时目录
mkdir -p $env:USERPROFILE\\.openclaw\\temp\\restore
cd $env:USERPROFILE\\.openclaw\\temp\\restore

# 解压备份文件
tar -xzf "${backupInfo.filename}"
\`\`\`

### 3.2 macOS / Linux

\`\`\`bash
# 创建临时目录
mkdir -p ~/.openclaw/temp/restore
cd ~/.openclaw/temp/restore

# 解压备份文件
tar -xzf "${backupInfo.filename}"
\`\`\`

## 4. 恢复各类文件

### 4.1 恢复系统配置

\`\`\`bash
# 复制系统配置文件
cp -r openclaw-backup/system/* ~/.openclaw/

# 或者选择性恢复
cp openclaw-backup/system/openclaw.json ~/.openclaw/
cp openclaw-backup/system/.env ~/.openclaw/
\`\`\`

### 4.2 恢复核心文件

\`\`\`bash
# 复制核心文件
cp -r openclaw-backup/workspace/* ~/.openclaw/workspace/

# 或者选择性恢复
cp openclaw-backup/workspace/SOUL.md ~/.openclaw/workspace/
cp openclaw-backup/workspace/USER.md ~/.openclaw/workspace/
\`\`\`

### 4.3 恢复技能目录

\`\`\`bash
# 复制技能目录
cp -r openclaw-backup/skills ~/.openclaw/workspace/

# 或者恢复单个技能
cp -r openclaw-backup/skills/your-skill-name ~/.openclaw/workspace/skills/
\`\`\`

### 4.4 恢复其他数据

\`\`\`bash
# 恢复记忆数据
cp -r openclaw-backup/memory ~/.openclaw/

# 恢复定时任务
cp -r openclaw-backup/cron ~/.openclaw/

# 恢复设备配置
cp -r openclaw-backup/devices ~/.openclaw/
\`\`\`

## 5. 验证恢复结果

### 5.1 检查文件完整性

\`\`\`bash
# 检查关键文件是否存在
ls -la ~/.openclaw/openclaw.json
ls -la ~/.openclaw/workspace/SOUL.md
ls -la ~/.openclaw/workspace/skills/
\`\`\`

### 5.2 重启 OpenClaw

\`\`\`bash
# 重启 OpenClaw 服务
openclaw gateway restart

# 或者重新加载配置
openclaw gateway reload
\`\`\`

## 6. 故障排除

### 6.1 权限问题

\`\`\`bash
# 修复文件权限
chmod 600 ~/.openclaw/.env
chmod -R u+rw ~/.openclaw/workspace/
\`\`\`

### 6.2 文件不存在

如果恢复时提示文件不存在，请确保：
1. OpenClaw 已正确安装
2. 目标目录结构正确
3. 备份文件完整解压

### 6.3 配置冲突

如果新旧配置有冲突：
1. 使用文本编辑器对比差异
2. 手动合并重要配置
3. 特别注意 .env 中的敏感信息

## 7. 备份内容清单

### 本次备份包含的文件：

`;

  // 添加文件清单
  for (const [category, data] of Object.entries(collectedFiles.categories)) {
    if (data.files.length === 0) continue;
    
    content += `\n#### ${FILE_CATEGORIES[category]?.name || category}\n\n`;
    
    for (const file of data.files) {
      const status = file.status === 'success' ? '✅' : '⏭️';
      const size = file.size > 0 ? ` (${formatSize(file.size)})` : '';
      const note = file.status === 'skipped' ? ' [不存在]' : '';
      content += `${status} \`${file.relativePath}\`${size}${note}\n`;
    }
  }

  content += `
## 8. 注意事项

1. **敏感文件**: .env 文件包含 API 密钥等敏感信息，请妥善保管备份
2. **恢复后验证**: 恢复后请检查 OpenClaw 是否正常运行
3. **定期备份**: 建议定期创建备份以保护您的配置
4. **备份保管**: 备份文件请保存在安全位置

---
*本恢复指导由 OpenClaw Backup v${VERSION} 自动生成*
`;

  return content;
}

// ============================================================================
// 输出模块
// ============================================================================

/**
 * 输出文本格式结果
 */
function outputText(backupInfo, collectedFiles, options) {
  console.log('\n📦 OpenClaw 备份完成!\n');
  console.log('━'.repeat(50));
  
  console.log('\n📊 备份统计:');
  console.log(`   类型: ${backupInfo.type}`);
  console.log(`   耗时: ${backupInfo.duration.toFixed(2)} 秒`);
  console.log(`   文件数: ${collectedFiles.stats.existing} 个成功, ${collectedFiles.stats.missing} 个跳过`);
  console.log(`   总大小: ${formatSize(collectedFiles.stats.totalSize)}`);
  console.log(`   备份文件: ${formatSize(backupInfo.size)}`);
  
  console.log('\n📁 输出文件:');
  console.log(`   ${backupInfo.backupPath}`);
  console.log(`   ${backupInfo.manifestPath}`);
  console.log(`   ${backupInfo.recoveryPath}`);
  
  // 显示各类别详情
  console.log('\n📋 备份详情:');
  for (const [category, data] of Object.entries(collectedFiles.categories)) {
    const categoryName = FILE_CATEGORIES[category]?.name || category;
    const success = data.files.filter(f => f.status === 'success').length;
    const skipped = data.files.filter(f => f.status === 'skipped').length;
    console.log(`   ${categoryName}: ${success} 个成功, ${skipped} 个跳过`);
  }
  
  // 显示跳过的文件
  const skippedFiles = [];
  for (const [category, data] of Object.entries(collectedFiles.categories)) {
    for (const file of data.files) {
      if (file.status === 'skipped') {
        skippedFiles.push(file);
      }
    }
  }
  
  if (skippedFiles.length > 0) {
    console.log('\n⏭️  跳过的文件:');
    for (const file of skippedFiles.slice(0, 5)) {
      console.log(`   ${file.relativePath} (不存在)`);
    }
    if (skippedFiles.length > 5) {
      console.log(`   ... 还有 ${skippedFiles.length - 5} 个文件`);
    }
  }
  
  console.log('\n' + '━'.repeat(50));
  console.log('💡 提示: 请查看 RECOVERY_GUIDE.md 了解恢复步骤\n');
}

/**
 * 输出 JSON 格式结果
 */
function outputJson(backupInfo, collectedFiles, options) {
  const manifest = generateBackupManifest(backupInfo, collectedFiles, options);
  manifest.backupPath = backupInfo.backupPath;
  manifest.manifestPath = backupInfo.manifestPath;
  manifest.recoveryPath = backupInfo.recoveryPath;
  console.log(JSON.stringify(manifest, null, 2));
}

// ============================================================================
// 主函数
// ============================================================================

async function main() {
  const program = new Command();
  
  program
    .name('openclaw-backup')
    .description('OpenClaw 关键文件备份工具')
    .version(VERSION)
    .option('-f, --full', '执行全量备份', false)
    .option('-s, --system', '只备份系统配置', false)
    .option('-w, --workspace', '只备份核心文件', false)
    .option('-k, --skills', '只备份技能目录', false)
    .option('-m, --memory', '只备份记忆数据', false)
    .option('-c, --cron', '只备份定时任务', false)
    .option('-d, --devices', '只备份设备配置', false)
    .option('-o, --output <path>', '指定输出目录')
    .option('--dry-run', '预览模式，不实际备份', false)
    .option('-j, --json', '以 JSON 格式输出', false)
    .option('--retain <days>', '保留最近 N 天的备份，自动删除更早的备份', parseInt)
    .option('--clean', '清理模式：只删除旧备份，不执行新备份', false)
    .parse(process.argv);

  const options = program.opts();
  
  // 确定备份类型
  let backupTypes = [];
  if (options.system) backupTypes.push('system');
  if (options.workspace) backupTypes.push('workspace');
  if (options.skills) backupTypes.push('skills');
  if (options.memory) backupTypes.push('memory');
  if (options.cron) backupTypes.push('cron');
  if (options.devices) backupTypes.push('devices');
  
  // 默认全量备份
  if (backupTypes.length === 0 || options.full) {
    backupTypes = ['system', 'workspace', 'skills', 'memory', 'cron', 'devices'];
  }

  const backupType = backupTypes.length === 6 ? 'full' : backupTypes.join('-');
  const outputDir = options.output || getDefaultOutputDir();
  const openclawRoot = getOpenClawRoot();
  
  const startTime = Date.now();
  
  try {
    // ========== 清理模式 ==========
    if (options.clean) {
      if (!options.retain) {
        console.error('❌ 错误: 清理模式需要指定 --retain 参数');
        console.error('💡 用法: node scripts/backup.js --clean --retain 14');
        process.exit(EXIT_CODES.PARAM_ERROR);
      }
      
      console.log('🗑️  正在扫描旧备份...\n');
      const cleanResult = await cleanOldBackups(outputDir, options.retain, options.dryRun);
      outputCleanResult(cleanResult, options.retain, options.dryRun);
      process.exit(EXIT_CODES.SUCCESS);
    }
    
    // ========== 备份模式 ==========
    // 收集文件信息
    console.log('🔍 正在扫描文件...');
    const collectedFiles = await collectFiles(backupTypes, openclawRoot);
    
    // Dry-run 模式
    if (options.dryRun) {
      console.log('\n📋 预览模式 - 将要备份的文件:\n');
      
      for (const [category, data] of Object.entries(collectedFiles.categories)) {
        const categoryName = FILE_CATEGORIES[category]?.name || category;
        console.log(`\n[${categoryName}]`);
        
        for (const file of data.files) {
          const status = file.status === 'success' ? '✅' : '⏭️';
          const size = file.size > 0 ? ` (${formatSize(file.size)})` : '';
          console.log(`  ${status} ${file.name}${size}`);
        }
      }
      
      console.log(`\n📊 统计:`);
      console.log(`   将备份: ${collectedFiles.stats.existing} 个文件/目录`);
      console.log(`   将跳过: ${collectedFiles.stats.missing} 个文件/目录 (不存在)`);
      console.log(`   预估大小: ${formatSize(collectedFiles.stats.totalSize)}\n`);
      
      process.exit(EXIT_CODES.SUCCESS);
    }
    
    // 确保输出目录存在
    if (!await ensureDir(outputDir)) {
      console.error(`❌ 错误: 无法创建输出目录: ${outputDir}`);
      console.error(`💡 建议: ${ERROR_SOLUTIONS['E006']}`);
      process.exit(EXIT_CODES.PERMISSION_ERROR);
    }
    
    // 创建临时目录
    const tempDir = path.join(openclawRoot, 'tmp', `backup-${Date.now()}`);
    await ensureDir(tempDir);
    
    // 复制文件
    console.log('📦 正在复制文件...');
    const { copiedFiles, errors } = await copyFilesToTemp(collectedFiles, tempDir, openclawRoot);
    
    // 创建清单
    const manifest = createManifest(backupType, copiedFiles);
    const manifestPath = path.join(tempDir, BACKUP_ROOT_NAME, 'manifest.json');
    await fse.ensureDir(path.dirname(manifestPath));
    await fse.writeJson(manifestPath, manifest, { spaces: 2 });
    
    // 生成文件名和目录名
    const timestamp = dayjs().format('YYYYMMDD-HHmmss');
    const backupDirName = `openclaw-backup-${backupType}-${timestamp}`;
    const backupFilename = `${backupDirName}.tar.gz`;
    const manifestFilename = `${backupDirName}.json`;
    
    // 创建备份输出子目录
    const backupDir = path.join(outputDir, backupDirName);
    await ensureDir(backupDir);
    
    // 压缩
    console.log('🗜️  正在压缩...');
    const tempBackupPath = path.join(tempDir, backupFilename);
    const backupSize = await compressBackup(tempDir, tempBackupPath);
    
    // 移动到备份子目录
    const finalBackupPath = path.join(backupDir, backupFilename);
    const finalManifestPath = path.join(backupDir, manifestFilename);
    
    await fse.move(tempBackupPath, finalBackupPath, { overwrite: true });
    
    // 生成详细清单
    const backupInfo = {
      type: backupType,
      timestamp: new Date().toISOString(),
      filename: backupFilename,
      size: backupSize,
      duration: (Date.now() - startTime) / 1000,
      errors: errors,
      warnings: []
    };
    
    const fullManifest = generateBackupManifest(backupInfo, collectedFiles, options);
    await fse.writeJson(finalManifestPath, fullManifest, { spaces: 2 });
    
    // 生成恢复指导
    const recoveryGuidePath = path.join(backupDir, 'RECOVERY_GUIDE.md');
    const recoveryGuide = generateRecoveryGuide(backupInfo, collectedFiles, recoveryGuidePath);
    await fse.writeFile(recoveryGuidePath, recoveryGuide);
    
    // 清理临时目录
    await fse.remove(tempDir);
    
    backupInfo.backupPath = finalBackupPath;
    backupInfo.manifestPath = finalManifestPath;
    backupInfo.recoveryPath = recoveryGuidePath;
    
    // 输出结果
    if (options.json) {
      outputJson(backupInfo, collectedFiles, options);
    } else {
      outputText(backupInfo, collectedFiles, options);
    }
    
    // ========== 清理旧备份 ==========
    if (options.retain) {
      console.log('🗑️  正在清理旧备份...');
      const cleanResult = await cleanOldBackups(outputDir, options.retain, false);
      if (cleanResult.deleted.length > 0) {
        console.log(`   已删除 ${cleanResult.deleted.length} 个旧备份`);
      }
      if (cleanResult.kept.length > 0) {
        console.log(`   保留 ${cleanResult.kept.length} 个最近备份\n`);
      }
    }
    
    process.exit(EXIT_CODES.SUCCESS);
    
  } catch (error) {
    console.error(`\n❌ 备份失败: ${error.message}`);
    console.error(error.stack);
    process.exit(EXIT_CODES.BACKUP_ERROR);
  }
}

// 运行主函数
main();