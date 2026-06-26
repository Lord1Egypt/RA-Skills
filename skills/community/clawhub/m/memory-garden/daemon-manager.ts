// Daemon lifecycle management for Memory Garden MCP skill
// IR-3: Health check verifies app marker
// IR-4: Shutdown method with PID file for orphan prevention
// MR-3: Spawn error handler for better diagnostics
// TC-4: Error messages with actionable guidance
// CR-1: PID verification before SIGTERM (prevent killing wrong process)
// CR-4: Safe HOME resolution with fallback + Startup race serialization
// CR-5: Null check for PID assignment + Symlink protection for PID file
// CR-11: Verify PATH candidates exist before returning

import { spawn, ChildProcess, execSync } from 'child_process';
import { existsSync, readFileSync, writeFileSync, unlinkSync, mkdirSync, lstatSync, realpathSync } from 'fs';
import { join } from 'path';
import * as net from 'net';

// CR-4: Safe HOME resolution with fallback to USERPROFILE (Windows)
function getHomeDir(): string {
  const home = process.env.HOME || process.env.USERPROFILE;
  if (!home) {
    throw new Error(
      'HOME environment variable not set. ' +
      'Set MG_DATA_DIR environment variable to specify data directory explicitly.'
    );
  }
  return home;
}

const DEFAULT_PORT = 18790;
const MAX_PORT_ATTEMPTS = 10;
const HEALTH_TIMEOUT_MS = 5000;
const STARTUP_TIMEOUT_MS = 10000;

export interface DaemonConfig {
  binaryPath?: string;
  port?: number;
  dataDir?: string;
}

interface HealthResponse {
  status: string;
  version: string;
  pattern_count?: number;
}

export class DaemonManager {
  private process: ChildProcess | null = null;
  private port: number;
  private url: string;
  private pid: number | null = null;
  private pidFile: string;
  private dataDir: string;
  // CR-4: Promise guard to serialize concurrent startup calls
  private startPromise: Promise<string> | null = null;

  constructor(private config: DaemonConfig = {}) {
    this.port = config.port || DEFAULT_PORT;
    this.url = `http://127.0.0.1:${this.port}`;
    // CR-4: Use safe HOME resolution
    this.dataDir = config.dataDir || join(getHomeDir(), '.memory-garden');
    this.pidFile = join(this.dataDir, 'daemon.pid');

    // Ensure data directory exists
    if (!existsSync(this.dataDir)) {
      mkdirSync(this.dataDir, { recursive: true });
    }

    // IR-4: Register cleanup handlers
    process.on('SIGTERM', () => this.shutdown());
    process.on('SIGINT', () => this.shutdown());
  }

