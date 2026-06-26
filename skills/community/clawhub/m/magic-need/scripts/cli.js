#!/usr/bin/env node
/**
 * magic-need CLI
 * Captures tool/data needs identified by AI agents
 * Usage: cli.js "description of the need"
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Determine data directory (preference: ~/.magic-need)
function getDataDir() {
  const homeDir = os.homedir();
  return path.join(homeDir, '.magic-need');
}

const DATA_DIR = getDataDir();
const DATA_FILE = path.join(DATA_DIR, 'needs.json');

// Ensure directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Load existing needs
function loadNeeds() {
  if (!fs.existsSync(DATA_FILE)) {
    return [];
  }
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  } catch {
    return [];
  }
}

// Save needs
function saveNeeds(needs) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(needs, null, 2));
}

// Generate short ID
function generateId() {
  return Math.random().toString(36).substring(2, 8);
}

// Command: add
function addNeed(description) {
  const needs = loadNeeds();
  const need = {
    id: generateId(),
    description: description.trim(),
    createdAt: new Date().toISOString(),
    status: 'pending',
    category: inferCategory(description)
  };
  needs.push(need);
  saveNeeds(needs);
  console.log(`✅ Need registered: #${need.id}`);
  console.log(`   "${need.description}"`);
  return need.id;
}

// Infer category based on text
function inferCategory(description) {
  const lower = description.toLowerCase();
  if (lower.includes('api') || lower.includes('endpoint')) return 'integration';
  if (lower.includes('metric') || lower.includes('log') || lower.includes('monitor')) return 'observability';
  if (lower.includes('deploy') || lower.includes('pipeline') || lower.includes('ci')) return 'devops';
  if (lower.includes('user') || lower.includes('auth') || lower.includes('login')) return 'auth';
  if (lower.includes('database') || lower.includes('db') || lower.includes('query')) return 'database';
  if (lower.includes('file') || lower.includes('storage') || lower.includes('upload')) return 'storage';
  return 'general';
}

// Command: list
function listNeeds() {
  const needs = loadNeeds();
  if (needs.length === 0) {
    console.log('📭 No needs registered yet.');
    return;
  }
  
  console.log(`📋 ${needs.length} need(s) registered:\n`);
  needs.forEach(n => {
    const date = new Date(n.createdAt).toLocaleDateString();
    const status = n.status === 'pending' ? '⏳' : '✅';
    console.log(`${status} #${n.id} [${n.category}] (${date})`);
    console.log(`   ${n.description}\n`);
  });
}

// Command: report (for cronjob)
function generateReport() {
  const needs = loadNeeds();
  const pending = needs.filter(n => n.status === 'pending');
  
  if (pending.length === 0) {
    return null;
  }
  
  // Group by category
  const byCategory = {};
  pending.forEach(n => {
    if (!byCategory[n.category]) byCategory[n.category] = [];
    byCategory[n.category].push(n);
  });
  
  // Format report
  let report = `🪄 **Magic Need Report** — ${pending.length} pending\n\n`;
  
  Object.entries(byCategory).forEach(([cat, items]) => {
    const emoji = getCategoryEmoji(cat);
    report += `${emoji} **${cat.toUpperCase()}** (${items.length})\n`;
    items.forEach(n => {
      report += `  • ${n.description}\n`;
    });
    report += '\n';
  });
  
  report += `_Total needs registered: ${needs.length} | Generated: ${new Date().toLocaleString()}_`;
  
  return report;
}

function getCategoryEmoji(cat) {
  const emojis = {
    integration: '🔌',
    observability: '📊',
    devops: '🚀',
    auth: '🔐',
    database: '🗄️',
    storage: '📁',
    general: '📝'
  };
  return emojis[cat] || '📝';
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

// If no args, or first arg is not a known command, treat as description
const knownCommands = ['add', 'list', 'report', 'clear', '--help', '-h'];
const isCommand = command && knownCommands.includes(command);

if (!isCommand) {
  // Description passed directly
  const description = args.join(' ');
  if (!description) {
    console.log('Usage: cli.js "description of the need"');
    process.exit(1);
  }
  addNeed(description);
} else if (command === 'add') {
  const description = args.slice(1).join(' ');
  if (!description) {
    console.log('Usage: cli.js add "description of the need"');
    process.exit(1);
  }
  addNeed(description);
} else if (command === 'list') {
  listNeeds();
} else if (command === 'report') {
  const report = generateReport();
  if (report) {
    console.log(report);
  } else {
    console.log('NO_REPORT');
  }
} else if (command === 'clear') {
  const needs = loadNeeds();
  const pending = needs.filter(n => n.status === 'pending');
  if (pending.length === 0) {
    console.log('No pending needs to clear.');
  } else {
    needs.forEach(n => {
      if (n.status === 'pending') n.status = 'archived';
    });
    saveNeeds(needs);
    console.log(`🗑️ ${pending.length} need(s) archived.`);
  }
} else {
  console.log(`
🪄 magic-need CLI

Usage:
  cli.js "description"     Register a new need
  cli.js list              List all needs
  cli.js report            Generate report for cronjob
  cli.js clear             Archive pending needs

The agent can use this when it identifies it needs
a tool or data that is not available.
  `);
}
