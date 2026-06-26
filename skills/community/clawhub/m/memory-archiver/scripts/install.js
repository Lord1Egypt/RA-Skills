#!/usr/bin/env node
/**
 * Memory Archiver Skill - 安装脚本
 * 用法：node scripts/install.js
 *
 * 功能：
 * 1. 创建记忆目录结构
 * 2. 安装 memory-archiver-hook hook（自动注册到 OpenClaw）
 * 3. 自动添加 cron 任务
 *
 * 原为 install.sh，已转为纯 JS
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE = path.join(process.env.HOME, '.openclaw', 'workspace');
const SKILL_DIR = path.join(WORKSPACE, 'skills', 'memory-archiver');
const HOOKS_DIR = path.join(WORKSPACE, 'hooks', 'memory-archiver-hook');
const MEMORY_DAILY = path.join(WORKSPACE, 'memory', 'daily');
const MEMORY_WEEKLY = path.join(WORKSPACE, 'memory', 'weekly');

console.log('🔧 开始安装 Memory Archiver Skill...\n');

// ===== Step 1: 创建记忆目录 =====
console.log('📁 Step 1: 创建记忆目录...');
fs.mkdirSync(MEMORY_DAILY, { recursive: true });
fs.mkdirSync(MEMORY_WEEKLY, { recursive: true });
console.log('   ✅ memory/daily/');
console.log('   ✅ memory/weekly/\n');

// ===== Step 2: 安装 hook =====
console.log('🔍 Step 2: 安装 memory-archiver-hook...');

const hookSource = path.join(SKILL_DIR, 'hooks');
const handlerJs = path.join(hookSource, 'handler.js');
const hookMd = path.join(hookSource, 'HOOK.md');

if (!fs.existsSync(handlerJs) || !fs.existsSync(hookMd)) {
  console.log(`   ❌ Hook 源文件不存在：${hookSource}/`);
  process.exit(1);
}

fs.mkdirSync(HOOKS_DIR, { recursive: true });
fs.copyFileSync(handlerJs, path.join(HOOKS_DIR, 'handler.js'));
fs.copyFileSync(hookMd, path.join(HOOKS_DIR, 'HOOK.md'));
console.log(`   ✅ Hook 文件已复制到 ${HOOKS_DIR}/\n`);

// 尝试通过 openclaw hooks install 正式注册
try {
  const listOutput = execSync('openclaw hooks list 2>/dev/null', { encoding: 'utf8' });
  if (listOutput.includes('memory-archiver-hook')) {
    console.log('   ✅ Hook 已注册（跳过重复安装）');
  } else {
    console.log('   📦 正在注册 hook...');
    const oldHookDir = path.join(process.env.HOME, '.openclaw', 'hooks', 'memory-archiver-hook');
    try { fs.rmSync(oldHookDir, { recursive: true, force: true }); } catch {}
    try {
      execSync(`openclaw hooks install --link "${HOOKS_DIR}"`, { stdio: 'pipe' });
      console.log('   ✅ Hook 已通过 openclaw hooks install 注册');
    } catch {
      console.log('   ⚠️  自动注册失败，请手动执行：');
      console.log(`      openclaw hooks install --link ${HOOKS_DIR}`);
    }
  }
  console.log('\n   💡 重启 gateway 生效：');
  console.log('      systemctl --user restart openclaw-gateway.service');
} catch {
  console.log('   ⚠️  未检测到 openclaw CLI，请手动注册 hook：');
  console.log(`      openclaw hooks install --link ${HOOKS_DIR}`);
}

console.log('');

// ===== Step 3: 自动添加 Cron 任务 =====
console.log('⏰ Step 3: 添加 Cron 任务...\n');

try {
  const cronList = execSync('openclaw cron list 2>/dev/null', { encoding: 'utf8' });
  const memoryCronCount = (cronList.match(/记忆/g) || []).length;

  if (memoryCronCount >= 3) {
    console.log('   ✅ Cron 任务已存在（跳过添加）');
  } else {
    const cronJobs = [
      {
        name: '记忆及时写入',
        schedule: '{"kind":"every","everyMs":600000}',
        payload: '{"kind":"systemEvent","text":"📝 记忆及时写入检查（静默模式）"}'
      },
      {
        name: '记忆归档 - Daily',
        schedule: '{"kind":"cron","expr":"0 23 * * *","tz":"Asia/Shanghai"}',
        payload: '{"kind":"systemEvent","text":"🌙 每日记忆归档时间（23:00）！"}'
      },
      {
        name: '记忆总结 - Weekly',
        schedule: '{"kind":"cron","expr":"0 22 * * 0","tz":"Asia/Shanghai"}',
        payload: '{"kind":"systemEvent","text":"📅 每周记忆总结时间（周日 22:00）！"}'
      }
    ];

    for (const job of cronJobs) {
      console.log(`   📅 正在添加 ${job.name}...`);
      try {
        execSync(
          `openclaw cron add --name "${job.name}" --schedule '${job.schedule}' --payload '${job.payload}' --session-target main --delivery '{"mode":"none"}'`,
          { stdio: 'pipe' }
        );
        console.log('   ✅ 已添加');
      } catch {
        console.log('   ⚠️  添加失败（可能已存在）');
      }
    }
  }
} catch {
  console.log('   ⚠️  无法检查 Cron 任务');
}

console.log('');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('✅ Memory Archiver 安装完成！');
console.log('');
console.log('   📂 记忆目录：~/.openclaw/workspace/memory/');
console.log('   🔍 Hook: ~/.openclaw/workspace/hooks/memory-archiver-hook/');
console.log('   📖 文档：skills/memory-archiver/SKILL.md');
console.log('   ⏰ Cron: 3 个定时任务已配置');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
