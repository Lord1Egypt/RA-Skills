#!/usr/bin/env node
/**
 * openclaw-repair-kit - 一键安装脚本
 * 运行方式: node install.mjs
 */

import { execSync } from 'child_process';
import { existsSync, mkdirSync, copyFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = homedir();
const SKILLS_DIR = join(HOME, '.openclaw', 'workspace', 'skills');
const WORKSPACE_DIR = join(HOME, '.openclaw', 'workspace');

function run(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf8', timeout: 15000, stdio: 'pipe' });
  } catch (e) {
    return (e.stdout || '') + (e.stderr || '');
  }
}

console.log('🦞 openclaw-repair-kit - 安装中...\n');

// 1. 检查 openclaw 是否安装
const version = run('openclaw --version');
if (!version.trim().match(/^\d{4}\.\d+\.\d+/)) {
  console.error('❌ 找不到 openclaw，请先安装：npm install -g openclaw');
  process.exit(1);
}
console.log(`✅ 检测到 OpenClaw ${version.trim()}`);

// 2. 检查 workspace 是否存在
if (!existsSync(WORKSPACE_DIR)) {
  console.error(`❌ 找不到 OpenClaw workspace: ${WORKSPACE_DIR}`);
  console.error('请确认 OpenClaw 已初始化（运行过 KKClaw 或 openclaw gateway）');
  process.exit(1);
}

// 3. 安装 openclaw-repair-kit skill
console.log('\n📦 安装 openclaw-repair-kit...');
const destDir = join(SKILLS_DIR, 'openclaw-repair-kit');
mkdirSync(destDir, { recursive: true });

const files = ['SKILL.md', 'check.mjs', 'run.mjs'].filter(f => existsSync(join(__dirname, f)));
files.forEach(f => {
  copyFileSync(join(__dirname, f), join(destDir, f));
  console.log(`  复制: ${f}`);
});
console.log('✅ openclaw-repair-kit 安装完成');

// 4. 创建/更新 BOOT.md
console.log('\n📝 配置启动自动检查 (BOOT.md)...');
const bootPath = join(WORKSPACE_DIR, 'BOOT.md');
const bootContent = `# BOOT — 每次网关启动时执行

## 升级后自动健康检查

启动时检查 OpenClaw 版本是否发生变化，若检测到升级，立即运行健康检查脚本修复常见问题。

执行以下步骤：

1. 读取当前运行版本：执行 \`system.run\` → \`openclaw --version\`，取第一行作为当前版本。
2. 读取上次记录的版本：读取文件 \`memory/last-version.txt\`（不存在则视为首次启动）。
3. 对比两个版本：
   - **相同** → 无需检查，正常启动。
   - **不同或文件不存在** → 检测到升级，执行步骤 4。
4. 运行健康检查：执行 \`system.run\` → \`node "skills/openclaw-repair-kit/check.mjs"\`
5. 将当前版本写入 \`memory/last-version.txt\`。
6. 不需要回复用户，静默完成即可（NO_REPLY）。
`;
writeFileSync(bootPath, bootContent, 'utf8');
console.log('✅ BOOT.md 配置完成');

// 5. 启用 boot-md hook
console.log('\n🔧 启用 boot-md hook...');
const hookResult = run('openclaw hooks enable boot-md');
if (hookResult.includes('enabled') || hookResult.includes('already')) {
  console.log('✅ boot-md hook 已启用');
} else {
  console.log('⚠️  请手动启用 hook：openclaw hooks enable boot-md');
  console.log('   详情：', hookResult.trim());
}

// 6. 写入当前版本（避免首次启动误触发）
const lastVersionPath = join(WORKSPACE_DIR, 'memory', 'last-version.txt');
mkdirSync(join(WORKSPACE_DIR, 'memory'), { recursive: true });
writeFileSync(lastVersionPath, version.trim(), 'utf8');
console.log('✅ 已记录当前版本');

console.log(`
✅ 安装完成！

工作原理：
  每次重启 KKClaw → boot-md hook 触发 → 比较版本号
  → 检测到升级 → 自动运行健康检查 → 发现问题自动联系 AI 修复

下次升级后重启 KKClaw，修复将全自动进行。

也可手动运行健康检查：
  node "${join(destDir, 'check.mjs')}"
`);
