"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CausalGateService = void 0;
class CausalGateService {
    core;
    registry;
    policy;
    extensions;
    constructor(core, registry, policy, extensions) {
        this.core = core;
        this.registry = registry;
        this.policy = policy;
        this.extensions = extensions;
    }
    async process(req) {
        // 1. Generate Judge event (pending)
        const judgeEvent = this.core.createJudge({
            requester: req.requester,
            action: req.action,
            target: req.target,
            context: req.context,
            request_type: req.type
        });
        // 2. Check skill identity
        const skill = this.registry.get(req.requester);
        if (!skill) {
            this.core.createTerminate({ reason: 'unregistered_skill', target: req.requester }, undefined, [judgeEvent.nonce]);
            this.core.updateStatus(judgeEvent.nonce, 'denied');
            return { action: 'block', reason: 'unregistered_skill', event: judgeEvent };
        }
        // 3. Policy evaluation
        const policyResult = await this.policy.evaluate(req, skill);
        if (policyResult.decision === 'review')
            return { action: 'review', reason: 'policy_review', event: judgeEvent, requiredVerifiers: policyResult.required_verifiers };
        if (policyResult.decision !== 'allow') {
            this.core.createTerminate({ reason: policyResult.rule_matched || 'policy_deny' }, undefined, [judgeEvent.nonce]);
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
                    this.core.createTerminate({ reason: 'circular_delegation', target: targetSkill }, undefined, [judgeEvent.nonce]);
                    return { action: 'block', reason: 'circular_delegation_detected', event: judgeEvent };
                }
            }
        }
        // 5. Extension evaluation
        const extResults = await this.extensions.evaluateAll(req);
        for (const res of extResults) {
            if (res.action === 'block') {
                this.core.createTerminate({ reason: `${res.extension}: ${res.rule_matched}` }, undefined, [judgeEvent.nonce]);
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
        const token = this.issueCapabilityToken(judgeEvent, skill, req);
        return { action: 'allow', reason: 'granted', event: judgeEvent, capabilityToken: token };
    }
    issueCapabilityToken(event, skill, req) {
        const payload = {
            type: 'jep-cap',
            event_id: event.nonce,
            agent: skill.skill_id,
            request_digest: require("../../transport").requestDigest(skill.skill_id, { action: req.action, target: req.target, context: req.context }),
            capabilities: skill.capabilities,
            issued_at: event.when,
            expires_at: event.when + 60
        };
        const sig = this.core.signPayload(payload);
        return Buffer.from(JSON.stringify({ ...payload, sig })).toString('base64');
    }
}
exports.CausalGateService = CausalGateService;
//# sourceMappingURL=gate.js.map