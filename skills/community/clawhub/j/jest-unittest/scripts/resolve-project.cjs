/**
 * 项目隔离模块 —— 按 projectRoot 的 hash 在 .temp/projects/<hash>/ 下存放 source.json 和 config.json。
 *
 * 解决用户级 skill 在多项目间配置冲突的问题。
 *
 * 用法：
 *   const { projectRoot, projectDir, sourcePath, configPath } = require('./resolve-project.cjs');
 *
 * 检测 projectRoot 的优先级：
 *   1. git rev-parse --show-toplevel（最准确）
 *   2. process.cwd()（降级方案）
 *
 * 向后兼容：
 *   如果 .temp/projects/<hash>/ 下不存在配置，但根级存在旧的 source.json / config.json，
 *   则自动迁移到新位置并删除旧文件。
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execSync } = require('child_process');

const skillRoot = path.resolve(__dirname, '..');

// ==================== 检测 projectRoot ====================

function detectProjectRoot() {
  // 优先使用 git
  try {
    const root = execSync('git rev-parse --show-toplevel', {
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
      timeout: 5000,
    }).trim();
    if (root && fs.existsSync(root)) return root;
  } catch (_) {
    // git 不可用，降级
  }

  return process.cwd();
}

// ==================== hash 计算 ====================

function shortHash(str) {
  return crypto.createHash('md5').update(str).digest('hex').substring(0, 8);
}

// ==================== 向后兼容：迁移旧文件 ====================

function migrateIfNeeded(projectDir) {
  const oldSourcePath = path.join(skillRoot, 'source.json');
  const oldConfigPath = path.join(skillRoot, 'config.json');
  const newSourcePath = path.join(projectDir, 'source.json');
  const newConfigPath = path.join(projectDir, 'config.json');

  let migrated = false;

  // 迁移 source.json
  if (!fs.existsSync(newSourcePath) && fs.existsSync(oldSourcePath)) {
    fs.mkdirSync(projectDir, { recursive: true });
    fs.copyFileSync(oldSourcePath, newSourcePath);
    fs.unlinkSync(oldSourcePath);
    migrated = true;
  }

  // 迁移 config.json
  if (!fs.existsSync(newConfigPath) && fs.existsSync(oldConfigPath)) {
    fs.mkdirSync(projectDir, { recursive: true });
    fs.copyFileSync(oldConfigPath, newConfigPath);
    fs.unlinkSync(oldConfigPath);
    migrated = true;
  }

  return migrated;
}

// ==================== 主逻辑 ====================

const projectRoot = detectProjectRoot();
const hash = shortHash(projectRoot);
const projectDir = path.join(skillRoot, '.temp', 'projects', hash);

// 首次运行时自动迁移旧文件
migrateIfNeeded(projectDir);

module.exports = {
  skillRoot,
  projectRoot,
  projectDir,
  hash,
  sourcePath: path.join(projectDir, 'source.json'),
  configPath: path.join(projectDir, 'config.json'),
};
