#!/usr/bin/env node
/**
 * NIMA Process Guard for Node.js
 * Prevents multiple gateway instances from running simultaneously
 * 
 * Usage (at top of index.js):
 *   const guard = require('./process_guard');
 *   guard.acquireGatewayLock();
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const PID_DIR = path.join(os.homedir(), '.nima', 'run');
const PID_FILE = path.join(PID_DIR, 'gateway.pid');

function ensurePidDir() {
    if (!fs.existsSync(PID_DIR)) {
        fs.mkdirSync(PID_DIR, { recursive: true });
    }
}

function isProcessRunning(pid) {
    try {
        process.kill(pid, 0);
        return true;
    } catch (e) {
        return false;
    }
}

function getRunningGatewayPid() {
    if (!fs.existsSync(PID_FILE)) {
        return null;
    }
    
    try {
        const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8').trim());
        if (isProcessRunning(pid)) {
            // Check if it's actually a gateway process
            try {
                const cmdline = fs.readFileSync(`/proc/${pid}/cmdline`, 'utf8').replace(/\0/g, ' ');
                if (cmdline.includes('openclaw') || cmdline.includes('gateway')) {
                    return pid;
                }
            } catch (e) {
                // Can't read cmdline on macOS, assume it's valid
                return pid;
            }
            return pid;
        }
        // Process dead - zombie
        return 'zombie';
    } catch (e) {
        return null;
    }
}

function acquireGatewayLock() {
    ensurePidDir();
    
    const existingPid = getRunningGatewayPid();
    
    if (existingPid && existingPid !== 'zombie') {
        console.error(`❌ Gateway already running (PID ${existingPid})`);
        console.error('Stop it first: kill ' + existingPid + ' or "openclaw gateway stop"');
        process.exit(1);
    }
    
    if (existingPid === 'zombie') {
        console.log('ℹ️  Found zombie gateway PID, cleaning up...');
        try {
            fs.unlinkSync(PID_FILE);
        } catch (e) {
            // Ignore
        }
    }
    
    // Write our PID
    fs.writeFileSync(PID_FILE, process.pid.toString());
    
    // Register cleanup
    process.on('exit', releaseGatewayLock);
    process.on('SIGTERM', () => { releaseGatewayLock(); process.exit(0); });
    process.on('SIGINT', () => { releaseGatewayLock(); process.exit(0); });
    
    console.log(`✅ Gateway lock acquired (PID ${process.pid})`);
}

function releaseGatewayLock() {
    try {
        if (fs.existsSync(PID_FILE)) {
            const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8').trim());
            if (pid === process.pid) {
                fs.unlinkSync(PID_FILE);
                console.log('ℹ️  Gateway lock released');
            }
        }
    } catch (e) {
        // Ignore cleanup errors
    }
}

function checkDatabaseLock(dbPath) {
    // Simple check - try to open db file for writing
    try {
        const fd = fs.openSync(dbPath, 'r+');
        try {
            fs.flockSync(fd, fs.constants.LOCK_EX | fs.constants.LOCK_NB);
            fs.flockSync(fd, fs.constants.LOCK_UN);
            fs.closeSync(fd);
            return false; // Not locked
        } catch (e) {
            fs.closeSync(fd);
            return true; // Locked by another process
        }
    } catch (e) {
        return false; // Assume free on error
    }
}

module.exports = {
    acquireGatewayLock,
    releaseGatewayLock,
    checkDatabaseLock,
    getRunningGatewayPid
};
