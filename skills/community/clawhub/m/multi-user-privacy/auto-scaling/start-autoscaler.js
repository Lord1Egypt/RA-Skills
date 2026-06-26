#!/usr/bin/env node

/**
 * Session Auto-Scaler Service
 * 
 * Runs the auto-scaler as a background service.
 * Monitors session load and performs automatic scaling operations.
 */

const fs = require('fs');
const path = require('path');
const { getSessionAutoScaler } = require('./session-autoscaler');
const { getSessionManager } = require('../session-persistence/session-manager');

// Configuration
const PID_FILE = path.join(__dirname, 'autoscaler.pid');
const LOG_FILE = path.join(__dirname, 'logs', 'autoscaler.log');
const STATE_FILE = path.join(__dirname, '..', 'memory', 'autoscaler-state.json');

/**
 * Log function
 */
function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
  const logLine = `[${timestamp}] [${level}] ${message}`;
  console.log(logLine);
  
  // Write to log file
  const logDir = path.dirname(LOG_FILE);
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  fs.appendFileSync(LOG_FILE, logLine + '\n');
}

/**
 * Save PID file
 */
function savePid() {
  try {
    fs.writeFileSync(PID_FILE, process.pid.toString());
  } catch (error) {
    log('Failed to save PID file: ' + error.message, 'ERROR');
  }
}

/**
 * Remove PID file
 */
function removePid() {
  try {
    if (fs.existsSync(PID_FILE)) {
      fs.unlinkSync(PID_FILE);
    }
  } catch (error) {
    log('Failed to remove PID file: ' + error.message, 'ERROR');
  }
}

/**
 * Check if already running
 */
function isRunning() {
  if (!fs.existsSync(PID_FILE)) {
    return false;
  }
  
  try {
    const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8'));
    process.kill(pid, 0);
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Get PID
 */
function getPid() {
  if (!fs.existsSync(PID_FILE)) {
    return null;
  }
  
  try {
    return parseInt(fs.readFileSync(PID_FILE, 'utf8'));
  } catch (error) {
    return null;
  }
}

/**
 * Show status
 */
function showStatus() {
  if (isRunning()) {
    const pid = getPid();
    console.log('Auto-scaler is running (PID:', pid + ')');
    
    // Try to read state file
    if (fs.existsSync(STATE_FILE)) {
      try {
        const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
        console.log('Total Scale Ups:', state.totalScaleUps || 0);
        console.log('Total Scale Downs:', state.totalScaleDowns || 0);
        console.log('Total Merges:', state.totalMerges || 0);
        console.log('Last Scale Up:', state.lastScaleUp ? new Date(state.lastScaleUp).toISOString() : 'Never');
        console.log('Last Scale Down:', state.lastScaleDown ? new Date(state.lastScaleDown).toISOString() : 'Never');
      } catch (error) {
        // Ignore
      }
    }
  } else {
    console.log('Auto-scaler is not running');
  }
}

/**
 * Stop the service
 */
function stop() {
  if (!isRunning()) {
    console.log('Auto-scaler is not running');
    return;
  }
  
  const pid = getPid();
  console.log('Stopping auto-scaler (PID:', pid + ')...');
  
  try {
    process.kill(pid, 'SIGTERM');
    console.log('Stop signal sent');
    
    // Wait a bit and check
    setTimeout(() => {
      if (!isRunning()) {
        console.log('Auto-scaler stopped successfully');
        removePid();
      } else {
        console.log('Auto-scaler is still running, sending SIGKILL...');
        process.kill(pid, 'SIGKILL');
        removePid();
      }
    }, 2000);
  } catch (error) {
    console.error('Failed to stop:', error.message);
    removePid();
  }
}

/**
 * Start the service
 */
async function start() {
  if (isRunning()) {
    console.log('Auto-scaler is already running (PID:', getPid() + ')');
    return;
  }
  
  console.log('Starting auto-scaler...');
  
  try {
    // Initialize session manager
    log('Initializing Session Manager...');
    const sessionManager = getSessionManager();
    await sessionManager.initialize();
    log('Session Manager initialized');
    
    // Initialize auto-scaler
    log('Initializing Auto-Scaler...');
    const autoScaler = getSessionAutoScaler();
    await autoScaler.initialize();
    log('Auto-Scaler initialized');
    
    // Save PID
    savePid();
    log('Auto-scaler started (PID: ' + process.pid + ')');
    
    // Handle shutdown signals
    process.on('SIGTERM', () => {
      log('Received SIGTERM, shutting down...');
      autoScaler.stop();
      removePid();
      process.exit(0);
    });
    
    process.on('SIGINT', () => {
      log('Received SIGINT, shutting down...');
      autoScaler.stop();
      removePid();
      process.exit(0);
    });
    
    // Keep running
    log('Auto-scaler is now monitoring sessions');
    log('Press Ctrl+C to stop');
    
  } catch (error) {
    log('Failed to start: ' + error.message, 'ERROR');
    removePid();
    process.exit(1);
  }
}

// Command line interface
const command = process.argv[2];

switch (command) {
  case 'start':
    start();
    break;
    
  case 'stop':
    stop();
    break;
    
  case 'status':
    showStatus();
    break;
    
  case 'restart':
    stop();
    setTimeout(start, 2000);
    break;
    
  default:
    console.log('Usage: node start-autoscaler.js [start|stop|status|restart]');
    console.log();
    console.log('Commands:');
    console.log('  start   - Start the auto-scaler service');
    console.log('  stop    - Stop the auto-scaler service');
    console.log('  status  - Show service status');
    console.log('  restart - Restart the service');
    console.log();
    console.log('Examples:');
    console.log('  node start-autoscaler.js start');
    console.log('  node start-autoscaler.js status');
    console.log('  node start-autoscaler.js stop');
    process.exit(1);
}
