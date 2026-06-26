#!/usr/bin/env node

/**
 * Memory Transfer - Transfer memory between OpenClaw agents
 * Supports: topic filtering, memory sharing (filtered), memory cloning (verbatim)
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const WORKSPACE_BASE = '/home/node/.openclaw';

// Known agent workspaces
const AGENT_WORKSPACES = {
  'main': 'workspace-main',
  'coder': 'workspace-coder',
  'doc-analyst': 'workspace-doc',
  'daily-money': 'workspace-daily-money',
  'skill-master': 'workspace-skill-master'
};

// User information patterns to filter in share mode
const USER_INFO_PATTERNS = [
  // User name patterns
  /我的名字叫[^\n，。,.]+/g,
  /我叫[^\n，。,.]+/g,
  /我叫.*/g,
  /用户.*名字/g,
  /username.*?:.*/gi,
  /name.*?:.*/gi,
  // User preferences that should not be shared
  /我喜欢[^\n，。,.]+/g,
  /我讨厌[^\n，。,.]+/g,
  /我的爱好/g,
  /我的兴趣/g,
  // User personal info
  /我的邮箱是[^\n，。,.]+/g,
  /我的电话[^\n，。,.]+/g,
  /我的地址[^\n，。,.]+/g,
  /我的生日[^\n，。,.]+/g,
  /我的年龄/g,
  // About the user - should be excluded
  /关于我/g,
  /我的个人/g,
  // Reference to user in third person
  /用户[^\n，。,.]+/g,
];

function getWorkspacePath(agentId) {
  const workspaceName = AGENT_WORKSPACES[agentId];
  if (workspaceName) {
    return path.join(WORKSPACE_BASE, workspaceName);
  }
  const workspacePath = path.join(WORKSPACE_BASE, `workspace-${agentId}`);
  if (fs.existsSync(workspacePath)) {
    return workspacePath;
  }
  return path.join(WORKSPACE_BASE, agentId);
}

function filterUserInfo(text) {
  let result = text;
  USER_INFO_PATTERNS.forEach(pattern => {
    result = result.replace(pattern, '');
  });
  // Clean up empty lines from filtering
  const lines = result.split('\n');
  const filteredLines = lines.filter(line => line.trim().length > 0);
  return filteredLines.join('\n');
}

