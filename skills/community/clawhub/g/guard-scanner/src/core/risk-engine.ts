// @ts-nocheck
'use strict';

const SEVERITY_WEIGHTS = { CRITICAL: 40, HIGH: 15, MEDIUM: 5, LOW: 2 };

function severityBaseConfidence(severity) {
    if (severity === 'CRITICAL') return 0.95;
    if (severity === 'HIGH') return 0.82;
    if (severity === 'MEDIUM') return 0.65;
    return 0.5;
}

function normalizeConfidence(finding) {
    if (typeof finding.confidence === 'number') {
        return Math.max(0, Math.min(1, Number(finding.confidence.toFixed(3))));
    }
    if (finding.validation_state === 'chain-validated' || finding.validated === true) return 0.98;
    if (finding.validation_state === 'semantic-match') return 0.9;
    if (finding.validation_state === 'runtime-observed' || finding.source === 'runtime') return 0.99;
    return severityBaseConfidence(finding.severity);
}

function detectAttackChainId(findings) {
    const ids = new Set(findings.map((finding) => finding.id || finding.rule_id));
    const categories = new Set(findings.map((finding) => finding.cat || finding.category));
    if (ids.has('AST_FETCH_TO_EXEC')) return 'remote-fetch-exec';
    if (categories.has('credential-handling') && categories.has('exfiltration')) return 'credential-exfiltration';
    if (categories.has('identity-hijack') && categories.has('persistence')) return 'identity-persistence';
    if (categories.has('prompt-injection') && categories.has('a2a-contagion')) return 'prompt-contagion';
    return null;
}

function enrichFinding(finding, sharedAttackChainId = null) {
    const confidence = normalizeConfidence(finding);
    return {
        ...finding,
        confidence,
        attack_chain_id: finding.attack_chain_id || sharedAttackChainId || null,
    };
}

function calculateRisk(findings) {
    if (findings.length === 0) return 0;

    const attackChainId = detectAttackChainId(findings);
    const enriched = findings.map((finding) => enrichFinding(finding, attackChainId));

    let score = 0;
    for (const finding of enriched) {
        const weight = SEVERITY_WEIGHTS[finding.severity] || 0;
        score += weight * finding.confidence;
    }

    const ids = new Set(enriched.map((finding) => finding.id || finding.rule_id));
    const categories = new Set(enriched.map((finding) => finding.cat || finding.category));

    if (categories.has('credential-handling') && categories.has('exfiltration')) score *= 2.2;
    if (categories.has('credential-handling') && enriched.some((finding) => finding.id === 'MAL_CHILD' || finding.id === 'MAL_EXEC')) score *= 1.5;
    if (categories.has('obfuscation') && (categories.has('malicious-code') || categories.has('credential-handling'))) score *= 1.8;
    if (ids.has('DEP_LIFECYCLE_EXEC')) score *= 2;
    if (ids.has('PI_BIDI') && enriched.length > 1) score *= 1.3;
    if (categories.has('leaky-skills') && (categories.has('exfiltration') || categories.has('malicious-code'))) score *= 2;
    if (categories.has('memory-poisoning')) score *= 1.5;
    if (categories.has('prompt-worm')) score *= 2;
    if (categories.has('cve-patterns')) score = Math.max(score, 70);
    if (categories.has('persistence') && (categories.has('malicious-code') || categories.has('credential-handling') || categories.has('memory-poisoning'))) score *= 1.5;
    if (categories.has('identity-hijack')) score *= 2;
    if (categories.has('identity-hijack') && (categories.has('persistence') || categories.has('memory-poisoning'))) score = Math.max(score, 90);
    if (ids.has('IOC_IP') || ids.has('IOC_URL') || ids.has('KNOWN_TYPOSQUAT')) score = 100;
    if (categories.has('config-impact')) score *= 2;
    if (categories.has('config-impact') && categories.has('sandbox-validation')) score = Math.max(score, 70);
    if (categories.has('complexity') && (categories.has('malicious-code') || categories.has('obfuscation'))) score *= 1.5;
    if (categories.has('pii-exposure') && categories.has('exfiltration')) score *= 3;
    if (categories.has('pii-exposure') && (ids.has('SHADOW_AI_OPENAI') || ids.has('SHADOW_AI_ANTHROPIC') || ids.has('SHADOW_AI_GENERIC'))) score *= 2.5;
    if (categories.has('pii-exposure') && categories.has('credential-handling')) score *= 2;
    if (attackChainId) score *= 1.2;

    return Math.min(100, Math.round(score));
}

function getVerdict(risk, thresholds) {
    if (risk >= thresholds.malicious) return { icon: '🔴', label: 'MALICIOUS', stat: 'malicious' };
    if (risk >= thresholds.suspicious) return { icon: '🟡', label: 'SUSPICIOUS', stat: 'suspicious' };
    if (risk > 0) return { icon: '🟢', label: 'LOW RISK', stat: 'low' };
    return { icon: '🟢', label: 'CLEAN', stat: 'clean' };
}

export { 
    SEVERITY_WEIGHTS,
    calculateRisk,
    getVerdict,
    enrichFinding,
    detectAttackChainId,
 };
