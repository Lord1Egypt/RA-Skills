#!/usr/bin/env node
/**
 * memory-migrate.js v5.0 — Seamless upgrade helper for memory-engine
 * 
 * Detects OpenClaw version capabilities and configures optimal memory setup:
 * - Enables native memorySearch if available (vector + hybrid search)
 * - Enables session-memory hook for /new and /reset
 * - Optionally enables experimental session memory indexing
 * - Updates cron frequency from 6h to 1h if needed
 * - Preserves all existing data (zero data loss)
 * 
 * Usage:
 *   node memory-migrate.js                  # dry-run: show what would change
 *   node memory-migrate.js --apply          # apply changes
 *   node memory-migrate.js --rollback       # revert to v4 mode (FTS5 only)
 *   node memory-migrate.js --status         # show current mode
 */
const fs = require('fs'), path = require('path');

const HOME = process.env.HOME || '/root';
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(HOME, '.openclaw/workspace');
const CONFIG_PATH = path.join(HOME, '.openclaw/openclaw.json');

const args = process.argv.slice(2);
const apply = args.includes('--apply');
const rollback = args.includes('--rollback');
const statusOnly = args.includes('--status');

function readConfig() {
  if (!fs.existsSync(CONFIG_PATH)) return {};
  try { return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8')); } catch { return {}; }
}

function writeConfig(cfg) {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2), 'utf8');
}

function detectCapabilities() {
  const caps = {
    openclawVersion: 'unknown',
    hasMemorySearch: false,
    hasSessionMemoryHook: false,
    hasQmdBackend: false,
    currentMode: 'legacy',  // legacy | native | hybrid
    nativeProvider: 'none',
    nativeIndexed: 0,
    fts5Available: false,
    betterSqlite3Available: false,
    sessionMemoryEnabled: false,
  };

  // Check OpenClaw version
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(
      require('child_process').execSync('npm root -g', { encoding: 'utf8' }).trim(),
      'openclaw/package.json'
    ), 'utf8'));
    caps.openclawVersion = pkg.version || 'unknown';
  } catch {}

  // Check if native memory_search tool exists (d.ts type file)
  const toolDts = path.join(HOME, '.openclaw');
  try {
    const npmRoot = require('child_process').execSync('npm root -g', { encoding: 'utf8' }).trim();
    const memToolPath = path.join(npmRoot, 'openclaw/dist/plugin-sdk/agents/tools/memory-tool.d.ts');
    caps.hasMemorySearch = fs.existsSync(memToolPath);
    const qmdPath = path.join(npmRoot, 'openclaw/dist/plugin-sdk/memory/qmd-manager.d.ts');
    caps.hasQmdBackend = fs.existsSync(qmdPath);
    const hookPath = path.join(npmRoot, 'openclaw/dist/bundled/session-memory/handler.js');
    caps.hasSessionMemoryHook = fs.existsSync(hookPath);
  } catch {}

  // Check current config
  const cfg = readConfig();
  const ms = cfg?.agents?.defaults?.memorySearch || {};
  const mem = cfg?.memory || {};
  caps.nativeProvider = ms.provider || 'auto';
  caps.sessionMemoryEnabled = ms?.experimental?.sessionMemory || false;
  
  if (ms.provider && ms.provider !== 'none') {
    caps.currentMode = 'native';
  } else if (mem.backend === 'qmd') {
    caps.currentMode = 'qmd';
  } else {
    caps.currentMode = 'legacy';
  }

  // Check better-sqlite3
  try {
    const npmRoot = require('child_process').execSync('npm root -g', { encoding: 'utf8' }).trim();
    require(path.join(npmRoot, 'better-sqlite3'));
    caps.betterSqlite3Available = true;
    caps.fts5Available = true;
  } catch {
    caps.betterSqlite3Available = false;
  }

  return caps;
}

function planMigration(caps) {
  const changes = [];
  
  if (rollback) {
    changes.push({
      key: 'rollback-native',
      desc: '禁用原生 memorySearch，回退到 FTS5 模式',
      path: 'agents.defaults.memorySearch',
      action: 'remove'
    });
    return changes;
  }

  // 1. Enable native memorySearch (if OpenClaw supports it)
  if (caps.hasMemorySearch && caps.currentMode === 'legacy') {
    changes.push({
      key: 'enable-native-search',
      desc: '启用原生 memory_search（向量+混合搜索，0 token 开销）',
      path: 'agents.defaults.memorySearch',
      value: {
        // Don't set provider — let OpenClaw auto-detect
        // This way it works with or without API keys
        sync: { watch: true, onSearch: true, onSessionStart: true },
        query: {
          maxResults: 5,
          minScore: 0.1,
          hybrid: {
            enabled: true,
            vectorWeight: 0.7,
            textWeight: 0.3,
            candidateMultiplier: 4,
            temporalDecay: {
              enabled: true,
              halfLifeDays: 30
            }
          }
        },
        cache: { enabled: true }
      }
    });
  }

  // 2. Enable session-memory hook
  if (caps.hasSessionMemoryHook) {
    const cfg = readConfig();
    const hookEnabled = cfg?.hooks?.internal?.entries?.['session-memory']?.enabled;
    if (hookEnabled !== true) {
      changes.push({
        key: 'enable-session-memory-hook',
        desc: '启用 session-memory hook（/new 和 /reset 时自动保存会话摘要）',
        path: 'hooks.internal.entries.session-memory',
        value: { enabled: true, messages: 20 }
      });
    }
  }

  // 3. Cron frequency check
  try {
    const crontab = require('child_process').execSync('crontab -l', { encoding: 'utf8' });
    if (crontab.includes('*/6') && crontab.includes('memory-cron.sh')) {
      changes.push({
        key: 'cron-frequency',
        desc: 'cron 频率 6h → 1h（更快检测 session reset）',
        action: 'cron-update'
      });
    }
  } catch {}

  // 4. memoryFlush improvement
  const cfg = readConfig();
  const flush = cfg?.agents?.defaults?.compaction?.memoryFlush;
  if (flush && !flush.forceFlushTranscriptBytes) {
    changes.push({
      key: 'flush-force-bytes',
      desc: '添加 forceFlushTranscriptBytes（大 session 也能触发 flush）',
      path: 'agents.defaults.compaction.memoryFlush.forceFlushTranscriptBytes',
      value: 2000000  // 2MB
    });
  }

  return changes;
}

