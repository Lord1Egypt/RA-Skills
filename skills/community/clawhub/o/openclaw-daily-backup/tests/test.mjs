#!/usr/bin/env node
// Minimal unit tests for soul-backup

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const SKILL_DIR = path.resolve(__dirname, '..');

let testsPassed = 0;
let testsFailed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`✅ ${message}`);
    testsPassed++;
  } else {
    console.error(`❌ ${message}`);
    testsFailed++;
  }
}

async function runTests() {
  console.log('🧪 Running SOUL Backup Tests\n');

  // Test 1: Backup script exists and is executable
  const backupScript = path.join(SKILL_DIR, 'scripts/backup.mjs');
  assert(fs.existsSync(backupScript), 'backup.mjs exists');
  assert(fs.statSync(backupScript).mode & 0o111, 'backup.mjs is executable');

  // Test 2: Restore script exists and is executable
  const restoreScript = path.join(SKILL_DIR, 'scripts/restore.mjs');
  assert(fs.existsSync(restoreScript), 'restore.mjs exists');
  assert(fs.statSync(restoreScript).mode & 0o111, 'restore.mjs is executable');

  // Test 3: List script exists and is executable
  const listScript = path.join(SKILL_DIR, 'scripts/list.mjs');
  assert(fs.existsSync(listScript), 'list.mjs exists');
  assert(fs.statSync(listScript).mode & 0o111, 'list.mjs is executable');

  // Test 4: Validate script exists and is executable
  const validateScript = path.join(SKILL_DIR, 'scripts/validate.mjs');
  assert(fs.existsSync(validateScript), 'validate.mjs exists');
  assert(fs.statSync(validateScript).mode & 0o111, 'validate.mjs is executable');

  // Test 5: Create test backup
  try {
    const { stdout } = await execAsync(`node ${backupScript} --name test-backup --desc "Unit test backup"`);
    assert(stdout.includes('Backup complete'), 'Backup creation succeeds');
    assert(stdout.includes('test-backup'), 'Backup name appears in output');
  } catch (err) {
    assert(false, `Backup creation failed: ${err.message}`);
  }

  // Test 6: List backups
  try {
    const { stdout } = await execAsync(`node ${listScript}`);
    assert(stdout.includes('test-backup'), 'List shows test backup');
  } catch (err) {
    assert(false, `List backups failed: ${err.message}`);
  }

  // Test 7: Validate backup
  try {
    const { stdout } = await execAsync(`node ${validateScript} --name test-backup`);
    assert(stdout.includes('Valid backup'), 'Backup validation passes');
  } catch (err) {
    assert(false, `Backup validation failed: ${err.message}`);
  }

  // Test 8: Dry-run restore
  try {
    const { stdout } = await execAsync(`node ${restoreScript} --name test-backup --dry-run`);
    assert(stdout.includes('Dry run complete'), 'Dry-run restore succeeds');
    assert(stdout.includes('No files were modified'), 'Dry-run does not modify files');
  } catch (err) {
    assert(false, `Dry-run restore failed: ${err.message}`);
  }

  // Test 9: openclaw.json sanitization (if exists)
  const openclawJsonPath = path.join(SKILL_DIR, '../..', 'openclaw.json');
  if (fs.existsSync(openclawJsonPath)) {
    const backupPath = path.join(SKILL_DIR, 'backups/named/test-backup');
    const sanitizedPath = path.join(backupPath, 'openclaw.sanitized.json');
    
    if (fs.existsSync(sanitizedPath)) {
      const sanitized = JSON.parse(fs.readFileSync(sanitizedPath, 'utf8'));
      const hasRedacted = JSON.stringify(sanitized).includes('[REDACTED]');
      assert(hasRedacted, 'openclaw.json contains [REDACTED] placeholders');
    }
  }

  // Test 10: Cleanup test backup
  try {
    const testBackupPath = path.join(SKILL_DIR, 'backups/named/test-backup');
    if (fs.existsSync(testBackupPath)) {
      fs.rmSync(testBackupPath, { recursive: true });
      assert(true, 'Test backup cleanup successful');
    }
  } catch (err) {
    assert(false, `Cleanup failed: ${err.message}`);
  }

  // Summary
  console.log(`\n📊 Test Summary`);
  console.log(`   Passed: ${testsPassed}`);
  console.log(`   Failed: ${testsFailed}`);
  
  if (testsFailed > 0) {
    console.log(`\n❌ Tests failed`);
    process.exit(1);
  } else {
    console.log(`\n✅ All tests passed`);
    process.exit(0);
  }
}

runTests().catch(err => {
  console.error('❌ Test runner failed:', err);
  process.exit(1);
});
