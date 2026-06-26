#!/usr/bin/env node

/**
 * Simple Memory Management
 * Save, retrieve, and search memories
 */

const fs = require('fs');
const path = require('path');

const MEMORIES_FILE = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace', 'memories.json');

// Load memories from file
function loadMemories() {
  try {
    if (fs.existsSync(MEMORIES_FILE)) {
      const data = fs.readFileSync(MEMORIES_FILE, 'utf8');
      return JSON.parse(data);
    }
    return {};
  } catch (error) {
    return {};
  }
}

// Save memories to file
function saveMemories(memories) {
  const dir = path.dirname(MEMORIES_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(MEMORIES_FILE, JSON.stringify(memories, null, 2));
}

// Save a memory
function saveMemory(key, value) {
  const memories = loadMemories();
  memories[key] = {
    value,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
  saveMemories(memories);
  console.log(`✅ Saved memory: ${key}`);
  console.log(`   Value: ${value}`);
}

// Get a memory
function getMemory(key) {
  const memories = loadMemories();
  const memory = memories[key];

  if (!memory) {
    console.log(`❌ Memory not found: ${key}`);
    return;
  }

  console.log(`📝 ${key}`);
  console.log(`   Value: ${memory.value}`);
  console.log(`   Updated: ${new Date(memory.updatedAt).toLocaleString()}`);
}

// List all memories
function listMemories() {
  const memories = loadMemories();
  const keys = Object.keys(memories);

  if (keys.length === 0) {
    console.log('📝 No memories yet. Save one with "node memorize.js save <key> <value>"');
    return;
  }

  console.log('\n📝 Saved Memories');
  console.log('─'.repeat(80));

  // Sort by updatedAt (most recent first)
  const sorted = keys.sort((a, b) => {
    return new Date(memories[b].updatedAt) - new Date(memories[a].updatedAt);
  });

  sorted.forEach(key => {
    const memory = memories[key];
    const value = memory.value.length > 60 ? memory.value.substring(0, 60) + '...' : memory.value;
    const updated = new Date(memory.updatedAt).toLocaleString();
    console.log(`🔑 ${key}`);
    console.log(`   ${value}`);
    console.log(`   📅 ${updated}`);
    console.log();
  });
}

// Search memories
function searchMemories(keyword) {
  const memories = loadMemories();
  const keys = Object.keys(memories);
  const keywordLower = keyword.toLowerCase();

  const matches = keys.filter(key => {
    const memory = memories[key];
    return key.toLowerCase().includes(keywordLower) ||
           memory.value.toLowerCase().includes(keywordLower);
  });

  if (matches.length === 0) {
    console.log(`🔍 No memories found matching: ${keyword}`);
    return;
  }

  console.log(`\n🔍 Search results for "${keyword}"`);
  console.log('─'.repeat(80));

  matches.forEach(key => {
    const memory = memories[key];
    const value = memory.value.length > 60 ? memory.value.substring(0, 60) + '...' : memory.value;
    const updated = new Date(memory.updatedAt).toLocaleString();
    console.log(`🔑 ${key}`);
    console.log(`   ${value}`);
    console.log(`   📅 ${updated}`);
    console.log();
  });

  console.log(`\n✅ Found ${matches.length} match${matches.length !== 1 ? 'es' : ''}\n`);
}

// Delete a memory
function deleteMemory(key) {
  const memories = loadMemories();

  if (!memories[key]) {
    console.log(`❌ Memory not found: ${key}`);
    return;
  }

  delete memories[key];
  saveMemories(memories);
  console.log(`🗑️ Deleted memory: ${key}`);
}

// Show help
function showHelp() {
  console.log(`
📝 OpenClaw Memorize

Usage:
  node memorize.js save <key> <value>
  node memorize.js get <key>
  node memorize.js list
  node memorize.js search <keyword>
  node memorize.js delete <key>

Examples:
  node memorize.js save "model-choice" "Use Claude Sonnet 4.6"
  node memorize.js get "model-choice"
  node memorize.js list
  node memorize.js search "model"
  node memorize.js delete "model-choice"

Use Cases:
  📝 Project decisions
  👤 User preferences
  📊 Key metrics
  💡 Ideas
  🔗 Links
`);
}

// Main function
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'save': {
      const key = args[1];
      const value = args.slice(2).join(' ');

      if (!key || !value) {
        console.log('❌ Please provide both key and value');
        showHelp();
        process.exit(1);
      }

      saveMemory(key, value);
      break;
    }

    case 'get': {
      const key = args[1];
      if (!key) {
        console.log('❌ Please provide a key');
        showHelp();
        process.exit(1);
      }
      getMemory(key);
      break;
    }

    case 'list':
    case 'ls':
      listMemories();
      break;

    case 'search': {
      const keyword = args[1];
      if (!keyword) {
        console.log('❌ Please provide a search keyword');
        showHelp();
        process.exit(1);
      }
      searchMemories(keyword);
      break;
    }

    case 'delete':
    case 'del': {
      const key = args[1];
      if (!key) {
        console.log('❌ Please provide a key');
        showHelp();
        process.exit(1);
      }
      deleteMemory(key);
      break;
    }

    default:
      showHelp();
      break;
  }
}

main();
