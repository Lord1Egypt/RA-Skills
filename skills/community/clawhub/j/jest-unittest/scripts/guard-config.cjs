/**
 * config.json 前置检查 + 环境检查模块。
 *
 * 功能：
 *   1. 校验 config.json 存在且有效
 *   2. 校验 jest 配置文件存在
 *   3. 校验 npx jest 可用
 *
 * 通过 → 返回 config 对象
 * 失败 → 输出统一的错误 JSON 并退出：
 *   { "success": false, "error": "...", "hint": "...", "type": "config_error" | "env_error" }
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const project = require('./resolve-project.cjs');
const { projectRoot, configPath, sourcePath } = project;
const relSourcePath = path.relative(projectRoot, sourcePath);

function fail(type, error, hint) {
  console.log(JSON.stringify({ success: false, type, error, hint, sourceJsonPath: relSourcePath }, null, 2));
  process.exit(1);
}

// ==================== 1. config.json 校验 ====================

if (!fs.existsSync(configPath)) {
  fail('config_error', 'config.json 不存在',
    `请先在 ${relSourcePath} 中配置 jestConfigPath（项目 jest 配置文件的相对路径），然后执行 reload.cjs 生成 config.json`);
}

let config;
try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf-8').trim());
} catch (e) {
  fail('config_error', `config.json 解析失败: ${e.message}`, '请执行 reload.cjs 重新生成');
}

if (!config || Object.keys(config).length === 0) {
  fail('config_error', 'config.json 内容为空',
    `请先在 ${relSourcePath} 中配置 jestConfigPath，然后执行 reload.cjs 生成 config.json`);
}

const required = ['jestConfigPath', 'coverageDir', 'componentDir', 'testDir', 'testAllCommand', 'testOneCommand'];
const missing = required.filter(f => !config[f]);
if (missing.length > 0) {
  fail('config_error', `config.json 缺少字段: ${missing.join(', ')}`, '请执行 reload.cjs 重新生成');
}

// ==================== 2. jest 配置文件存在性校验 ====================

const jestConfigFullPath = path.join(projectRoot, config.jestConfigPath);
if (!fs.existsSync(jestConfigFullPath)) {
  fail('config_error', `jest 配置文件不存在: ${config.jestConfigPath}`,
    `请检查 ${relSourcePath} 中的 jestConfigPath 是否正确，然后执行 reload.cjs 重新生成`);
}

// ==================== 3. jest 可用性校验 ====================

try {
  execSync('npx jest --version', { cwd: projectRoot, stdio: 'pipe', timeout: 10000 });
} catch (e) {
  fail('env_error', 'npx jest 不可用', '请排查 jest 环境问题');
}

// 通过所有检查，将 projectRoot 挂到 config 上供调用方使用
config.projectRoot = projectRoot;
module.exports = config;
