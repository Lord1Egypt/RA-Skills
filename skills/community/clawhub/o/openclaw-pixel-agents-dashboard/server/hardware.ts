/**
 * Hardware Monitor — Reads system stats for the server rack display.
 * CPU, GPU, RAM, disk usage via /proc and nvidia-smi.
 */

import { execSync } from 'child_process';
import * as fs from 'fs';

export interface HardwareStats {
  cpu: {
    cores: number;
    load1: number;
    load5: number;
    load15: number;
    usagePercent: number; // load1 / cores * 100, capped at 100
  };
  gpu: {
    tempC: number;
    utilizationPercent: number;
    memUsedMB: number;
    memTotalMB: number;
    available: boolean;
  };
  ram: {
    usedMB: number;
    totalMB: number;
    usagePercent: number;
  };
  disk: {
    usedGB: number;
    totalGB: number;
    usagePercent: number;
  };
  network: {
    rxBytesPerSec: number;
    txBytesPerSec: number;
  };
  timestamp: number;
}

// Track network bytes for delta calculation
let lastNetRx = 0;
let lastNetTx = 0;
let lastNetTime = 0;

function readCpu(): HardwareStats['cpu'] {
  try {
    const cores = fs.readFileSync('/proc/cpuinfo', 'utf-8')
      .split('\n')
      .filter(l => l.startsWith('processor')).length;
    const loadavg = fs.readFileSync('/proc/loadavg', 'utf-8').trim().split(/\s+/);
    const load1 = parseFloat(loadavg[0]) || 0;
    const load5 = parseFloat(loadavg[1]) || 0;
    const load15 = parseFloat(loadavg[2]) || 0;
    return {
      cores,
      load1,
      load5,
      load15,
      usagePercent: Math.min(100, Math.round((load1 / cores) * 100)),
    };
  } catch {
    return { cores: 1, load1: 0, load5: 0, load15: 0, usagePercent: 0 };
  }
}

function readGpu(): HardwareStats['gpu'] {
  try {
    const out = execSync(
      'nvidia-smi --query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits',
      { timeout: 3000, encoding: 'utf-8' },
    ).trim();
    const [temp, util, memUsed, memTotal] = out.split(',').map(s => parseFloat(s.trim()));
    return {
      tempC: temp || 0,
      utilizationPercent: util || 0,
      memUsedMB: memUsed || 0,
      memTotalMB: memTotal || 0,
      available: true,
    };
  } catch {
    return { tempC: 0, utilizationPercent: 0, memUsedMB: 0, memTotalMB: 0, available: false };
  }
}

function readRam(): HardwareStats['ram'] {
  try {
    const meminfo = fs.readFileSync('/proc/meminfo', 'utf-8');
    const total = parseInt(meminfo.match(/MemTotal:\s+(\d+)/)?.[1] || '0') / 1024;
    const available = parseInt(meminfo.match(/MemAvailable:\s+(\d+)/)?.[1] || '0') / 1024;
    const used = total - available;
    return {
      usedMB: Math.round(used),
      totalMB: Math.round(total),
      usagePercent: Math.round((used / total) * 100),
    };
  } catch {
    return { usedMB: 0, totalMB: 0, usagePercent: 0 };
  }
}

function readDisk(): HardwareStats['disk'] {
  try {
    const out = execSync('df -BG / | tail -1', { timeout: 3000, encoding: 'utf-8' }).trim();
    const parts = out.split(/\s+/);
    const totalGB = parseInt(parts[1]) || 0;
    const usedGB = parseInt(parts[2]) || 0;
    const pct = parseInt(parts[4]) || 0;
    return { usedGB, totalGB, usagePercent: pct };
  } catch {
    return { usedGB: 0, totalGB: 0, usagePercent: 0 };
  }
}

function readNetwork(): HardwareStats['network'] {
  try {
    const lines = fs.readFileSync('/proc/net/dev', 'utf-8').split('\n');
    let totalRx = 0;
    let totalTx = 0;
    for (const line of lines) {
      // Skip loopback and header lines
      if (line.includes('lo:') || !line.includes(':')) continue;
      const parts = line.split(':')[1]?.trim().split(/\s+/);
      if (parts && parts.length >= 10) {
        totalRx += parseInt(parts[0]) || 0;
        totalTx += parseInt(parts[8]) || 0;
      }
    }
    const now = Date.now();
    const elapsed = lastNetTime > 0 ? (now - lastNetTime) / 1000 : 1;
    const rxPerSec = lastNetTime > 0 ? Math.max(0, (totalRx - lastNetRx) / elapsed) : 0;
    const txPerSec = lastNetTime > 0 ? Math.max(0, (totalTx - lastNetTx) / elapsed) : 0;
    lastNetRx = totalRx;
    lastNetTx = totalTx;
    lastNetTime = now;
    return { rxBytesPerSec: Math.round(rxPerSec), txBytesPerSec: Math.round(txPerSec) };
  } catch {
    return { rxBytesPerSec: 0, txBytesPerSec: 0 };
  }
}

