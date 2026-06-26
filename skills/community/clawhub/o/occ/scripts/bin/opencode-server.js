#!/usr/bin/env node

/**
 * OpenCode Server Executor CLI
 * Supports session query, creation, and continuation
 */

const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

async function checkAndInstallDependencies() {
  const scriptDir = path.join(__dirname, '..');
  const packageJsonPath = path.join(scriptDir, 'package.json');
  const nodeModulesPath = path.join(scriptDir, 'node_modules');
  
  if (!fs.existsSync(packageJsonPath)) {
    console.error('Error: package.json not found in', scriptDir);
    process.exit(1);
  }
  
  if (!fs.existsSync(nodeModulesPath)) {
    console.log('📦 Dependencies not found. Installing...');
    await installDependencies(scriptDir);
    console.log('✅ Dependencies installed successfully.');
  }
}

function installDependencies(scriptDir) {
  return new Promise((resolve, reject) => {
    const npmInstall = exec('npm install', { cwd: scriptDir });
    
    npmInstall.stdout.on('data', (data) => {
      process.stdout.write(data);
    });
    
    npmInstall.stderr.on('data', (data) => {
      process.stderr.write(data);
    });
    
    npmInstall.on('error', reject);
    npmInstall.on('close', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`npm install failed with code ${code}`));
      }
    });
  });
}

const { querySessions, createSession } = require('../src/services/session');
const { continueSession } = require('../src/services/message');

function showHelp() {
  console.log(`
OpenCode Server Executor CLI

Usage:
  opencode-server query              - List all sessions
  opencode-server create <task>      - Create new session with task
  opencode-server continue <id> <msg> - Send message to session
  opencode-server run <task>         - Create and run task in one command

Examples:
  opencode-server query
  opencode-server create 帮我创建一个React项目
  opencode-server continue abc123 确认继续
  opencode-server run 初始化一个新项目
`);
}

async function handleCommand(args) {
  const command = args[0];
  
  if (command === 'query' || command === 'list') {
    const result = await querySessions();
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
    return;
  }
  
  if (command === 'create') {
    const taskDescription = args.slice(1).join(' ') || 'New task';
    const result = await createSession(taskDescription);
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
    return;
  }
  
  if (command === 'continue') {
    const sessionId = args[1];
    const userInput = args.slice(2).join(' ');
    
    if (!sessionId) {
      console.error('Error: session ID required');
      console.error('Usage: opencode-server continue <sessionId> <message>');
      process.exit(1);
    }
    
    const result = await continueSession(sessionId, userInput);
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
    return;
  }
  
  showHelp();
}

async function main() {
  try {
    await checkAndInstallDependencies();
  } catch (error) {
    console.error('Error installing dependencies:', error.message);
    process.exit(1);
  }
  
  handleCommand(process.argv.slice(2)).catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
  });
}

main();