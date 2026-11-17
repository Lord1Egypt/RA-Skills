"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PolicyEngineService = void 0;
const fs_1 = __importDefault(require("fs"));
class PolicyEngineService {
    rules = [
        { id: 'default_deny', match: {}, decision: 'deny' }
    ];
    constructor(configPath) {
        if (configPath && fs_1.default.existsSync(configPath)) {
            const { readPrivate } = require('../../transport');
            const rules = JSON.parse(readPrivate(configPath));
            if (!Array.isArray(rules) || rules.length > 128)
                throw new Error('Invalid policy');
            for (const rule of [...rules].reverse())
                this.addRule(rule);
        }
    }
    addRule(rule) {
        if (!rule || !rule.id || !rule.match || !['allow', 'deny', 'review'].includes(rule.decision))
            throw new Error('Invalid rule');
        if (rule.rate_limit)
            throw new Error('Rate-limit rules require an external limiter');
        this.rules.unshift(rule);
    }
    async evaluate(req, skill) {
        for (const rule of this.rules) {
            if (this.matches(rule, req, skill)) {
                return {
                    decision: rule.decision,
                    rule_matched: rule.id,
                    required_verifiers: rule.required_verifiers
                };
            }
        }
        return { decision: 'deny', rule_matched: 'default_deny' };
    }
    matches(rule, req, skill) {
        if (rule.match.action && !this.globMatch(req.action, rule.match.action))
            return false;
        if (rule.match.target && !this.globMatch(req.target, rule.match.target))
            return false;
        if (rule.match.skill && skill.skill_id !== rule.match.skill)
            return false;
        if (rule.match.risk_level && skill.risk_level !== rule.match.risk_level)
            return false;
        return true;
    }
    globMatch(input, pattern) {
        const regex = new RegExp('^' + pattern.split('').map(c => c === '*' ? '.*' : c === '?' ? '.' : c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('') + '$');
        return regex.test(input);
    }
}
exports.PolicyEngineService = PolicyEngineService;
//# sourceMappingURL=policy.js.map