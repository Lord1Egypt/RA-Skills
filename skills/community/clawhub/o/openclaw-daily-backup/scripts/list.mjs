#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const BACKUP_DIR = path.join(__dirname, '../backups');

// Parse CLI arguments
const args = process.argv.slice(2);
const options = {
  verbose: false
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--verbose' || args[i] === '-v') {
    options.verbose = true;
  }
}

// Main list function
function listBackups() {
  if (!fs.existsSync(BACKUP_DIR)) {
    console.log('📦 No backups found (backup directory does not exist)');
    return;
  }

  const backups = [];

  // Scan timestamped backups
  const entries = fs.readdirSync(BACKUP_DIR);
  for (const entry of entries) {
    if (entry === 'named') continue;
    
    const fullPath = path.join(BACKUP_DIR, entry);
    if (!fs.statSync(fullPath).isDirectory()) continue;

    const manifestPath = path.join(fullPath, 'manifest.json');
    if (!fs.existsSync(manifestPath)) continue;

    try {
      const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
      backups.push({
        type: 'timestamped',
        path: fullPath,
        dirname: entry,
        manifest
      });
    } catch (err) {
      console.error(`⚠️  Invalid manifest in ${entry}: ${err.message}`);
    }
  }

  // Scan named backups
  const namedDir = path.join(BACKUP_DIR, 'named');
  if (fs.existsSync(namedDir)) {
    const namedEntries = fs.readdirSync(namedDir);
    for (const entry of namedEntries) {
      const fullPath = path.join(namedDir, entry);
      if (!fs.statSync(fullPath).isDirectory()) continue;

      const manifestPath = path.join(fullPath, 'manifest.json');
      if (!fs.existsSync(manifestPath)) continue;

      try {
        const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
        backups.push({
          type: 'named',
          path: fullPath,
          dirname: entry,
          manifest
        });
      } catch (err) {
        console.error(`⚠️  Invalid manifest in named/${entry}: ${err.message}`);
      }
    }
  }

  if (backups.length === 0) {
    console.log('📦 No backups found');
    return;
  }

  // Sort by timestamp (newest first)
  backups.sort((a, b) => new Date(b.manifest.timestamp) - new Date(a.manifest.timestamp));

  console.log(`📦 Found ${backups.length} backup(s)\n`);

  for (const backup of backups) {
    const { manifest, dirname, type } = backup;
    
    // Calculate total size
    let totalSize = 0;
    let fileCount = 0;
    for (const [filename, info] of Object.entries(manifest.files)) {
      if (info.exists) {
        totalSize += info.size;
        fileCount++;
      }
    }

    // Format timestamp
    const date = new Date(manifest.timestamp);
    const dateStr = date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });

    // Print summary
    if (type === 'named') {
      console.log(`📌 ${dirname} (named)`);
    } else {
      console.log(`📅 ${dirname}`);
    }
    console.log(`   Created: ${dateStr}`);
    if (manifest.name && type !== 'named') {
      console.log(`   Name: ${manifest.name}`);
    }
    if (manifest.description) {
      console.log(`   Description: ${manifest.description}`);
    }
    console.log(`   Files: ${fileCount} (${formatBytes(totalSize)})`);

    if (options.verbose) {
      console.log(`   Location: ${backup.path}`);
      console.log(`   Files backed up:`);
      for (const [filename, info] of Object.entries(manifest.files)) {
        if (info.exists) {
          console.log(`     ✅ ${filename} (${formatBytes(info.size)})`);
        } else {
          console.log(`     ⚠️  ${filename} (not found at backup time)`);
        }
      }
    }

    console.log();
  }

  // Summary
  const latestBackup = backups[0];
  console.log(`💡 Latest backup: ${latestBackup.dirname}`);
  console.log(`   To restore: node scripts/restore.mjs --timestamp ${latestBackup.dirname}`);
}

// Utility: Format bytes
function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Run list
listBackups();
