import net from 'net';
import path from 'path';
import os from 'os';

export class JEPGuardSDK {
  private socketPath: string;
  private skillId: string;

  constructor(skillId: string, socketPath?: string) {
    if (socketPath) throw new Error("Custom socket paths are not trusted");
    this.skillId = skillId;
    this.socketPath = socketPath || path.join(os.tmpdir(), 'jep-guard.sock');
  }

  private async call(method: string, payload: unknown): Promise<any> {
    return require('../../transport').guardCall(method,this.skillId,payload);
  }

  async judge(decision: { action: string; target?: string; context?: unknown }) {
    return this.call('JUDGE', {...decision,target:decision.target || ''});
  }

  async delegate(target: string, scope: string[], payload?: unknown) {
    return this.call('DELEGATE', { target, scope, payload });
  }

  async verify(targetEvent: string, verdict: 'approved' | 'rejected', evidence?: string[]) {
    return this.call('VERIFY', { target_event: targetEvent, verdict, evidence });
  }

  async terminate(targetEvent: string, reason: string) {
    return this.call('TERMINATE', { target_event: targetEvent, reason });
  }
}

export function init(skillId: string) {
  return new JEPGuardSDK(skillId);
}