  // CR-4: Serialize concurrent startup calls with promise guard
  async ensureRunning(): Promise<string> {
    // If startup already in progress, return the shared promise
    if (this.startPromise) return this.startPromise;

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
  private async doStart(): Promise<string> {
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
  async isHealthy(): Promise<boolean> {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), HEALTH_TIMEOUT_MS);

      const response = await fetch(`${this.url}/health`, {
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (!response.ok) return false;

      // IR-3: Verify it's actually Memory Garden, not another service
      const body = await response.json() as HealthResponse;
      return body.status === 'ok' && typeof body.version === 'string';
    } catch {
      return false;
    }
  }

  private async findAvailablePort(): Promise<number> {
    for (let i = 0; i < MAX_PORT_ATTEMPTS; i++) {
      const port = DEFAULT_PORT + i;
      if (await this.isPortAvailable(port)) {
        return port;
      }
    }
    throw new Error(
      `No available port found (tried ${DEFAULT_PORT}-${DEFAULT_PORT + MAX_PORT_ATTEMPTS - 1}).\n` +
      `Try: lsof -i :${DEFAULT_PORT} to see what's using the port.`
    );
  }

  private isPortAvailable(port: number): Promise<boolean> {
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

  private async startDaemon(): Promise<void> {
    const binary = this.config.binaryPath || this.findBinary();
    const patternDir = join(this.dataDir, 'patterns');

    // Ensure pattern directory exists
    if (!existsSync(patternDir)) {
      mkdirSync(patternDir, { recursive: true });
    }

    this.process = spawn(binary, [
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
      writeFileSync(this.pidFile, String(this.pid));
    } else {
      throw new Error('Daemon process spawned but PID not assigned. Check spawn permissions.');
    }

    this.process.unref();
  }

  // CR-11: Verify PATH candidates exist before returning
  private findBinary(): string {
    // Check absolute paths first
    const absoluteCandidates = [
      join(__dirname, 'bin', 'memory-garden'),
      join(__dirname, '..', 'bin', 'memory-garden'),
      join(__dirname, '..', '..', 'bin', 'mg-daemon'),
    ];

    for (const path of absoluteCandidates) {
      if (existsSync(path)) return path;
    }

    // Check PATH using 'which' (Unix) or 'where' (Windows)
    const pathCandidates = ['memory-garden', 'mg-daemon'];
    for (const name of pathCandidates) {
      try {
        const cmd = process.platform === 'win32' ? `where ${name}` : `which ${name}`;
        const result = execSync(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }).trim();
        if (result) return result.split('\n')[0]; // Take first result
      } catch {
        // Not found in PATH, continue
      }
    }

    throw new Error(
      'Memory Garden binary not found.\n' +
      'Tried: ' + [...absoluteCandidates, ...pathCandidates].join(', ') + '\n\n' +
      'Install with: go install github.com/live-neon/memory-garden/cmd/mg-daemon@latest\n' +
      'Or download from: https://github.com/live-neon/memory-garden/releases'
    );
  }

  private async waitForHealthy(): Promise<void> {
    const start = Date.now();
    while (Date.now() - start < STARTUP_TIMEOUT_MS) {
      if (await this.isHealthy()) return;
      await new Promise(r => setTimeout(r, 200));
    }
    throw new Error(
      `Daemon failed to start within ${STARTUP_TIMEOUT_MS}ms.\n` +
      `Check logs at: ${join(this.dataDir, 'logs', 'daemon.log')}\n` +
      `Try manual start: mg-daemon --serve --addr 127.0.0.1:${this.port}`
    );
  }

  // CR-5: Safe PID file unlinking with symlink protection
  private safeUnlinkPidFile(): void {
    try {
      const stats = lstatSync(this.pidFile);
      // Refuse to operate on symlinks
      if (stats.isSymbolicLink()) {
        console.error('PID file is a symlink, refusing to operate');
        return;
      }
      // Verify PID file is within data directory
      // TR-7: The '+ "/"' prevents path confusion (e.g., /foo/bar matching /foo/barbaz)
      // The 'realPath !== dataDir' allows PID file at dataDir root (edge case)
      const realPath = realpathSync(this.pidFile);
      const dataDir = realpathSync(this.dataDir);
      if (!realPath.startsWith(dataDir + '/') && realPath !== dataDir) {
        console.error('PID file outside data directory');
        return;
      }
      unlinkSync(this.pidFile);
    } catch {
      // File doesn't exist or other error - OK
    }
  }

  // CR-1: Check if process is actually Memory Garden before killing
  private isMemoryGardenProcess(pid: number): boolean {
    try {
      // On macOS/Linux, check process command line
      const cmd = process.platform === 'darwin'
        ? `ps -p ${pid} -o command=`
        : `cat /proc/${pid}/cmdline 2>/dev/null || ps -p ${pid} -o command=`;
      const output = execSync(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
      return output.includes('memory-garden') || output.includes('mg-daemon');
    } catch {
      return false; // Process doesn't exist or can't read
    }
  }

  // IR-4: Clean up orphaned daemon from previous crash
  // CR-1: Verify process is Memory Garden before SIGTERM
  private async cleanupOrphan(): Promise<void> {
    if (!existsSync(this.pidFile)) return;

    try {
      const storedPid = parseInt(readFileSync(this.pidFile, 'utf-8').trim());
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
        } catch {
          // Process not running, just clean up PID file
        }
      }
      // CR-5: Use safe unlink with symlink protection
      this.safeUnlinkPidFile();
    } catch {
      // OK if file operations fail
    }
  }

  // IR-4: Graceful shutdown with orphan recovery
  // CR-1: Verify process is Memory Garden before SIGTERM
  async shutdown(): Promise<void> {
    // Kill tracked process (we know this.pid is ours)
    if (this.pid) {
      try {
        process.kill(this.pid, 'SIGTERM');
      } catch {
        // Process may already be gone
      }
      this.pid = null;
    }

    // Also check PID file for orphaned processes from crashes
    // CR-1: Verify process is Memory Garden before killing
    if (existsSync(this.pidFile)) {
      try {
        const storedPid = parseInt(readFileSync(this.pidFile, 'utf-8').trim());
        if (!isNaN(storedPid) && this.isMemoryGardenProcess(storedPid)) {
          process.kill(storedPid, 'SIGTERM');
        }
      } catch {
        // OK if already dead
      }
      // CR-5: Use safe unlink with symlink protection
      this.safeUnlinkPidFile();
    }
  }

  getUrl(): string {
    return this.url;
  }

  getPort(): number {
    return this.port;
  }
}
