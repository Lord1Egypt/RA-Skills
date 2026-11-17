import fs from "fs";
import { ExecutionRequest, SkillIdentity, PolicyRule, PolicyResult } from '../core/types';

export class PolicyEngineService {
  private rules: PolicyRule[] = [
    { id: 'default_deny', match: {}, decision: 'deny' }
  ];

  constructor(configPath?: string) {
    if(configPath && fs.existsSync(configPath)) {
      const {readPrivate}=require('../../transport');
      const rules=JSON.parse(readPrivate(configPath));
      if(!Array.isArray(rules) || rules.length>128) throw new Error('Invalid policy');
      for(const rule of [...rules].reverse()) this.addRule(rule);
    }
  }

  addRule(rule: PolicyRule): void {
    if(!rule || !rule.id || !rule.match || !['allow','deny','review'].includes(rule.decision)) throw new Error('Invalid rule');
    if(rule.rate_limit) throw new Error('Rate-limit rules require an external limiter');
    this.rules.unshift(rule);
  }

  async evaluate(req: ExecutionRequest, skill: SkillIdentity): Promise<PolicyResult> {
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

  private matches(rule: PolicyRule, req: ExecutionRequest, skill: SkillIdentity): boolean {
    if (rule.match.action && !this.globMatch(req.action, rule.match.action)) return false;
    if (rule.match.target && !this.globMatch(req.target, rule.match.target)) return false;
    if (rule.match.skill && skill.skill_id !== rule.match.skill) return false;
    if (rule.match.risk_level && skill.risk_level !== rule.match.risk_level) return false;
    return true;
  }

  private globMatch(input: string, pattern: string): boolean {
    const regex = new RegExp('^' + pattern.split('').map(c => c==='*' ? '.*' : c==='?' ? '.' : c.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('') + '$');
    return regex.test(input);
  }
}