function applyChanges(changes) {
  const cfg = readConfig();
  let cronUpdated = false;
  
  for (const change of changes) {
    if (change.action === 'remove') {
      // Remove nested path
      const parts = change.path.split('.');
      let obj = cfg;
      for (let i = 0; i < parts.length - 1; i++) {
        if (!obj[parts[i]]) break;
        obj = obj[parts[i]];
      }
      delete obj[parts[parts.length - 1]];
      console.log(`  ✅ ${change.desc}`);
      continue;
    }
    
    if (change.action === 'cron-update') {
      try {
        const { execSync } = require('child_process');
        const crontab = execSync('crontab -l', { encoding: 'utf8' });
        const updated = crontab.replace(
          /0 \*\/6 \* \* \* (.*memory-cron\.sh)/,
          '0 * * * * $1'
        );
        execSync(`echo '${updated.replace(/'/g, "'\\''")}' | crontab -`);
        cronUpdated = true;
        console.log(`  ✅ ${change.desc}`);
      } catch (e) {
        console.log(`  ❌ ${change.desc}: ${e.message.slice(0, 60)}`);
      }
      continue;
    }
    
    // Set nested config value
    const parts = change.path.split('.');
    let obj = cfg;
    for (let i = 0; i < parts.length - 1; i++) {
      if (!obj[parts[i]]) obj[parts[i]] = {};
      obj = obj[parts[i]];
    }
    obj[parts[parts.length - 1]] = change.value;
    console.log(`  ✅ ${change.desc}`);
  }
  
  // Backup old config
  if (fs.existsSync(CONFIG_PATH)) {
    const backupPath = CONFIG_PATH + '.pre-v5.' + Date.now();
    fs.copyFileSync(CONFIG_PATH, backupPath);
    console.log(`\n  💾 配置备份: ${path.basename(backupPath)}`);
  }
  
  writeConfig(cfg);
  console.log(`  📝 已更新 openclaw.json`);
}

// ── Main ──
const caps = detectCapabilities();

if (statusOnly) {
  console.log(JSON.stringify({
    openclawVersion: caps.openclawVersion,
    currentMode: caps.currentMode,
    nativeProvider: caps.nativeProvider,
    hasMemorySearch: caps.hasMemorySearch,
    hasSessionMemoryHook: caps.hasSessionMemoryHook,
    hasQmdBackend: caps.hasQmdBackend,
    fts5Available: caps.fts5Available,
    sessionMemoryEnabled: caps.sessionMemoryEnabled,
    memoryEngineVersion: '5.0.0',
  }, null, 2));
  process.exit(0);
}

console.log(`\n🧠 Memory Engine Migration Tool v5.0`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`OpenClaw: ${caps.openclawVersion}`);
console.log(`当前模式: ${caps.currentMode}`);
console.log(`原生 memory_search: ${caps.hasMemorySearch ? '✅ 可用' : '❌ 不可用'}`);
console.log(`session-memory hook: ${caps.hasSessionMemoryHook ? '✅ 可用' : '❌ 不可用'}`);
console.log(`FTS5 (better-sqlite3): ${caps.betterSqlite3Available ? '✅ 可用' : '❌ 不可用'}`);
console.log('');

const changes = planMigration(caps);

if (changes.length === 0) {
  console.log('✅ 无需变更，已是最优配置');
  process.exit(0);
}

console.log(`📋 ${rollback ? '回滚' : '升级'}计划 (${changes.length} 项变更):\n`);
for (const c of changes) {
  console.log(`  ${apply ? '→' : '○'} ${c.desc}`);
}

if (!apply) {
  console.log(`\n⚠️  以上为预览。执行: node memory-migrate.js --apply`);
  console.log(`   回滚: node memory-migrate.js --rollback --apply`);
} else {
  console.log('');
  applyChanges(changes);
  console.log(`\n✅ 完成！重启 OpenClaw gateway 使配置生效:`);
  console.log(`   openclaw gateway restart`);
}
