#!/usr/bin/env node
// backup.mjs - 自动备份脚本 (v2.4)
// 用法: node scripts/backup.mjs [--dir ./backups] [--keep 7]

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');

// 解析参数
const args = process.argv.slice(2);
const backupDir = args.includes('--dir')
  ? path.resolve(args[args.indexOf('--dir') + 1])
  : path.join(root, 'memory', 'backups');
const keepDays = args.includes('--keep')
  ? parseInt(args[args.indexOf('--keep') + 1]) || 7
  : 7;

// 确保备份目录存在
fs.mkdirSync(backupDir, { recursive: true });

const dateStr = new Date().toISOString().split('T')[0];
const timestamp = Date.now();

async function backup() {
  console.log(`📦 开始备份... ${dateStr}`);

  // 1. 备份 SQLite 文件
  const dbPath = path.join(root, 'memory', 'memory.db');
  if (fs.existsSync(dbPath)) {
    const bakFile = path.join(backupDir, `memory-${dateStr}-${timestamp}.db`);
    fs.copyFileSync(dbPath, bakFile);
    console.log(`  ✅ SQLite: ${bakFile} (${(fs.statSync(bakFile).size / 1024).toFixed(1)} KB)`);
  } else {
    console.log(`  ⚠️ SQLite 文件不存在: ${dbPath}`);
  }

  // 2. 导出 JSON 备份
  try {
    const { exportMemories } = await import('../src/db/repository.mjs');
    const { loadConfig } = await import('../src/db/config-loader.mjs');
    const { initDatabase } = await import('../src/db/database.mjs');
    
    const config = loadConfig();
    await initDatabase(config);
    
    const data = exportMemories({ status: 'all' });
    const jsonFile = path.join(backupDir, `memories-${dateStr}-${timestamp}.json`);
    fs.writeFileSync(jsonFile, JSON.stringify(data, null, 2));
    console.log(`  ✅ JSON: ${jsonFile} (${(fs.statSync(jsonFile).size / 1024).toFixed(1)} KB)`);
  } catch (e) {
    console.log(`  ⚠️ JSON 导出失败: ${e.message}`);
  }

  // 3. 清理过期备份
  const files = fs.readdirSync(backupDir)
    .filter(f => f.startsWith('memory-') || f.startsWith('memories-'))
    .map(f => ({ name: f, ctime: fs.statSync(path.join(backupDir, f)).ctimeMs }))
    .sort((a, b) => b.ctime - a.ctime);

  const cutoff = Date.now() - keepDays * 86400000;
  let deleted = 0;
  for (const f of files) {
    if (f.ctime < cutoff) {
      fs.unlinkSync(path.join(backupDir, f.name));
      deleted++;
    }
  }
  
  if (deleted > 0) console.log(`  🧹 清理了 ${deleted} 个过期备份`);
  console.log(`  📊 当前备份: ${files.length - deleted} 个`);

  console.log(`✅ 备份完成!`);
}

backup().catch(e => {
  console.error('❌ 备份失败:', e.message);
  process.exit(1);
});
