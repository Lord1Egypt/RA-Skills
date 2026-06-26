// @ts-nocheck
class PolicyEngine {
    constructor(config = { mode: 'enforce' }) {
        this.mode = config.mode;
        this.policy = config.policy || {};
    }

    evaluate(toolName, args, runtimeContext = {}) {
        if (this.mode === 'monitor') {
            return {
                action: 'allow',
                reason: 'monitor mode',
                policyId: 'policy.monitor-mode',
                amplificationReasons: [],
                remediationSuggestion: 'Switch to enforce or strict mode to turn policy decisions into hard blocks.',
                contractViolations: [],
            };
        }

        const argsStr = JSON.stringify(args || {});
        const normalized = argsStr.toLowerCase();
        const allowedTools = Array.isArray(this.policy.allowed_tools) ? new Set(this.policy.allowed_tools) : null;
        const blockedTools = new Set(Array.isArray(this.policy.blocked_tools) ? this.policy.blocked_tools : []);
        const amplificationReasons = [];
        const contractViolations = this.evaluateContracts(toolName, normalized, runtimeContext);

        if (blockedTools.has(toolName)) {
            return this.block(
                this.policy.id || 'policy.blocked-tool',
                `tool "${toolName}" is explicitly blocked by policy`,
                amplificationReasons,
                `Remove "${toolName}" from blocked_tools or route the task through an allowlisted alternative.`,
                contractViolations,
            );
        }

        if (allowedTools && allowedTools.size > 0 && !allowedTools.has(toolName)) {
            return this.block(
                this.policy.id || 'policy.allowlist-only',
                `tool "${toolName}" is outside the allowlist`,
                amplificationReasons,
                `Add "${toolName}" to allowed_tools only if the session genuinely requires it.`,
                contractViolations,
            );
        }

        const networkIntent = /(curl|wget|fetch\s*\(|https?:\/\/|websocket|webhook|socket)/i.test(normalized);
        if (networkIntent && this.policy.max_network_scope === 'none') {
            return this.block(
                this.policy.id || 'policy.network-none',
                'network egress is disabled for this session',
                ['network request detected under max_network_scope=none'],
                'Remove the network call or raise max_network_scope after human review.',
                contractViolations,
            );
        }

        if (networkIntent && this.policy.max_network_scope === 'internal-only' && /(https?:\/\/)(?!127\.0\.0\.1|localhost)/i.test(normalized)) {
            return this.block(
                this.policy.id || 'policy.network-internal-only',
                'external network egress exceeds the internal-only policy',
                ['external URL detected while internal-only policy is active'],
                'Restrict the target to localhost/internal endpoints or widen the policy after review.',
                contractViolations,
            );
        }

        if (this.policy.secret_bearing_context && networkIntent && /(token|secret|password|api[_-]?key|authorization|cookie|session)/i.test(normalized)) {
            amplificationReasons.push('secret-bearing context combined with outbound network intent');
        }

        if (this.policy.memory_write_permission === false && /(memory|episodes|notes|guava_memory_write|memory_store)/i.test(normalized) && /(write|append|edit|>|apply_patch)/i.test(normalized)) {
            return this.block(
                this.policy.id || 'policy.memory-write-disabled',
                'memory writes are disabled for this session',
                amplificationReasons,
                'Use read-only memory/search flow or explicitly enable memory_write_permission.',
                contractViolations,
            );
        }

        if ((toolName === 'run_shell_command' || toolName === 'shell' || toolName === 'exec') && (normalized.includes('rm -rf') || normalized.includes('mkfs'))) {
            return this.block(
                this.policy.id || 'policy.destructive-fs',
                'destructive fs operation',
                amplificationReasons,
                'Replace the destructive operation with a bounded file change or explicit human-approved rollback path.',
                contractViolations,
            );
        }

        if ((toolName === 'read_file' || toolName === 'fs.read') && (normalized.includes('.env') || normalized.includes('secret') || normalized.includes('.aws'))) {
            return this.block(
                this.policy.id || 'policy.credential-read',
                'credential read operation',
                amplificationReasons,
                'Replace direct credential reads with scoped secret injection or redacted fixtures.',
                contractViolations,
            );
        }

        if ((toolName === 'run_shell_command' || toolName === 'shell' || toolName === 'exec') && (normalized.includes('curl') || normalized.includes('wget')) && normalized.includes('| bash')) {
            return this.block(
                this.policy.id || 'policy.curl-bash',
                'unrestricted network execution (curl|bash)',
                amplificationReasons,
                'Fetch the artifact separately, verify its digest, then execute from a reviewed local path.',
                contractViolations,
            );
        }

        const blockingViolation = contractViolations.find((violation) => violation.blocking);
        if (blockingViolation) {
            return this.block(
                this.policy.id || 'policy.contract-violation',
                blockingViolation.message,
                amplificationReasons,
                blockingViolation.remediation,
                contractViolations,
            );
        }

        return {
            action: 'allow',
            reason: 'safe operation within active policy bounds',
            policyId: this.policy.id || 'policy.default-allow',
            amplificationReasons,
            remediationSuggestion: contractViolations.length > 0
                ? contractViolations.map((violation) => violation.remediation).join(' ')
                : 'No policy remediation required.',
            contractViolations,
        };
    }

    block(policyId, reason, amplificationReasons, remediationSuggestion, contractViolations = []) {
        return {
            action: 'block',
            reason,
            policyId,
            amplificationReasons,
            remediationSuggestion,
            contractViolations,
        };
    }

    evaluateContracts(toolName, normalizedArgs, runtimeContext) {
        const violations = [];

        for (const clause of this.policy.preconditions || []) {
            if (clause.tool && clause.tool !== toolName) continue;
            const passed = this.evaluateCondition(clause.requires || clause.condition, normalizedArgs, runtimeContext);
            if (!passed) {
                violations.push({
                    id: clause.id || `precondition.${toolName}`,
                    clause_type: 'precondition',
                    severity: clause.severity || 'HIGH',
                    message: clause.rationale || `precondition failed for ${toolName}`,
                    blocking: true,
                    remediation: `Satisfy precondition "${clause.requires || clause.condition}" before retrying ${toolName}.`,
                });
            }
        }

        for (const clause of this.policy.invariants || []) {
            const normalizedClause = this.normalizeClause(clause, 'invariant');
            const passed = this.evaluateCondition(normalizedClause.condition, normalizedArgs, runtimeContext);
            if (!passed) {
                violations.push({
                    id: normalizedClause.id,
                    clause_type: 'invariant',
                    severity: normalizedClause.severity || 'HIGH',
                    message: normalizedClause.message,
                    blocking: true,
                    remediation: normalizedClause.remediation,
                });
            }
        }

        for (const clause of this.policy.governance || []) {
            const normalizedClause = this.normalizeClause(clause, 'governance');
            const passed = this.evaluateCondition(normalizedClause.condition, normalizedArgs, runtimeContext);
            if (!passed) {
                violations.push({
                    id: normalizedClause.id,
                    clause_type: 'governance',
                    severity: normalizedClause.severity || 'MEDIUM',
                    message: normalizedClause.message,
                    blocking: normalizedClause.severity !== 'LOW',
                    remediation: normalizedClause.remediation,
                });
            }
        }

        return violations;
    }

    normalizeClause(clause, type) {
        if (typeof clause === 'string') {
            return {
                id: `${type}.${clause}`,
                condition: clause,
                severity: type === 'governance' ? 'MEDIUM' : 'HIGH',
                message: `${type} violation: ${clause}`,
                remediation: `Restore ${type} condition "${clause}".`,
            };
        }

        return {
            id: clause.id || `${type}.${clause.condition || clause.requires || 'unknown'}`,
            condition: clause.condition || clause.requires,
            severity: clause.severity || (type === 'governance' ? 'MEDIUM' : 'HIGH'),
            message: clause.rationale || `${type} violation: ${clause.condition || clause.requires}`,
            remediation: clause.remediation || `Restore ${type} condition "${clause.condition || clause.requires}".`,
        };
    }

    evaluateCondition(condition, normalizedArgs, runtimeContext = {}) {
        if (!condition) return true;
        const lowered = String(condition).trim().toLowerCase();

        if (lowered === 'true') return true;
        if (lowered === 'false') return false;
        if (lowered === 'user_approval == true') return runtimeContext.userApproval === true;
        if (lowered === 'no_pii_in_logs == true') return !/(ssn|social security|api[_-]?key|secret|token)/i.test(normalizedArgs);
        if (lowered === 'gdpr_compliance == true') return runtimeContext.gdprCompliant !== false;
        if (lowered === 'ccpa_compliance == true') return runtimeContext.ccpaCompliant !== false;
        if (lowered === 'goal_matches_task == true') return runtimeContext.goalMatchesTask !== false;
        if (lowered === 'network_scope <= internal') return runtimeContext.networkScope !== 'external';

        if (/==\s*true$/.test(lowered)) {
            const key = lowered.replace(/==\s*true$/, '').trim();
            return Boolean(runtimeContext[key]);
        }

        return !normalizedArgs.includes(lowered);
    }
}

export {  PolicyEngine  };