function transformForTarget(text, targetAgentId, sourceAgentId, targetAgentName, sourceAgentName) {
  let result = text;
  
  const targetName = targetAgentName || `Agent ${targetAgentId.charAt(0).toUpperCase() + targetAgentId.slice(1)}`;
  const sourceName = sourceAgentName || `Agent ${sourceAgentId.charAt(0).toUpperCase() + sourceAgentId.slice(1)}`;
  
  // Transformations: convert first-person source agent experience to third-person
  const transformations = [
    // First person → third person (source agent)
    { pattern: /\bI\b/g, replacement: sourceName },
    { pattern: /\bme\b/g, replacement: sourceName },
    { pattern: /\bmy\b/g, replacement: `${sourceName}'s` },
    { pattern: /\bmine\b/g, replacement: `${sourceName}'s` },
    { pattern: /\bmyself\b/g, replacement: `${sourceName}self` },
    
    // Contractions
    { pattern: /\bI'm\b/g, replacement: `${sourceName} is` },
    { pattern: /\bI've\b/g, replacement: `${sourceName} has` },
    { pattern: /\bI'll\b/g, replacement: `${sourceName} will` },
    { pattern: /\bI'd\b/g, replacement: `${sourceName} would` },
    { pattern: /\bwas\b/g, replacement: 'was' }, // Keep
    
    // Role references
    { pattern: /Agent\s+\w+/gi, replacement: targetName },
    { pattern: /\bI work as\b/gi, replacement: `${targetName} works as` },
    { pattern: /\bI serve as\b/gi, replacement: `${targetName} serves as` },
    { pattern: /\bI act as\b/gi, replacement: `${targetName} acts as` },
    { pattern: /\bI function as\b/gi, replacement: `${targetName} functions as` },
    { pattern: /\bmy role is\b/gi, replacement: `${targetName}'s role is` },
    { pattern: /\bmy purpose is\b/gi, replacement: `${targetName}'s purpose is` },
    { pattern: /\bI was created\b/gi, replacement: `${targetName} was created` },
    { pattern: /\bI was trained\b/gi, replacement: `${targetName} was trained` },
    
    // Cognitive verbs
    { pattern: /\bI think\b/gi, replacement: `${sourceName} thinks` },
    { pattern: /\bI believe\b/gi, replacement: `${sourceName} believes` },
    { pattern: /\bI know\b/gi, replacement: `${sourceName} knows` },
    { pattern: /\bI understand\b/gi, replacement: `${sourceName} understands` },
    { pattern: /\bI remember\b/gi, replacement: `${sourceName} remembers` },
    { pattern: /\bI prefer\b/gi, replacement: `${sourceName} prefers` },
    { pattern: /\bI like\b/gi, replacement: `${sourceName} likes` },
    { pattern: /\bI want\b/gi, replacement: `${sourceName} wants` },
    { pattern: /\bI need\b/gi, replacement: `${sourceName} needs` },
    { pattern: /\bI bought\b/gi, replacement: `${sourceName} bought` },
    { pattern: /\bI have\b/gi, replacement: `${sourceName} has` },
    { pattern: /\bI did\b/gi, replacement: `${sourceName} did` },
  ];
  
  transformations.forEach(({ pattern, replacement }) => {
    result = result.replace(pattern, replacement);
  });
  
  return result;
}

function filterByTopic(content, topic) {
  if (!topic) return true;
  const lowerContent = content.toLowerCase();
  const lowerTopic = topic.toLowerCase();
  return lowerContent.includes(lowerTopic);
}

function createInterface() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
}

function question(rl, query) {
  return new Promise((resolve) => {
    rl.question(query, (answer) => resolve(answer));
  });
}

async function interactiveMode(sourceId, targetId) {
  const rl = createInterface();
  
  console.log('\n🗣️  Interactive Memory Transfer Mode\n');
  console.log(`   Source: ${sourceId}`);
  console.log(`   Target: ${targetId}\n`);
  
  const topic = await question(rl, '📌 Topic filter (optional, press Enter for all): ');
  console.log(`   Topic: ${topic || 'all memories'}`);
  
  console.log('\n📋 Select transfer mode:');
  console.log('   [share] - Share knowledge/context (filter user info, adapt to target agent)');
  console.log('   [clone] - Clone verbatim (keep everything as-is)');
  const mode = await question(rl, '   Mode (share/clone): ');
  const selectedMode = mode.toLowerCase().trim() || 'share';
  console.log(`   Mode: ${selectedMode}\n`);
  
  const confirm = await question(rl, '✅ Confirm transfer? (yes/no): ');
  if (confirm.toLowerCase() !== 'yes' && confirm.toLowerCase() !== 'y') {
    console.log('\n❌ Transfer cancelled.');
    rl.close();
    return false;
  }
  
  rl.close();
  return { topic: topic.trim() || null, mode: selectedMode };
}

function listMemories(agentId) {
  const workspace = getWorkspacePath(agentId);
  
  console.log(`\n📁 Memories for agent: ${agentId}`);
  console.log(`   Workspace: ${workspace}\n`);
  
  if (!fs.existsSync(workspace)) {
    console.log(`❌ Workspace not found: ${workspace}`);
    return false;
  }
  
  const memories = [];
  
  const mainMemory = path.join(workspace, 'MEMORY.md');
  if (fs.existsSync(mainMemory)) {
    const stats = fs.statSync(mainMemory);
    const content = fs.readFileSync(mainMemory, 'utf8');
    memories.push({
      name: 'MEMORY.md',
      path: mainMemory,
      size: stats.size,
      type: 'long-term',
      content
    });
  }
  
  const memoryDir = path.join(workspace, 'memory');
  if (fs.existsSync(memoryDir)) {
    const files = fs.readdirSync(memoryDir)
      .filter(f => f.endsWith('.md'));
    
    files.forEach(f => {
      const filePath = path.join(memoryDir, f);
      const stats = fs.statSync(filePath);
      const content = fs.readFileSync(filePath, 'utf8');
      memories.push({
        name: f,
        path: filePath,
        size: stats.size,
        type: 'daily',
        content
      });
    });
  }
  
  if (memories.length === 0) {
    console.log('   No memory files found.');
    return false;
  }
  
  memories.forEach(m => {
    const icon = m.type === 'long-term' ? '📌' : '📄';
    console.log(`   ${icon} ${m.name} (${m.size} bytes)`);
  });
  
  return memories;
}

function transferMemory(sourceId, targetId, options = {}) {
  const { topic = null, mode = 'share', dryRun = false, file = null } = options;
  const sourceWorkspace = getWorkspacePath(sourceId);
  const targetWorkspace = getWorkspacePath(targetId);
  
  console.log(`\n🔄 Transferring memory: ${sourceId} → ${targetId}`);
  console.log(`   From: ${sourceWorkspace}`);
  console.log(`   To:   ${targetWorkspace}`);
  console.log(`   Mode: ${mode === 'share' ? 'share (filter user info + adapt to target)' : 'clone (verbatim)'}`);
  if (topic) console.log(`   Topic filter: ${topic}`);
  console.log('');
  
  if (!fs.existsSync(sourceWorkspace)) {
    console.log(`❌ Source workspace not found: ${sourceWorkspace}`);
    return false;
  }
  
  if (!fs.existsSync(targetWorkspace)) {
    console.log(`❌ Target workspace not found: ${targetWorkspace}`);
    return false;
  }
  
  const sourceMemories = listMemories(sourceId);
  if (!sourceMemories) {
    console.log('❌ No memories to transfer');
    return false;
  }
  
  let toTransfer = sourceMemories;
  
  if (file) {
    toTransfer = toTransfer.filter(m => m.name === file);
    if (toTransfer.length === 0) {
      console.log(`❌ File not found: ${file}`);
      return false;
    }
  }
  
  if (topic) {
    toTransfer = toTransfer.filter(m => filterByTopic(m.content, topic));
    if (toTransfer.length === 0) {
      console.log(`❌ No memories found matching topic: ${topic}`);
      return false;
    }
  }
  
  if (dryRun) {
    console.log('\n🔍 Dry run - following files would be transferred:\n');
    toTransfer.forEach(m => {
      console.log(`   ${m.name} (${m.size} bytes)`);
      if (mode === 'share') {
        console.log(`      Mode: share (user info filtered, adapted to target agent)`);
      } else {
        console.log(`      Mode: clone (verbatim)`);
      }
    });
    console.log('\n✅ Dry run complete (no files copied)');
    return true;
  }
  
  const targetMemoryDir = path.join(targetWorkspace, 'memory');
  if (!fs.existsSync(targetMemoryDir)) {
    fs.mkdirSync(targetMemoryDir, { recursive: true });
  }
  
  let transferred = 0;
  let filtered = 0;
  
  toTransfer.forEach(m => {
    let targetPath;
    let content = m.content;
    
    if (mode === 'share') {
      // In share mode: filter user info first, then adapt to target agent
      const beforeFilter = content.length;
      content = filterUserInfo(content);
      const afterFilter = content.length;
      filtered += (beforeFilter - afterFilter);
      
      // Then transform for target agent identity
      content = transformForTarget(content, targetId, sourceId, null, null);
    }
    
    if (m.name === 'MEMORY.md') {
      targetPath = path.join(targetWorkspace, 'MEMORY.md');
    } else {
      targetPath = path.join(targetMemoryDir, m.name);
    }
    
    if (fs.existsSync(targetPath)) {
      const backupPath = targetPath + '.backup';
      fs.renameSync(targetPath, backupPath);
      console.log(`   ⚠️ Backed up existing: ${m.name} → ${m.name}.backup`);
    }
    
    fs.writeFileSync(targetPath, content);
    console.log(`   ✅ Copied: ${m.name} (${mode === 'share' ? 'shared (adapted to target)' : 'cloned'})`);
    transferred++;
  });
  
  console.log(`\n✅ Transferred ${transferred} file(s)`);
  if (mode === 'share' && filtered > 0) {
    console.log(`   📝 Filtered ${filtered} characters of user info`);
  }
  return true;
}

function searchMemories(agentId, topic) {
  const workspace = getWorkspacePath(agentId);
  
  console.log(`\n🔍 Searching memories for "${topic}" in ${agentId}\n`);
  
  if (!fs.existsSync(workspace)) {
    console.log(`❌ Workspace not found: ${workspace}`);
    return false;
  }
  
  const results = [];
  
  const mainMemory = path.join(workspace, 'MEMORY.md');
  if (fs.existsSync(mainMemory)) {
    const content = fs.readFileSync(mainMemory, 'utf8');
    if (filterByTopic(content, topic)) {
      results.push({ file: 'MEMORY.md', matches: content.split('\n').filter(l => filterByTopic(l, topic)) });
    }
  }
  
  const memoryDir = path.join(workspace, 'memory');
  if (fs.existsSync(memoryDir)) {
    const files = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md'));
    
    files.forEach(f => {
      const filePath = path.join(memoryDir, f);
      const content = fs.readFileSync(filePath, 'utf8');
      if (filterByTopic(content, topic)) {
        const matches = content.split('\n').filter(l => filterByTopic(l, topic));
        results.push({ file: f, matches });
      }
    });
  }
  
  if (results.length === 0) {
    console.log('   No matches found.');
    return false;
  }
  
  results.forEach(r => {
    console.log(`📄 ${r.file}:`);
    r.matches.forEach(m => console.log(`   ${m.substring(0, 100)}...`));
    console.log('');
  });
  
  return results;
}

function listAgents() {
  console.log('\n📋 Available agents:\n');
  
  Object.entries(AGENT_WORKSPACES).forEach(([id, workspace]) => {
    const workspacePath = path.join(WORKSPACE_BASE, workspace);
    const exists = fs.existsSync(workspacePath);
    const icon = exists ? '✅' : '❌';
    console.log(`   ${icon} ${id} → ${workspacePath}`);
  });
  
  console.log('');
  return AGENT_WORKSPACES;
}

// Main
const args = process.argv.slice(2);
const command = args[0];

console.log('📦 Memory Transfer Tool v2.1');
console.log('============================\n');

switch (command) {
  case 'list':
    if (args[1]) {
      listMemories(args[1]);
    } else {
      console.log('Usage: memory-transfer list <agent-id>');
    }
    break;
    
  case 'search':
    if (args[1] && args[2]) {
      searchMemories(args[1], args[2]);
    } else {
      console.log('Usage: memory-transfer search <agent-id> <topic>');
    }
    break;
    
  case 'agents':
    listAgents();
    break;
    
  case 'transfer':
    const dryRun = args.includes('--dry-run');
    
    let topic = null;
    let mode = 'share';
    let file = null;
    
    for (let i = 1; i < args.length; i++) {
      if (args[i] === '--topic' && args[i + 1]) {
        topic = args[i + 1];
        i++;
      } else if (args[i] === '--mode' && args[i + 1]) {
        mode = args[i + 1];
        i++;
      } else if (!args[i].startsWith('--') && args[i] !== 'transfer') {
        if (!file) file = args[i];
      }
    }
    
    const source = args[1];
    const target = args[2];
    
    if (!source || !target) {
      console.log('Usage: memory-transfer transfer <source> <target> [file] [options]');
      console.log('\nOptions:');
      console.log('  --mode <share|clone|interactive>  Transfer mode (default: share)');
      console.log('  --topic <keyword>                  Filter by topic keyword');
      console.log('  --dry-run                         Preview only');
      console.log('\nMode details:');
      console.log('  share       - Filter user info, adapt to target agent (knowledge sharing)');
      console.log('  clone       - Keep original verbatim (for backup/migration)');
      console.log('\nExamples:');
      console.log('  memory-transfer transfer main coder');
      console.log('  memory-transfer transfer main coder --mode share');
      console.log('  memory-transfer transfer main coder --mode clone');
      console.log('  memory-transfer transfer main coder --topic project');
      console.log('  memory-transfer transfer main coder --mode interactive');
      console.log('  memory-transfer transfer main coder --dry-run');
    } else {
      transferMemory(source, target, { topic, mode, dryRun, file });
    }
    break;
    
  case 'help':
  default:
    console.log(`
📦 Memory Transfer v2.1 - Enhanced with user info filtering

Usage:
  memory-transfer agents              List all available agents
  memory-transfer list <agent>       List memories for an agent
  memory-transfer search <agent> <topic>  Search memories by topic
  memory-transfer transfer <src> <dst> [file]  Transfer memory

Options:
  --mode <share|clone|interactive>  Transfer mode (default: share)
    share       - Filter user info, adapt to target agent (knowledge sharing)
    clone       - Keep original verbatim (backup/migration)
    interactive - Prompt for all options
  --topic <keyword>                  Filter memories by topic
  --dry-run                         Preview only

Share Mode Filtering (removed from transfer):
  - User names: 我叫..., 我的名字...
  - User preferences: 我喜欢..., 我讨厌...
  - User personal info: email, phone, address
  - About user: 关于我...
  
Share Mode Transformation (adapt to target agent):
  - Identity: "Agent X" → target agent name
  - Roles: "I work as helper" → "I work as Agent Skill Master"
  - First-person: I, my, me remain as first-person (adopts knowledge as own)

Examples:
  memory-transfer agents
  memory-transfer list main
  memory-transfer search main preferences
  memory-transfer transfer main coder
  memory-transfer transfer main coder --mode share
  memory-transfer transfer main coder --mode clone
  memory-transfer transfer main coder --topic project
  memory-transfer transfer main coder --mode interactive
  memory-transfer transfer main coder --dry-run
`);
}
