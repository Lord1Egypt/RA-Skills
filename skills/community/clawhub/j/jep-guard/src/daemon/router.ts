import { RouteRequest, RouteResult, JPEvent } from '../core/types';
import { JEPCore } from '../core/jep-core';
import { CausalGateService } from './gate';
import net from 'net';
import path from 'path';
import os from 'os';

export class CausalRouterService {
  constructor(private core: JEPCore, private gate: CausalGateService) {}

  async route(req: RouteRequest): Promise<RouteResult> {
    const gateResult = await this.gate.process({
      requester: req.from,
      action: 'delegate',
      target: req.to,
      type: 'skill_delegate',
      context: { scope: req.scope, payload: req.payload }
    });

    if (gateResult.action !== 'allow') {
      return { success: false, error: gateResult.reason };
    }

    const delegateEvent = this.core.createDelegate(
      {
        target_agent: req.to,
        scope: req.scope,
        capability_token: gateResult.capabilityToken
      },
      req.from,
      [gateResult.event!.nonce]
    );

    try {
      const result = await this.invokeSkill(req.to, {
        type: 'delegated_execution',
        token: gateResult.capabilityToken,
        payload: req.payload,
        from: req.from
      }, req.timeout || 30000);

      if (result.success) {
        const verifyEvent = this.core.createVerify(
          {
            target_event: delegateEvent.nonce,
            verdict: 'approved',
            evidence: [result.output_hash]
          },
          req.to,
          [delegateEvent.nonce]
        );
        return { success: true, event: verifyEvent, output: result.output };
      } else {
        const termEvent = this.core.createTerminate(
          {
            target_event: delegateEvent.nonce,
            reason: result.error || 'execution_failed',
            triggered_by: 'user'
          },
          req.to,
          [delegateEvent.nonce]
        );
        return { success: false, event: termEvent, error: result.error };
      }
    } catch (err) {
      const termEvent = this.core.createTerminate(
        {
          target_event: delegateEvent.nonce,
          reason: err instanceof Error ? err.message : 'invocation_timeout',
          triggered_by: 'user'
        },
        req.to,
        [delegateEvent.nonce]
      );
      return { success: false, event: termEvent, error: 'invocation_failed' };
    }
  }

  private async invokeSkill(skillId: string, message: unknown, timeout: number): Promise<any> {
    return new Promise((resolve, reject) => {
      const socketPath = path.join(os.tmpdir(), `openclaw-${skillId}.sock`);
      const client = net.createConnection(socketPath);
      client.write(JSON.stringify(message) + '\n');

      let data = '';
      client.on('data', chunk => data += chunk);
      client.on('end', () => {
        try { resolve(JSON.parse(data)); } catch { reject(new Error('Invalid JSON')); }
      });
      client.on('error', reject);
      setTimeout(() => { client.destroy(); reject(new Error('Timeout')); }, timeout);
    });
  }
}