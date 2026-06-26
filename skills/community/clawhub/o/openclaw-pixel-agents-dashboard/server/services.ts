/**
 * Service Controller — Manages systemd services for the breaker panel.
 * Supports local (--user) and remote (SSH) services.
 * Service list built from config — no hardcoded hosts or credentials.
 */

import { execSync } from 'child_process';

import { REMOTE_AGENTS } from './config.js';

export interface ServiceDef {
  id: string;
  label: string;
  unit: string;
  remote?: {
    host: string;
    user: string;
    password?: string;
    keyPath?: string;
  };
}

export interface ServiceStatus {
  id: string;
  label: string;
  state: 'running' | 'stopped' | 'starting' | 'stopping' | 'unknown';
}

/**
 * Build service list from config.
 * Always includes local gateway. Adds remote gateways for each remoteAgent.
 */
function buildServiceList(): ServiceDef[] {
  const services: ServiceDef[] = [
    {
      id: 'local-gateway',
      label: 'Local Gateway',
      unit: 'openclaw-gateway',
    },
  ];

  // Add remote gateways from config
  for (const remote of REMOTE_AGENTS) {
    services.push({
      id: `${remote.id}-gateway`,
      label: `${remote.id.charAt(0).toUpperCase() + remote.id.slice(1)} Gateway`,
      unit: 'openclaw-gateway',
      remote: {
        host: remote.host,
        user: remote.user,
        password: remote.password,
        keyPath: remote.keyPath,
      },
    });
  }

  return services;
}

export const SERVICES: ServiceDef[] = buildServiceList();

function runSystemctl(service: ServiceDef, action: 'is-active' | 'start' | 'stop' | 'restart'): string {
  let cmd: string;

  if (service.remote) {
    const r = service.remote;
    const sshBase = `-o StrictHostKeyChecking=no -o ConnectTimeout=5 -o LogLevel=ERROR`;
    const systemctlCmd = `systemctl --user ${action} ${service.unit}`;

    if (r.password) {
      cmd = `sshpass -p '${r.password}' ssh ${sshBase} ${r.user}@${r.host} '${systemctlCmd}'`;
    } else if (r.keyPath) {
      cmd = `ssh -i '${r.keyPath}' ${sshBase} ${r.user}@${r.host} '${systemctlCmd}'`;
    } else {
      cmd = `ssh ${sshBase} ${r.user}@${r.host} '${systemctlCmd}'`;
    }
  } else {
    cmd = `systemctl --user ${action} ${service.unit}`;
  }

  try {
    return execSync(cmd, { timeout: 10_000, encoding: 'utf-8' }).trim();
  } catch (err: unknown) {
    const error = err as { stdout?: string; stderr?: string; status?: number };
    if (action === 'is-active' && error.stdout) {
      return error.stdout.trim();
    }
    throw new Error(`Service command failed: ${action} ${service.unit}${service.remote ? ` (remote ${service.remote.host})` : ''}`);
  }
}

export function getServiceStatuses(): ServiceStatus[] {
  return SERVICES.map(svc => {
    try {
      const result = runSystemctl(svc, 'is-active');
      let state: ServiceStatus['state'] = 'unknown';
      if (result === 'active') state = 'running';
      else if (result === 'inactive' || result === 'dead') state = 'stopped';
      else if (result === 'activating') state = 'starting';
      else if (result === 'deactivating') state = 'stopping';
      return { id: svc.id, label: svc.label, state };
    } catch {
      return { id: svc.id, label: svc.label, state: 'unknown' as const };
    }
  });
}

export function restartService(serviceId: string): { success: boolean; error?: string } {
  const svc = SERVICES.find(s => s.id === serviceId);
  if (!svc) return { success: false, error: `Unknown service: ${serviceId}` };

  try {
    runSystemctl(svc, 'restart');
    return { success: true };
  } catch (err) {
    return { success: false, error: (err as Error).message };
  }
}

export function controlService(serviceId: string, action: 'start' | 'stop'): { success: boolean; error?: string } {
  const svc = SERVICES.find(s => s.id === serviceId);
  if (!svc) return { success: false, error: `Unknown service: ${serviceId}` };

  try {
    runSystemctl(svc, action);
    return { success: true };
  } catch (err) {
    return { success: false, error: (err as Error).message };
  }
}
