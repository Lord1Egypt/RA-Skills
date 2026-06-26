#!/usr/bin/env node
/**
 * dream.js - Dream cycle control script
 * 
 * Commands:
 *   --check --workspace <path>     Gate check result
 *   --count-sessions --workspace <path>  Session count
 *   --finalize --workspace <path>  Write lock timestamp
 *   --workspace <path>             Return config info
 */

const fs = require('fs');
const path = require('path');

function loadConfig(workspace) {
  const baseDir = path.dirname(path.dirname(__filename));
  const configPath = path.join(baseDir, 'assets', 'dream-config.json');
  
  if (!fs.existsSync(configPath)) {
    console.error(JSON.stringify({ error: 'Config not found', path: configPath }));
    process.exit(1);
  }
  
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  
  // Use workspace argument if provided, otherwise use config
  const ws = workspace || config.workspace;
  
  return {
    workspace: ws,
    sessionsPath: config.sessionsPath,
    dreamsDir: config.dreamsDir || path.join(ws, 'memory', 'dreams'),
    dreamLock: config.dreamLock || path.join(ws, 'memory', 'dreams', '.dream-lock'),
    baseDir
  };
}

function countSessions(sessionsPath) {
  if (!fs.existsSync(sessionsPath)) {
    return 0;
  }
  
  const files = fs.readdirSync(sessionsPath).filter(f => f.endsWith('.jsonl'));
  return files.length;
}

function getLastRun(dreamLockPath) {
  if (!fs.existsSync(dreamLockPath)) {
    return '0';
  }
  return fs.readFileSync(dreamLockPath, 'utf8').trim() || '0';
}

function needsReflection(dreamsDir) {
  if (!fs.existsSync(dreamsDir)) {
    return true;
  }
  
  // Get this week's range (Monday to Sunday)
  const now = new Date();
  const dayOfWeek = now.getDay();
  const diffToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
  const monday = new Date(now);
  monday.setDate(now.getDate() - diffToMonday);
  monday.setHours(0, 0, 0, 0);
  
  const files = fs.readdirSync(dreamsDir).filter(f => f.endsWith('.md') && !f.startsWith('.'));
  
  for (const file of files) {
    const filePath = path.join(dreamsDir, file);
    const stat = fs.statSync(filePath);
    if (stat.mtime >= monday) {
      return false; // Already done reflection this week
    }
  }
  
  return true; // No reflection this week yet
}

function doCheck(workspace) {
  const config = loadConfig(workspace);
  const sessionCount = countSessions(config.sessionsPath);
  const lastRun = getLastRun(config.dreamLock);
  const needsRef = needsReflection(config.dreamsDir);
  
  // Gate logic: sessionCount >= 5 OR >= 24h since last run
  const lastRunTs = parseInt(lastRun, 10) || 0;
  const now = Date.now();
  const hoursSince = (now - lastRunTs) / (1000 * 60 * 60);
  
  const passed = sessionCount >= 5 || hoursSince >= 24;
  
  return {
    passed,
    sessionCount,
    lastRun,
    needsReflection: needsRef
  };
}

function doCountSessions(workspace) {
  const config = loadConfig(workspace);
  const count = countSessions(config.sessionsPath);
  
  return {
    count,
    sessionsPath: config.sessionsPath
  };
}

function doFinalize(workspace) {
  const config = loadConfig(workspace);
  
  // Ensure dreamsDir exists
  const dreamsDir = path.dirname(config.dreamLock);
  if (!fs.existsSync(dreamsDir)) {
    fs.mkdirSync(dreamsDir, { recursive: true });
  }
  
  // Save previous value
  const prevPath = config.dreamLock + '.prev';
  if (fs.existsSync(config.dreamLock)) {
    const prev = fs.readFileSync(config.dreamLock, 'utf8');
    fs.writeFileSync(prevPath, prev);
  }
  
  // Write current timestamp
  const now = Date.now();
  fs.writeFileSync(config.dreamLock, now.toString());
  
  return {
    success: true,
    timestamp: now
  };
}

function doGetConfig(workspace) {
  return loadConfig(workspace);
}

// Main
const args = process.argv.slice(2);
let workspace = null;

// Parse arguments
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--workspace' && i + 1 < args.length) {
    workspace = args[i + 1];
    i++;
  }
}

// Determine command
if (args.includes('--check')) {
  console.log(JSON.stringify(doCheck(workspace), null, 2));
} else if (args.includes('--count-sessions')) {
  console.log(JSON.stringify(doCountSessions(workspace), null, 2));
} else if (args.includes('--finalize')) {
  console.log(JSON.stringify(doFinalize(workspace), null, 2));
} else {
  console.log(JSON.stringify(doGetConfig(workspace), null, 2));
}
