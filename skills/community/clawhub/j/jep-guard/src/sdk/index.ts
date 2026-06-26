import net from 'net';
import path from 'path';
import os from 'os';

export class JEPGuardSDK {
  private socketPath: string;
  private skillId: string;

  constructor(skillId: string, socketPath?: string) {
    this.skillId = skillId;
    this.socketPath = socketPath || path.join(os.tmpdir(), 'jep-guard.sock');
  }

  private async call(method: string, payload: unknown): Promise<any> {
    return new Promise((resolve, reject) => {
      const client = net.createConnection(this.socketPath);
      const req = JSON.stringify({ method, skill: this.skillId, payload });

      let data = '';
      let settled = false;

      client.write(req);
      client.on('data', chunk => data += chunk);
      client.on('end', () => {
        if (settled) return;
        settled = true;
        try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
      });
      client.on('error', (err) => {
        if (settled) return;
        settled = true;
        reject(err);
      });
      setTimeout(() => {
        if (settled) return;
        settled = true;
        client.destroy();
        reject(new Error('JEP Guard timeout'));
      }, 5000);
    });
  }

  async judge(decision: { action: string; target?: string; context?: unknown }) {
    return this.call('JUDGE', decision);
  }

  async delegate(target: string, scope: string[], payload?: unknown) {
    return this.call('DELEGATE', { target, scope, payload });
  }

  async verify(targetEvent: string, verdict: 'approved' | 'rejected', evidence?: string[]) {
    return this.call('VERIFY', { targetEvent, verdict, evidence });
  }

  async terminate(targetEvent: string, reason: string) {
    return this.call('TERMINATE', { targetEvent, reason });
  }
}

export function init(skillId: string) {
  return new JEPGuardSDK(skillId);
}