#!/usr/bin/env node
/**
 * check-update.js — 检查 ielts-reading-review skill 是否有新版本
 * 
 * 用法：
 *   node check-update.js          # 检查并提示
 *   node check-update.js --auto   # 如果有更新自动执行 clawhub update
 * 
 * 工作原理：
 *   1. 读取本地 SKILL.md 中的版本号（从 Architecture 行提取 vX.Y.Z）
 *   2. clawhub inspect 获取 ClawHub 上的最新版本
 *   3. 比较 semver，如果远程更新则提示/自动更新
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const SLUG = 'ielts-reading-review';
const AUTO = process.argv.includes('--auto');

// ===== 1. 读取本地版本 =====
function getLocalVersion() {
  // 优先从 SKILL.md 读取
  const locations = [
    path.join(__dirname, '..', 'SKILL.md'),                          // skill repo 内
    path.join(process.env.HOME, '.workbuddy/skills', SLUG, 'SKILL.md'), // 用户级安装
  ];
  
  for (const loc of locations) {
    if (fs.existsSync(loc)) {
      const content = fs.readFileSync(loc, 'utf-8');
      // 匹配 "## Architecture (vX.Y.Z" 或 "## Architecture (vX.Y"
      const match = content.match(/Architecture\s*\(v(\d+\.\d+(?:\.\d+)?)/);
      if (match) {
        let v = match[1];
        if (v.split('.').length === 2) v += '.0'; // 补齐三位
        return { version: v, path: loc };
      }
      // 也匹配 VERSION="X.Y.Z" (publish script)
      const match2 = content.match(/VERSION="(\d+\.\d+\.\d+)"/);
      if (match2) return { version: match2[1], path: loc };
    }
  }
  
  // fallback: 从 publish-clawhub.sh 读
  const pubScript = path.join(__dirname, '..', 'publish-clawhub.sh');
  if (fs.existsSync(pubScript)) {
    const content = fs.readFileSync(pubScript, 'utf-8');
    const match = content.match(/VERSION="(\d+\.\d+\.\d+)"/);
    if (match) return { version: match[1], path: pubScript };
  }
  
  return null;
}

// ===== 2. 获取远程版本 =====
function getRemoteVersion() {
  try {
    const raw = execSync(`clawhub inspect ${SLUG} --json 2>/dev/null`, { encoding: 'utf-8' });
    // 跳过 "- Fetching skill" 等非 JSON 行
    const jsonStart = raw.indexOf('{');
    if (jsonStart < 0) return null;
    const data = JSON.parse(raw.slice(jsonStart));
    const skill = data.skill || data;
    // 版本可能在 tags.latest 或 latestVersion
    const ver = skill.tags?.latest || skill.latestVersion || data.latestVersion;
    return typeof ver === 'string' ? ver : null;
  } catch (e) {
    // clawhub 未安装或网络不通
    return null;
  }
}

// ===== 3. semver 比较 =====
function compareSemver(a, b) {
  const pa = a.split('.').map(Number);
  const pb = b.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    const va = pa[i] || 0;
    const vb = pb[i] || 0;
    if (va < vb) return -1;
    if (va > vb) return 1;
  }
  return 0;
}

// ===== Main =====
function main() {
  const local = getLocalVersion();
  if (!local) {
    console.log('⚠️  无法检测本地版本（找不到 SKILL.md）');
    process.exit(1);
  }
  
  console.log(`📦 本地版本: v${local.version}  (${local.path})`);
  
  const remote = getRemoteVersion();
  if (!remote) {
    console.log('⚠️  无法获取远程版本（clawhub 未安装或网络不通）');
    process.exit(0);
  }
  
  console.log(`☁️  远程版本: v${remote}  (ClawHub)`);
  
  const cmp = compareSemver(local.version, remote);
  
  if (cmp >= 0) {
    console.log('✅ 已是最新版本');
    process.exit(0);
  }
  
  // 有更新
  console.log('');
  console.log(`🆕 有新版本可用！v${local.version} → v${remote}`);
  
  if (AUTO) {
    console.log('🔄 正在自动更新...');
    try {
      const userSkillsDir = path.join(process.env.HOME, '.workbuddy/skills');
      const targetDir = path.join(userSkillsDir, SLUG);
      const backupDir = `${targetDir}.bak-${Date.now()}`;

      // clawhub install 没有 --dir 参数，只能在 cwd 下创建 <slug> 子目录
      // 策略：先备份旧目录，再在 userSkillsDir 下 install --force（必要时清理 skills/<slug> 嵌套）
      if (fs.existsSync(targetDir)) {
        fs.renameSync(targetDir, backupDir);
        console.log(`📦 旧版本备份至：${backupDir}`);
      }

      execSync(`clawhub install ${SLUG} --force`, {
        cwd: userSkillsDir,
        encoding: 'utf-8',
        stdio: 'inherit'
      });

      // 处理 clawhub 嵌套问题：有时会装到 ~/.workbuddy/skills/skills/<slug>
      const nested = path.join(userSkillsDir, 'skills', SLUG);
      if (fs.existsSync(nested) && !fs.existsSync(targetDir)) {
        fs.renameSync(nested, targetDir);
        const skillsDir = path.join(userSkillsDir, 'skills');
        try { fs.rmdirSync(skillsDir); } catch (e) {}
      }

      if (fs.existsSync(targetDir)) {
        console.log(`✅ 已更新到 v${remote}（备份保留在 ${backupDir}，确认无误后可手动删除）`);
      } else {
        // 失败回滚
        if (fs.existsSync(backupDir)) {
          fs.renameSync(backupDir, targetDir);
          console.log('❌ 安装失败，已回滚到旧版本');
        }
        process.exit(1);
      }
    } catch (e) {
      console.log('❌ 自动更新失败：' + e.message);
      console.log('   请手动运行: cd ~/.workbuddy/skills && clawhub install ' + SLUG + ' --force');
      process.exit(1);
    }
  } else {
    console.log('');
    console.log('更新方式：');
    console.log(`  node ${path.basename(__filename)} --auto     # 自动更新`);
    console.log(`  clawhub install ${SLUG}                      # 手动安装最新版`);
  }
}

main();
