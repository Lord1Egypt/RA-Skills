import { ExecutionRequest, GateResult, JPEvent, SkillIdentity } from '../core/types';
import { JEPCore } from '../core/jep-core';
import { SkillRegistryService } from './registry';
import { PolicyEngineService } from './policy';
import { ExtensionLoaderService } from '../extensions/loader';

export class CausalGateService {
  constructor(
    private core: JEPCore,
    private registry: SkillRegistryService,
    private policy: PolicyEngineService,
    private extensions: ExtensionLoaderService
  ) {}

  async process(req: ExecutionRequest): Promise<GateResult> {
    // 1. Generate Judge event (pending)
    const judgeEvent = this.core.createJudge({
      action: req.action,
      target: req.target,
      context: req.context,
      request_type: req.type
    }, req.requester);

    // 2. Check skill identity
    const skill = this.registry.get(req.requester);
    if (!skill) {
      this.core.createTerminate(
        { reason: 'unregistered_skill', target: req.requester },
        req.requester,
        [judgeEvent.nonce]
      );
      this.core.updateStatus(judgeEvent.nonce, 'denied');
      return { action: 'block', reason: 'unregistered_skill', event: judgeEvent };
    }

    // 3. Policy evaluation
    const policyResult = await this.policy.evaluate(req, skill);
    if (policyResult.decision === 'deny') {
      this.core.createTerminate(
        { reason: policyResult.rule_matched || 'policy_deny' },
        req.requester,
        [judgeEvent.nonce]
      );
      this.core.updateStatus(judgeEvent.nonce, 'denied');
      return { action: 'block', reason: policyResult.rule_matched || 'policy_deny', event: judgeEvent };
    }

    // 4. Cross-skill delegation checks
    if (req.type === 'skill_delegate') {
      const targetSkill = req.target;
      const rep = this.extensions.getReputation?.(targetSkill);
      if (rep && rep.completionRate < 0.6) {
        return {
          action: 'review',
          reason: `low_reputation: ${targetSkill} rate=${rep.completionRate}`,
          event: judgeEvent,
          requiredVerifiers: ['user', 'admin']
        };
      }

      const activeDelegations = this.core.getActiveDelegations(req.requester);
      for (const d of activeDelegations) {
        if (this.core.dag.hasCycle(d.who, targetSkill)) {
          this.core.createTerminate(
            { reason: 'circular_delegation', target: targetSkill },
            req.requester,
            [judgeEvent.nonce]
          );
          return { action: 'block', reason: 'circular_delegation_detected', event: judgeEvent };
        }
      }
    }

    // 5. Extension evaluation
    const extResults = await this.extensions.evaluateAll(req);
    for (const res of extResults) {
      if (res.action === 'block') {
        this.core.createTerminate(
          { reason: `${res.extension}: ${res.rule_matched}` },
          req.requester,
          [judgeEvent.nonce]
        );
        this.core.updateStatus(judgeEvent.nonce, 'denied');
        return { action: 'block', reason: `${res.extension}: ${res.rule_matched}`, event: judgeEvent };
      }
      if (res.action === 'review') {
        return {
          action: 'review',
          reason: `${res.extension}: review required`,
          event: judgeEvent,
          requiredVerifiers: ['user']
        };
      }
    }

    // 6. Grant
    this.core.updateStatus(judgeEvent.nonce, 'granted');
    const token = this.issueCapabilityToken(judgeEvent, skill);
    return { action: 'allow', reason: 'granted', event: judgeEvent, capabilityToken: token };
  }

  private issueCapabilityToken(event: JPEvent, skill: SkillIdentity): string {
    const payload = {
      type: 'jep-cap',
      event_id: event.nonce,
      agent: event.who,
      capabilities: skill.capabilities,
      issued_at: event.when,
      expires_at: event.when + 300
    };
    const canonical = JSON.stringify(payload);
    // @ts-ignore - accessing private crypto for signing
    const sig = this.core['crypto'].sign(canonical);
    return Buffer.from(JSON.stringify({ ...payload, sig })).toString('base64');
  }
}