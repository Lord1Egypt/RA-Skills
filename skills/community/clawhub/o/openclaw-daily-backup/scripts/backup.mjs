#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import os from 'os';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DEFAULT_WORKSPACE_ROOT = path.resolve(__dirname, '../../..');
const BACKUP_DIR = path.join(__dirname, '../backups');
const SOUL_FILES = [
  'SOUL.md',
  'USER.md',
  'AGENTS.md',
  'IDENTITY.md',
  'TOOLS.md',
  'HEARTBEAT.md',
  'BOOTSTRAP.md'
];

const SENSITIVE_PATTERNS = [
  /token/i,
  /key/i,
  /secret/i,
  /password/i,
  /apikey/i,
  /api_key/i,
  /auth/i,
  /credential/i,
  /bearer/i
];

const args = process.argv.slice(2);
const options = {
  name: null,
  description: null,
  workspace: DEFAULT_WORKSPACE_ROOT
};

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--name' && args[i + 1]) {
    options.name = args[i + 1];
    i++;
  } else if (args[i] === '--desc' && args[i + 1]) {
    options.description = args[i + 1];
    i++;
  } else if (args[i] === '--workspace' && args[i + 1]) {
    options.workspace = path.resolve(args[i + 1]);
    i++;
  }
}

function calculateHash(filePath) {
  const content = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(content).digest('hex');
}

function getTimestamp() {
  return new Date().toISOString().replace(/:/g, '-').split('.')[0];
}

function sanitizeObject(obj) {
  if (typeof obj !== 'object' || obj === null) return obj;

  const sanitized = Array.isArray(obj) ? [] : {};

  for (const [key, value] of Object.entries(obj)) {
    const isSensitive = SENSITIVE_PATTERNS.some(pattern => pattern.test(key));

    if (isSensitive && typeof value === 'string' && value.length > 0) {
      sanitized[key] = '[REDACTED]';
    } else if (typeof value === 'object' && value !== null) {
      sanitized[key] = sanitizeObject(value);
    } else {
      sanitized[key] = value;
    }
  }

  return sanitized;
}

function sanitizeOpenClawConfig(configPath) {
  try {
    const content = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(content);
    return JSON.stringify(sanitizeObject(config), null, 2);
  } catch {
    return null;
  }
}

function getAgentMarkdownFiles(agentsRoot) {
  const files = [];

  if (!fs.existsSync(agentsRoot)) return files;

  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.isFile() && entry.name.toLowerCase().endsWith('.md')) {
        files.push(path.relative(agentsRoot, fullPath));
      }
    }
  }

  walk(agentsRoot);
  return files.sort();
}

function backupFile({ sourcePath, backupRelativePath, manifest, backupPath, restoreTo }) {
  const destPath = path.join(backupPath, backupRelativePath);
  fs.mkdirSync(path.dirname(destPath), { recursive: true });
  fs.copyFileSync(sourcePath, destPath);

  const stats = fs.statSync(sourcePath);
  const hash = calculateHash(sourcePath);

  manifest.files[backupRelativePath] = {
    size: stats.size,
    hash: `sha256:${hash}`,
    exists: true,
    restoreTo
  };

  return stats.size;
}

async function backup() {
  const WORKSPACE_ROOT = options.workspace;
  const OPENCLAW_ROOT = path.join(os.homedir(), '.openclaw');
  const AGENTS_ROOT = path.join(OPENCLAW_ROOT, 'agents');

  console.log('🔍 Starting SOUL backup...\n');

  const timestamp = getTimestamp();
  const backupPath = options.name
    ? path.join(BACKUP_DIR, 'named', options.name)
    : path.join(BACKUP_DIR, timestamp);

  if (fs.existsSync(backupPath)) {
    console.error(`❌ Backup already exists: ${backupPath}`);
    process.exit(1);
  }

  fs.mkdirSync(backupPath, { recursive: true });

  const manifest = {
    timestamp: new Date().toISOString(),
    name: options.name || null,
    description: options.description || null,
    workspace: WORKSPACE_ROOT,
    openclaw_root: OPENCLAW_ROOT,
    files: {},
    created_by: path.basename(WORKSPACE_ROOT),
    openclaw_version: '1.1.1'
  };

  let backedUpCount = 0;
  let skippedCount = 0;

  for (const filename of SOUL_FILES) {
    const sourcePath = path.join(WORKSPACE_ROOT, filename);

    if (fs.existsSync(sourcePath)) {
      const size = backupFile({
        sourcePath,
        backupRelativePath: filename,
        manifest,
        backupPath,
        restoreTo: 'workspace'
      });
      console.log(`✅ Backed up: ${filename} (${size} bytes)`);
      backedUpCount++;
    } else {
      manifest.files[filename] = {
        size: 0,
        hash: null,
        exists: false,
        restoreTo: 'workspace'
      };
      console.log(`⚠️  Skipped: ${filename} (not found)`);
      skippedCount++;
    }
  }

  const agentMarkdownFiles = getAgentMarkdownFiles(AGENTS_ROOT);
  if (agentMarkdownFiles.length === 0) {
    console.log('⚠️  No agent markdown files found under ~/.openclaw/agents');
  } else {
    console.log(`\n🤖 Backing up ${agentMarkdownFiles.length} agent markdown file(s)...`);
    for (const relPath of agentMarkdownFiles) {
      const sourcePath = path.join(AGENTS_ROOT, relPath);
      const backupRelativePath = path.join('openclaw-agents', relPath);
      const size = backupFile({
        sourcePath,
        backupRelativePath,
        manifest,
        backupPath,
        restoreTo: 'openclaw_agents'
      });
      console.log(`✅ Backed up: ~/.openclaw/agents/${relPath} (${size} bytes)`);
      backedUpCount++;
    }
  }

  const openclawJsonPath = path.join(OPENCLAW_ROOT, 'openclaw.json');
  if (fs.existsSync(openclawJsonPath)) {
    const sanitizedContent = sanitizeOpenClawConfig(openclawJsonPath);

    if (sanitizedContent) {
      const backupRelativePath = 'openclaw.sanitized.json';
      const destPath = path.join(backupPath, backupRelativePath);
      fs.writeFileSync(destPath, sanitizedContent);

      const stats = fs.statSync(destPath);
      const hash = crypto.createHash('sha256').update(sanitizedContent).digest('hex');

      manifest.files[backupRelativePath] = {
        size: stats.size,
        hash: `sha256:${hash}`,
        exists: true,
        sanitized: true,
        original: '~/.openclaw/openclaw.json',
        restoreTo: 'manual'
      };

      console.log(`✅ Backed up: ~/.openclaw/openclaw.json → openclaw.sanitized.json (${stats.size} bytes, sensitive fields redacted)`);
      backedUpCount++;
    } else {
      console.log('⚠️  Skipped: ~/.openclaw/openclaw.json (parse error)');
      skippedCount++;
    }
  } else {
    console.log('⚠️  Skipped: ~/.openclaw/openclaw.json (not found)');
    skippedCount++;
  }

  const manifestPath = path.join(backupPath, 'manifest.json');
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));

  console.log('\n📦 Backup complete!');
  console.log(`   Location: ${backupPath}`);
  console.log(`   Files backed up: ${backedUpCount}`);
  console.log(`   Files skipped: ${skippedCount}`);

  if (options.name) console.log(`   Name: ${options.name}`);
  if (options.description) console.log(`   Description: ${options.description}`);
}

backup().catch(err => {
  console.error('❌ Backup failed:', err.message);
  process.exit(1);
});
