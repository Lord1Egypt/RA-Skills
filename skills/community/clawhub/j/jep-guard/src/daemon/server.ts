import net from 'net';
import path from 'path';
import os from 'os';
import fs from 'fs';
import { JEPCore } from '../core/jep-core';
import { SkillRegistryService } from './registry';
import { PolicyEngineService } from './policy';
import { CausalGateService } from './gate';
import { CausalRouterService } from './router';
import { ReputationEngineService } from './reputation';
import { AuditStreamService } from './audit';
import { ExtensionLoaderService } from '../extensions/loader';

export class GuardDaemon {
  public socketPath: string;
  private server?: net.Server;
  private core: JEPCore;
  private registry: SkillRegistryService;
  private policy: PolicyEngineService;
  private reputation: ReputationEngineService;
  private audit: AuditStreamService;
  private extensions: ExtensionLoaderService;
  private gate: CausalGateService;
  private router: CausalRouterService;

  constructor(private mode: string) {
    this.socketPath = path.join(os.tmpdir(), 'jep-guard.sock');
    this.core = new JEPCore('jep-guard-daemon');
    this.registry = new SkillRegistryService();
    this.policy = new PolicyEngineService();
    this.reputation = new ReputationEngineService();
    this.audit = new AuditStreamService();
    this.extensions = new ExtensionLoaderService({
      core: this.core as any,
      registry: this.registry,
      policy: this.policy,
      reputation: this.reputation,
      audit: this.audit
    });
    this.gate = new CausalGateService(this.core, this.registry, this.policy, this.extensions);
    this.router = new CausalRouterService(this.core, this.gate);
  }

  async start(): Promise<void> {
    await this.extensions.loadBuiltins();

    this.server = net.createServer((socket) => {
      socket.on('data', async (data) => {
        try {
          const req = JSON.parse(data.toString());
          const result = await this.handleRequest(req);
          socket.write(JSON.stringify(result));
          socket.end();
        } catch (err) {
          socket.write(JSON.stringify({ error: err instanceof Error ? err.message : 'unknown' }));
          socket.end();
        }
      });
    });

    // Remove old socket
    if (fs.existsSync(this.socketPath)) {
      fs.unlinkSync(this.socketPath);
    }

    this.server.listen(this.socketPath);
    fs.chmodSync(this.socketPath, 0o600);

    console.log(`[JEP Guard] Daemon listening on ${this.socketPath}`);
  }

  stop(): void {
    this.server?.close();
    if (fs.existsSync(this.socketPath)) {
      fs.unlinkSync(this.socketPath);
    }
  }

  private async handleRequest(req: any): Promise<any> {
    switch (req.method) {
      case 'REGISTER_SKILL':
        const skill = this.registry.register(req.payload);
        return { success: true, skill_id: skill.skill_id, status: 'registered' };

      case 'JUDGE':
        return this.gate.process({
          requester: req.skill,
          action: req.payload.action,
          target: req.payload.target || '',
          type: 'system_call',
          context: req.payload.context
        });

      case 'DELEGATE':
        return this.router.route({
          from: req.skill,
          to: req.payload.target,
          scope: req.payload.scope,
          payload: req.payload.payload
        });

      case 'VERIFY':
        const vEvent = this.core.createVerify(req.payload, req.skill);
        await this.audit.emit(vEvent);
        this.reputation.recordEvent(req.skill, vEvent);
        return { success: true, event: vEvent };

      case 'TERMINATE':
        const tEvent = this.core.createTerminate(req.payload, req.skill);
        await this.audit.emit(tEvent);
        this.reputation.recordEvent(req.skill, tEvent);
        return { success: true, event: tEvent };

      default:
        return { error: 'Unknown method' };
    }
  }
}