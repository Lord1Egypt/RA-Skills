#!/usr/bin/env node

/**
 * Continuous Learning Analysis Script
 * Analyzes actual session history from OpenClaw agents
 * 
 * Usage:
 *   node analyze.mjs              # Run analysis
 *   node analyze.mjs list        # Show optimizations
 *   node analyze.mjs instincts   # Show instincts
 *   node analyze.mjs patterns    # Show patterns
 *   node analyze.mjs errors      # Show error patterns
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Paths - use relative resolution for portability
const SKILL_DIR = join(__dirname, '..');
const WORKSPACE = join(SKILL_DIR, '..', '..');
const AGENTS_DIR = join(process.env.HOME || join(process.env.USERPROFILE || '/home/user'), '.openclaw', 'agents');
const MEMORY_DIR = join(WORKSPACE, 'memory', 'learning');
const INSTINCTS_FILE = join(MEMORY_DIR, 'instincts.jsonl');
const PATTERNS_FILE = join(MEMORY_DIR, 'patterns.json');
const OPTIMIZATIONS_FILE = join(MEMORY_DIR, 'optimizations.json');

// Ensure directory exists
if (!existsSync(MEMORY_DIR)) {
  mkdirSync(MEMORY_DIR, { recursive: true });
}

// Initialize files if not exist
if (!existsSync(INSTINCTS_FILE)) {
  writeFileSync(INSTINCTS_FILE, '');
}
if (!existsSync(PATTERNS_FILE)) {
  writeFileSync(PATTERNS_FILE, JSON.stringify({ patterns: [] }, null, 2));
}
if (!existsSync(OPTIMIZATIONS_FILE)) {
  writeFileSync(OPTIMIZATIONS_FILE, JSON.stringify({ optimizations: [] }, null, 2));
}

function loadPatterns() {
  try {
    return JSON.parse(readFileSync(PATTERNS_FILE, 'utf-8')).patterns || [];
  } catch {
    return [];
  }
}

function savePatterns(patterns) {
  writeFileSync(PATTERNS_FILE, JSON.stringify({ patterns }, null, 2));
}

function loadOptimizations() {
  try {
    return JSON.parse(readFileSync(OPTIMIZATIONS_FILE, 'utf-8')).optimizations || [];
  } catch {
    return [];
  }
}

function saveOptimizations(optimizations) {
  writeFileSync(OPTIMIZATIONS_FILE, JSON.stringify({ optimizations }, null, 2));
}

function loadInstincts() {
  try {
    const content = readFileSync(INSTINCTS_FILE, 'utf-8');
    return content.trim().split('\n').filter(l => l).map(l => JSON.parse(l));
  } catch {
    return [];
  }
}

function saveInstincts(instincts) {
  writeFileSync(INSTINCTS_FILE, instincts.map(i => JSON.stringify(i)).join('\n') + '\n');
}

function addInstinct(id, domain, trigger, confidence = 0.3, evidence = []) {
  const existing = loadInstincts();
  const existingIdx = existing.findIndex(i => i.id === id);
  
  const instinct = {
    id,
    domain,
    trigger,
    confidence,
    source: 'session-observation',
    created: new Date().toISOString(),
    evidence,
    updated: new Date().toISOString()
  };
  
  if (existingIdx >= 0) {
    const old = existing[existingIdx];
    instinct.confidence = Math.min(0.9, old.confidence + 0.1);
    instinct.evidence = [...old.evidence, ...evidence].slice(-10);
    existing[existingIdx] = instinct;
    saveInstincts(existing);
    console.log(`✓ Updated instinct: ${id} (${old.confidence} → ${instinct.confidence})`);
  } else {
    existing.push(instinct);
    saveInstincts(existing);
    console.log(`✓ Added instinct: ${id}`);
  }
  
  return instinct;
}

function getSessionFiles(agentDir) {
  const sessionsDir = join(agentDir, 'sessions');
  if (!existsSync(sessionsDir)) return [];
  
  try {
    return readdirSync(sessionsDir)
      .filter(f => f.endsWith('.jsonl'))
      .map(f => join(sessionsDir, f));
  } catch {
    return [];
  }
}

function parseJsonl(content) {
  return content.trim().split('\n')
    .filter(l => l.trim())
    .map(l => {
      try {
        return JSON.parse(l);
      } catch {
        return null;
      }
    })
    .filter(Boolean);
}

// Extract tool calls and errors from message content
function extractToolCalls(messages) {
  const toolCalls = [];
  const errors = [];
  
  for (const msg of messages) {
    // Look for toolResult messages - these contain actual tool executions
    if (msg.type === 'message' && msg.message?.role === 'toolResult') {
      const toolName = msg.message?.toolName;
      const content = msg.message?.content?.[0]?.text || '';
      
      if (toolName) {
        toolCalls.push({
          tool: toolName.toLowerCase(),
          timestamp: msg.timestamp
        });
        
        // Check for errors in tool results
        if (content.includes('"status": "error"') || 
            content.toLowerCase().includes('error') ||
            content.toLowerCase().includes('failed')) {
          // Extract error message
          let errorMsg = content;
          try {
            const parsed = JSON.parse(content);
            errorMsg = parsed.error || parsed.message || content.substring(0, 100);
          } catch {}
          
          errors.push({
            tool: toolName.toLowerCase(),
            message: errorMsg.substring(0, 150),
            timestamp: msg.timestamp
          });
        }
      }
    }
    
    // Also look for tool calls (assistant making tool calls)
    if (msg.type === 'message' && msg.message?.role === 'assistant') {
      const content = msg.message?.content || [];
      for (const block of content) {
        if (block.type === 'toolCall') {
          toolCalls.push({
            tool: block.name?.toLowerCase() || 'unknown',
            timestamp: msg.timestamp
          });
        }
      }
    }
  }
  
  return { toolCalls, errors };
}

function analyzeSessions() {
  console.log('\n🧠 Continuous Learning - Session Analysis\n');
  console.log('═'.repeat(50));
  
  const allToolCalls = [];
  const allErrors = [];
  const toolCounts = {};
  const errorPatterns = {};
  
  if (!existsSync(AGENTS_DIR)) {
    console.log('⚠️ No agents directory found');
    return { toolCalls: [], errors: [], patterns: [] };
  }
  
  const agentDirs = readdirSync(AGENTS_DIR).filter(d => 
    existsSync(join(AGENTS_DIR, d, 'sessions'))
  );
  
  console.log(`\n📂 Found ${agentDirs.length} agents with sessions\n`);
  
  for (const agentDir of agentDirs) {
    const sessionFiles = getSessionFiles(join(AGENTS_DIR, agentDir));
    
    for (const sessionFile of sessionFiles.slice(-3)) { // Last 3 sessions per agent
      try {
        const content = readFileSync(sessionFile, 'utf-8');
        const messages = parseJsonl(content);
        
        const { toolCalls, errors } = extractToolCalls(messages);
        
        allToolCalls.push(...toolCalls);
        allErrors.push(...errors);
        
        for (const tc of toolCalls) {
          toolCounts[tc.tool] = (toolCounts[tc.tool] || 0) + 1;
        }
        
        for (const err of errors) {
          const key = `${err.tool}:${err.message.substring(0, 40)}`;
          errorPatterns[key] = (errorPatterns[key] || 0) + 1;
        }
      } catch (e) {
        // Skip unreadable files
      }
    }
  }
  
  console.log('📊 Session Statistics:');
  console.log(`   Total tool mentions: ${allToolCalls.length}`);
  console.log(`   Total errors detected: ${allErrors.length}`);
  console.log(`   Unique tools: ${Object.keys(toolCounts).length}`);
  
  // Top tools
  const topTools = Object.entries(toolCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);
  
  console.log('\n🔧 Top Tools:');
  topTools.forEach(([tool, count]) => {
    console.log(`   ${tool}: ${count}`);
  });
  
  // Error patterns
  const topErrors = Object.entries(errorPatterns)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);
  
  console.log('\n❌ Frequent Errors:');
  if (topErrors.length === 0) {
    console.log('   (No errors detected)');
  } else {
    topErrors.forEach(([pattern, count]) => {
      console.log(`   ${count}x: ${pattern.substring(0, 55)}`);
    });
  }
  
  // Generate insights
  const optimizations = [];
  
  // Detect message errors
  const msgErrors = allErrors.filter(e => e.tool === 'message');
  if (msgErrors.length > 2) {
    optimizations.push({
      id: 'discord-message-errors',
      title: 'Discord message errors detected',
      description: `${msgErrors.length} message tool errors. Check guildId and target format.`,
      impact: 'high',
      effort: 'low',
      category: 'errors'
    });
    
    // Learn instinct
    const errorSamples = msgErrors.slice(0, 3).map(e => e.message);
    addInstinct(
      'discord-message-requires-guild',
      'errors',
      'when sending Discord messages',
      0.6,
      errorSamples
    );
  }
  
  // Detect web_fetch errors
  const fetchErrors = allErrors.filter(e => e.tool === 'web_fetch');
  if (fetchErrors.length > 2) {
    optimizations.push({
      id: 'web-fetch-errors',
      title: 'Web fetch errors detected',
      description: `${fetchErrors.length} web fetch errors. Check URL validity.`,
      impact: 'medium',
      effort: 'low',
      category: 'errors'
    });
  }
  
  // Save patterns
  const existingPatterns = loadPatterns();
  const newPattern = {
    id: `analysis-${Date.now()}`,
    timestamp: new Date().toISOString(),
    toolCounts,
    errorCounts: Object.fromEntries(
      Object.entries(errorPatterns).map(([k, v]) => [k.substring(0, 30), v])
    ),
    sessionCount: agentDirs.length
  };
  
  savePatterns([...existingPatterns.slice(-49), newPattern]);
  
  // Save optimizations
  const existingOptimizations = loadOptimizations();
  const existingIds = new Set(existingOptimizations.map(o => o.id));
  
  for (const opt of optimizations) {
    if (!existingIds.has(opt.id)) {
      existingOptimizations.push(opt);
    }
  }
  
  saveOptimizations(existingOptimizations);
  
  console.log('\n📈 Analysis Complete');
  console.log('═'.repeat(50));
  
  return { toolCounts, errors: allErrors, patterns: newPattern, optimizations };
}

function listInstincts() {
  console.log('\n🧠 Learned Instincts\n');
  console.log('═'.repeat(40));
  
  const instincts = loadInstincts();
  
  if (instincts.length === 0) {
    console.log('No instincts learned yet.\n');
    return;
  }
  
  instincts.forEach(instinct => {
    const conf = instinct.confidence || 0;
    const emoji = conf >= 0.7 ? '🟢' : conf >= 0.5 ? '🟡' : '🔴';
    console.log(`${emoji} ${instinct.id}`);
    console.log(`   Domain: ${instinct.domain} | Confidence: ${conf}`);
    console.log(`   Trigger: ${instinct.trigger}`);
    if (instinct.evidence?.length > 0) {
      console.log(`   Evidence: ${instinct.evidence.length} items`);
    }
    console.log('');
  });
  
  console.log(`Total: ${instincts.length} instincts`);
}

function listOptimizations() {
  console.log('\n💡 Suggested Optimizations\n');
  console.log('═'.repeat(40));
  
  const optimizations = loadOptimizations();
  
  if (optimizations.length === 0) {
    console.log('No optimizations suggested yet.\n');
    return;
  }
  
  optimizations.forEach((opt, i) => {
    const impact = opt.impact === 'high' ? '🟢' : opt.impact === 'medium' ? '🟡' : '🔴';
    console.log(`${i + 1}. ${opt.title} ${impact}`);
    console.log(`   ${opt.description}`);
    console.log(`   Impact: ${opt.impact} | Effort: ${opt.effort}`);
    console.log('');
  });
  
  console.log(`Total: ${optimizations.length} optimizations`);
}

function listPatterns() {
  console.log('\n📊 Stored Patterns\n');
  console.log('═'.repeat(40));
  
  const patterns = loadPatterns();
  
  if (patterns.length === 0) {
    console.log('No patterns recorded yet.\n');
    return;
  }
  
  console.log(`Last ${patterns.length} analysis runs:`);
  patterns.slice(-5).forEach((p, i) => {
    console.log(`\n${i + 1}. ${p.timestamp?.substring(0, 10)}`);
    if (p.toolCounts) {
      const top = Object.entries(p.toolCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3);
      console.log(`   Top tools: ${top.map(([k, v]) => `${k}(${v})`).join(', ')}`);
    }
  });
}

// CLI
const args = process.argv.slice(2);
const command = args[0] || 'analyze';

if (command === 'analyze') {
  analyzeSessions();
} else if (command === 'instincts') {
  listInstincts();
} else if (command === 'optimizations' || command === 'list') {
  listOptimizations();
} else if (command === 'patterns') {
  listPatterns();
} else if (command === 'errors') {
  const result = analyzeSessions();
  console.log('\n❌ All Detected Errors:');
  result.errors.forEach((e, i) => {
    console.log(`${i + 1}. [${e.tool}] ${e.message.substring(0, 80)}`);
  });
} else if (command === 'help') {
  console.log('Usage:');
  console.log('  node analyze.mjs           # Analyze sessions');
  console.log('  node analyze.mjs instincts # List instincts');
  console.log('  node analyze.mjs list      # List optimizations');
  console.log('  node analyze.mjs patterns # List patterns');
  console.log('  node analyze.mjs errors    # Show all errors');
} else {
  console.log('Unknown command:', command);
}
