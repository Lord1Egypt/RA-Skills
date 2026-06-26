#!/usr/bin/env node
/**
 * JEP Guard v2.0.4 — Pre-Uninstall Hook
 * 
 * v2.0.4 FIX: Retained pure Node.js tar backup. No shell commands.
 */

const readline = require('readline');
const fs = require('fs');
const path = require('path');
const os = require('os');

const CONFIG_DIR = path.join(os.homedir(), '.jep-guard');

function ask(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => rl.question(question, ans => { rl.close(); resolve(ans.trim().toLowerCase()); }));
}

// v2.0.4: Pure Node.js tar backup (no shell commands)
async function createBackup(sourceDir, outputPath) {
  const tar = require('tar'); // Node.js tar package (already in dependencies)
  return tar.create({
    gzip: true,
    file: outputPath,
    cwd: sourceDir
  }, ['.']);
}

async function main() {
  console.log('\n⚠️  JEP Guard Uninstall\n');

  if (!fs.existsSync(CONFIG_DIR)) {
    console.log('No data found. Uninstalling...');
    return;
  }

  const stats = { files: 0, size: 0 };
  function calcSize(dir) {
    const items = fs.readdirSync(dir);
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        calcSize(fullPath);
      } else {
        stats.files++;
        stats.size += stat.size;
      }
    }
  }
  calcSize(CONFIG_DIR);

  console.log(`Found ${stats.files} files (${(stats.size / 1024 / 1024).toFixed(1)} MB)`);
  console.log(`Location: ${CONFIG_DIR}\n`);

  if (process.env.CI || process.env.JEP_PURGE === '1') {
    console.log('CI mode: Purging all data...');
    fs.rmSync(CONFIG_DIR, { recursive: true, force: true });
    console.log('All JEP Guard data removed.');
    return;
  }

  console.log('Choose data retention:');
  console.log('  [1] Keep audit logs and config (recommended)');
  console.log('  [2] Delete all data permanently');
  console.log('  [3] Export then delete');
  console.log('  [Enter] Cancel uninstall\n');

  const choice = await ask('Your choice: ');

  switch (choice) {
    case '1':
    case 'keep':
      console.log('\n✅ Config preserved.');
      console.log('   To restart: claw install jep-guard');
      console.log('   To delete later: rm -rf ~/.jep-guard\n');
      break;

    case '2':
    case 'delete':
      console.log('\n🗑️  Deleting all data...');
      fs.rmSync(CONFIG_DIR, { recursive: true, force: true });
      console.log('All JEP Guard data removed.\n');
      break;

    case '3':
    case 'export':
      const exportPath = path.join(os.homedir(), `jep-guard-backup-${Date.now()}.tar.gz`);
      console.log(`\n📦 Exporting to ${exportPath}...`);

      try {
        await createBackup(CONFIG_DIR, exportPath);
        console.log(`✅ Exported to: ${exportPath}`);
      } catch (e) {
        console.log(`⚠️  Export failed: ${e.message}`);
        console.log('   Falling back to manual backup.');
      }

      const confirm = await ask('\nDelete original data? [y/N]: ');
      if (confirm === 'y' || confirm === 'yes') {
        fs.rmSync(CONFIG_DIR, { recursive: true, force: true });
        console.log('Original data deleted.\n');
      } else {
        console.log('Original data kept.\n');
      }
      break;

    default:
      console.log('\n❌ Uninstall cancelled.\n');
      process.exit(1);
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});