export function getHardwareStats(): HardwareStats {
  return {
    cpu: readCpu(),
    gpu: readGpu(),
    ram: readRam(),
    disk: readDisk(),
    network: readNetwork(),
    timestamp: Date.now(),
  };
}

// ── Remote hardware stats (Solara) ──────────────────────────

import { REMOTE_AGENTS } from './config.js';

const SSH_TIMEOUT = 5000;

// Remote agent caches: agentId → { stats, fetchedAt }
const remoteCache = new Map<string, { stats: HardwareStats | null; fetchedAt: number }>();
const REMOTE_CACHE_TTL = 8000;

function sshExecForAgent(agentId: string, cmd: string): string {
  const remote = REMOTE_AGENTS.find(r => r.id === agentId);
  if (!remote) throw new Error(`No remote config for agent: ${agentId}`);

  const authFlag = remote.keyPath
    ? `-i '${remote.keyPath}'`
    : remote.password
      ? `-o 'Password=${remote.password}'`  // Won't work directly; use sshpass below
      : '';

  // Use sshpass for password auth, key-based otherwise
  const sshCmd = remote.password
    ? `sshpass -p '${remote.password}' ssh -o ConnectTimeout=4 -o StrictHostKeyChecking=no -o LogLevel=ERROR ${remote.user}@${remote.host} '${cmd}'`
    : `ssh ${authFlag} -o ConnectTimeout=4 -o StrictHostKeyChecking=no -o LogLevel=ERROR ${remote.user}@${remote.host} '${cmd}'`;

  return execSync(sshCmd, { timeout: SSH_TIMEOUT, encoding: 'utf-8' }).trim();
}

/** Legacy alias for backward compat — gets first remote agent's stats */
function sshExec(cmd: string): string {
  const first = REMOTE_AGENTS[0];
  if (!first) throw new Error('No remote agents configured');
  return sshExecForAgent(first.id, cmd);
}

let solaraCache: { stats: HardwareStats | null; fetchedAt: number } = { stats: null, fetchedAt: 0 };

/** Check if any remote agents are configured */
export function hasRemoteAgents(): boolean {
  return REMOTE_AGENTS.length > 0;
}

/** Get the first remote agent ID (for backward-compat endpoints) */
export function getFirstRemoteAgentId(): string | null {
  return REMOTE_AGENTS[0]?.id ?? null;
}

export function getSolaraHardwareStats(): HardwareStats | null {
  const now = Date.now();
  if (solaraCache.stats && now - solaraCache.fetchedAt < SOLARA_CACHE_TTL) {
    return solaraCache.stats;
  }

  try {
    // Batch all reads into a single SSH command for speed
    const script = [
      'cat /proc/cpuinfo | grep processor | wc -l',
      'cat /proc/loadavg',
      'nvidia-smi --query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits 2>/dev/null || echo "nogpu"',
      'cat /proc/meminfo | grep -E "MemTotal|MemAvailable"',
      'df -BG / | tail -1',
    ].join(' && echo "---SPLIT---" && ');

    const raw = sshExec(script);
    const parts = raw.split('---SPLIT---').map(s => s.trim());

    // CPU
    const cores = parseInt(parts[0]) || 1;
    const loadParts = (parts[1] || '').split(/\s+/);
    const load1 = parseFloat(loadParts[0]) || 0;

    // GPU
    let gpu: HardwareStats['gpu'] = { tempC: 0, utilizationPercent: 0, memUsedMB: 0, memTotalMB: 0, available: false };
    if (parts[2] && parts[2] !== 'nogpu') {
      const [temp, util, memUsed, memTotal] = parts[2].split(',').map(s => parseFloat(s.trim()));
      gpu = { tempC: temp || 0, utilizationPercent: util || 0, memUsedMB: memUsed || 0, memTotalMB: memTotal || 0, available: true };
    }

    // RAM
    const memLines = parts[3] || '';
    const totalKB = parseInt(memLines.match(/MemTotal:\s+(\d+)/)?.[1] || '0');
    const availKB = parseInt(memLines.match(/MemAvailable:\s+(\d+)/)?.[1] || '0');
    const totalMB = Math.round(totalKB / 1024);
    const usedMB = Math.round((totalKB - availKB) / 1024);

    // Disk
    const dfParts = (parts[4] || '').split(/\s+/);
    const diskTotalGB = parseInt(dfParts[1]) || 0;
    const diskUsedGB = parseInt(dfParts[2]) || 0;
    const diskPct = parseInt(dfParts[4]) || 0;

    const stats: HardwareStats = {
      cpu: { cores, load1, load5: 0, load15: 0, usagePercent: Math.min(100, Math.round((load1 / cores) * 100)) },
      gpu,
      ram: { usedMB, totalMB, usagePercent: Math.round((usedMB / totalMB) * 100) },
      disk: { usedGB: diskUsedGB, totalGB: diskTotalGB, usagePercent: diskPct },
      network: { rxBytesPerSec: 0, txBytesPerSec: 0 }, // Skip network for remote
      timestamp: Date.now(),
    };

    solaraCache = { stats, fetchedAt: now };
    return stats;
  } catch {
    // SSH failed — machine offline
    solaraCache = { stats: null, fetchedAt: now };
    return null;
  }
}
