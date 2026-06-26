"use strict";
// Daemon lifecycle management for Memory Garden MCP skill
// IR-3: Health check verifies app marker
// IR-4: Shutdown method with PID file for orphan prevention
// MR-3: Spawn error handler for better diagnostics
// TC-4: Error messages with actionable guidance
// CR-1: PID verification before SIGTERM (prevent killing wrong process)
// CR-4: Safe HOME resolution with fallback + Startup race serialization
// CR-5: Null check for PID assignment + Symlink protection for PID file
// CR-11: Verify PATH candidates exist before returning
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.DaemonManager = void 0;
const child_process_1 = require("child_process");
const fs_1 = require("fs");
const path_1 = require("path");
const net = __importStar(require("net"));
// CR-4: Safe HOME resolution with fallback to USERPROFILE (Windows)
function getHomeDir() {
    const home = process.env.HOME || process.env.USERPROFILE;
    if (!home) {
        throw new Error('HOME environment variable not set. ' +
            'Set MG_DATA_DIR environment variable to specify data directory explicitly.');
    }
    return home;
}
const DEFAULT_PORT = 18790;
const MAX_PORT_ATTEMPTS = 10;
const HEALTH_TIMEOUT_MS = 5000;
const STARTUP_TIMEOUT_MS = 10000;
class DaemonManager {
    config;
    process = null;
    port;
    url;
    pid = null;
    pidFile;
    dataDir;
    // CR-4: Promise guard to serialize concurrent startup calls
    startPromise = null;
    constructor(config = {}) {
        this.config = config;
        this.port = config.port || DEFAULT_PORT;
        this.url = `http://127.0.0.1:${this.port}`;
        // CR-4: Use safe HOME resolution
        this.dataDir = config.dataDir || (0, path_1.join)(getHomeDir(), '.memory-garden');
        this.pidFile = (0, path_1.join)(this.dataDir, 'daemon.pid');
        // Ensure data directory exists
        if (!(0, fs_1.existsSync)(this.dataDir)) {
            (0, fs_1.mkdirSync)(this.dataDir, { recursive: true });
        }
        // IR-4: Register cleanup handlers
        process.on('SIGTERM', () => this.shutdown());
        process.on('SIGINT', () => this.shutdown());
    }
    // CR-4: Serialize concurrent startup calls with promise guard
    async ensureRunning() {
        // If startup already in progress, return the shared promise
        if (this.startPromise)
            return this.startPromise;
        // Check if already running (external or previous start)
        if (await this.isHealthy()) {
            return this.url;
        }
        // Start with serialization guard
        this.startPromise = this.doStart().finally(() => {
            this.startPromise = null;
        });
        return this.startPromise;
    }
    // CR-4: Actual startup logic, called through promise guard
    async doStart() {
        // Check for orphaned daemon from PID file
        await this.cleanupOrphan();
        // Find available port
        this.port = await this.findAvailablePort();
        this.url = `http://127.0.0.1:${this.port}`;
        // Start daemon
        await this.startDaemon();
        // Wait for healthy
        await this.waitForHealthy();
        return this.url;
    }
    // IR-3: Verify app-specific marker, not just HTTP 200
    async isHealthy() {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), HEALTH_TIMEOUT_MS);
            const response = await fetch(`${this.url}/health`, {
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!response.ok)
                return false;
            // IR-3: Verify it's actually Memory Garden, not another service
            const body = await response.json();
            return body.status === 'ok' && typeof body.version === 'string';
        }
        catch {
            return false;
        }
    }
    async findAvailablePort() {
        for (let i = 0; i < MAX_PORT_ATTEMPTS; i++) {
            const port = DEFAULT_PORT + i;
            if (await this.isPortAvailable(port)) {
                return port;
            }
        }
        throw new Error(`No available port found (tried ${DEFAULT_PORT}-${DEFAULT_PORT + MAX_PORT_ATTEMPTS - 1}).\n` +
            `Try: lsof -i :${DEFAULT_PORT} to see what's using the port.`);
    }
    isPortAvailable(port) {
        return new Promise((resolve) => {
            const server = net.createServer();
            server.once('error', () => resolve(false));
            server.once('listening', () => {
                server.close();
                resolve(true);
            });
            server.listen(port, '127.0.0.1');
        });
    }
    async startDaemon() {
        const binary = this.config.binaryPath || this.findBinary();
        const patternDir = (0, path_1.join)(this.dataDir, 'patterns');
        // Ensure pattern directory exists
        if (!(0, fs_1.existsSync)(patternDir)) {
            (0, fs_1.mkdirSync)(patternDir, { recursive: true });
        }
        this.process = (0, child_process_1.spawn)(binary, [
            '--serve',
            '--addr', `127.0.0.1:${this.port}`,
            '--pattern-dir', patternDir
        ], {
            detached: true,
            stdio: 'ignore'
        });
        // MR-3 + TC-4: Error handler for spawn failures with actionable guidance
        this.process.on('error', (err) => {
            console.error(`Could not start Memory Garden daemon.`);
            console.error(`\nTechnical details: ${err.message}`);
            console.error(`Binary path: ${binary}`);
            console.error(`\nCommon fixes:`);
            console.error(`  1. Ensure the binary has execute permissions: chmod +x ${binary}`);
            console.error(`  2. Check if another instance is running: lsof -i :${this.port}`);
            console.error(`  3. Try manual start for diagnostics: ${binary} --serve --addr 127.0.0.1:${this.port}`);
            console.error(`\nNeed help? https://github.com/live-neon/memory-garden/issues`);
        });
        // IR-4: Track PID for shutdown/recovery
        // CR-5: Null check for PID assignment
        if (this.process.pid != null) {
            this.pid = this.process.pid;
            (0, fs_1.writeFileSync)(this.pidFile, String(this.pid));
        }
        else {
            throw new Error('Daemon process spawned but PID not assigned. Check spawn permissions.');
        }
        this.process.unref();
    }
    // CR-11: Verify PATH candidates exist before returning
    findBinary() {
        // Check absolute paths first
        const absoluteCandidates = [
            (0, path_1.join)(__dirname, 'bin', 'memory-garden'),
            (0, path_1.join)(__dirname, '..', 'bin', 'memory-garden'),
            (0, path_1.join)(__dirname, '..', '..', 'bin', 'mg-daemon'),
        ];
        for (const path of absoluteCandidates) {
            if ((0, fs_1.existsSync)(path))
                return path;
        }
        // Check PATH using 'which' (Unix) or 'where' (Windows)
        const pathCandidates = ['memory-garden', 'mg-daemon'];
        for (const name of pathCandidates) {
            try {
                const cmd = process.platform === 'win32' ? `where ${name}` : `which ${name}`;
                const result = (0, child_process_1.execSync)(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
                if (result)
                    return result.split('\n')[0]; // Take first result
            }
            catch {
                // Not found in PATH, continue
            }
        }
        throw new Error('Memory Garden binary not found.\n' +
            'Tried: ' + [...absoluteCandidates, ...pathCandidates].join(', ') + '\n\n' +
            'Install with: go install github.com/live-neon/memory-garden/cmd/mg-daemon@latest\n' +
            'Or download from: https://github.com/live-neon/memory-garden/releases');
    }
    async waitForHealthy() {
        const start = Date.now();
        while (Date.now() - start < STARTUP_TIMEOUT_MS) {
            if (await this.isHealthy())
                return;
            await new Promise(r => setTimeout(r, 200));
        }
        throw new Error(`Daemon failed to start within ${STARTUP_TIMEOUT_MS}ms.\n` +
            `Check logs at: ${(0, path_1.join)(this.dataDir, 'logs', 'daemon.log')}\n` +
            `Try manual start: mg-daemon --serve --addr 127.0.0.1:${this.port}`);
    }
    // CR-5: Safe PID file unlinking with symlink protection
    safeUnlinkPidFile() {
        try {
            const stats = (0, fs_1.lstatSync)(this.pidFile);
            // Refuse to operate on symlinks
            if (stats.isSymbolicLink()) {
                console.error('PID file is a symlink, refusing to operate');
                return;
            }
            // Verify PID file is within data directory
            // TR-7: The '+ "/"' prevents path confusion (e.g., /foo/bar matching /foo/barbaz)
            // The 'realPath !== dataDir' allows PID file at dataDir root (edge case)
            const realPath = (0, fs_1.realpathSync)(this.pidFile);
            const dataDir = (0, fs_1.realpathSync)(this.dataDir);
            if (!realPath.startsWith(dataDir + '/') && realPath !== dataDir) {
                console.error('PID file outside data directory');
                return;
            }
            (0, fs_1.unlinkSync)(this.pidFile);
        }
        catch {
            // File doesn't exist or other error - OK
        }
    }
    // CR-1: Check if process is actually Memory Garden before killing
    isMemoryGardenProcess(pid) {
        try {
            // On macOS/Linux, check process command line
            const cmd = process.platform === 'darwin'
                ? `ps -p ${pid} -o command=`
                : `cat /proc/${pid}/cmdline 2>/dev/null || ps -p ${pid} -o command=`;
            const output = (0, child_process_1.execSync)(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
            return output.includes('memory-garden') || output.includes('mg-daemon');
        }
        catch {
            return false; // Process doesn't exist or can't read
        }
    }
    // IR-4: Clean up orphaned daemon from previous crash
    // CR-1: Verify process is Memory Garden before SIGTERM
    async cleanupOrphan() {
        if (!(0, fs_1.existsSync)(this.pidFile))
            return;
        try {
            const storedPid = parseInt((0, fs_1.readFileSync)(this.pidFile, 'utf-8').trim());
            if (!isNaN(storedPid)) {
                // Check if process is actually running AND is Memory Garden
                try {
                    process.kill(storedPid, 0); // Signal 0 = check if alive
                    // CR-1: Only kill if it's actually Memory Garden
                    if (this.isMemoryGardenProcess(storedPid)) {
                        process.kill(storedPid, 'SIGTERM');
                        // Wait a bit for graceful shutdown
                        await new Promise(r => setTimeout(r, 1000));
                    }
                }
                catch {
                    // Process not running, just clean up PID file
                }
            }
            // CR-5: Use safe unlink with symlink protection
            this.safeUnlinkPidFile();
        }
        catch {
            // OK if file operations fail
        }
    }
    // IR-4: Graceful shutdown with orphan recovery
    // CR-1: Verify process is Memory Garden before SIGTERM
    async shutdown() {
        // Kill tracked process (we know this.pid is ours)
        if (this.pid) {
            try {
                process.kill(this.pid, 'SIGTERM');
            }
            catch {
                // Process may already be gone
            }
            this.pid = null;
        }
        // Also check PID file for orphaned processes from crashes
        // CR-1: Verify process is Memory Garden before killing
        if ((0, fs_1.existsSync)(this.pidFile)) {
            try {
                const storedPid = parseInt((0, fs_1.readFileSync)(this.pidFile, 'utf-8').trim());
                if (!isNaN(storedPid) && this.isMemoryGardenProcess(storedPid)) {
                    process.kill(storedPid, 'SIGTERM');
                }
            }
            catch {
                // OK if already dead
            }
            // CR-5: Use safe unlink with symlink protection
            this.safeUnlinkPidFile();
        }
    }
    getUrl() {
        return this.url;
    }
    getPort() {
        return this.port;
    }
}
exports.DaemonManager = DaemonManager;
//# sourceMappingURL=daemon-manager.js.map