// @ts-nocheck
'use strict';

import { PATTERNS  } from '../patterns';

function buildScope(rule) {
    if (rule.scope) return rule.scope;
    if (rule.codeOnly) return 'code';
    if (rule.docOnly) return 'doc';
    if (rule.skillDocOnly) return 'skill-doc';
    return 'all';
}

function normalizeRule(rule) {
    return {
        id: rule.id,
        category: rule.category || rule.cat || 'unknown',
        severity: rule.severity || 'LOW',
        description: rule.description || rule.desc || rule.id,
        scope: buildScope(rule),
        evidence: rule.evidence || ['regex-match'],
        remediation: rule.remediation || rule.remediationHint || 'Review the finding and remove or isolate the risky construct.',
        rationale: rule.rationale || 'Pattern matches a known risky construct.',
        preconditions: rule.preconditions || rule.exploitPrecondition || 'The matched content must be reachable in execution or agent control flow.',
        tests: Array.isArray(rule.tests) ? rule.tests : [],
        regex: rule.regex,
        codeOnly: !!rule.codeOnly,
        docOnly: !!rule.docOnly,
        skillDocOnly: !!rule.skillDocOnly,
        all: rule.all !== false && !rule.codeOnly && !rule.docOnly && !rule.skillDocOnly,
    };
}

class RuleRegistry {
    constructor(baseRules = PATTERNS, customRules = []) {
        this.baseRules = baseRules.map(normalizeRule);
        this.customRules = customRules.map(normalizeRule);
    }

    withCustomRules(customRules = []) {
        return new RuleRegistry(this.baseRules, customRules);
    }

    getAllRules() {
        return [...this.baseRules, ...this.customRules];
    }

    getRuleById(id) {
        return this.getAllRules().find((rule) => rule.id === id) || null;
    }

    getRulesForFileType(fileType) {
        return this.getAllRules().filter((rule) => {
            if (rule.scope === 'all') return true;
            if (rule.scope === 'code') return fileType === 'code';
            if (rule.scope === 'doc') return fileType === 'doc';
            if (rule.scope === 'skill-doc') return fileType === 'skill-doc';
            return true;
        });
    }

    getStats() {
        const allRules = this.getAllRules();
        return {
            total: allRules.length,
            categories: new Set(allRules.map((rule) => rule.category)).size,
        };
    }
}

export { 
    RuleRegistry,
    normalizeRule,
 };
