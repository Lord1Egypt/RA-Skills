import { ExecutionRequest, SkillIdentity, PolicyRule, PolicyResult } from '../core/types';
export declare class PolicyEngineService {
    private rules;
    constructor(configPath?: string);
    addRule(rule: PolicyRule): void;
    evaluate(req: ExecutionRequest, skill: SkillIdentity): Promise<PolicyResult>;
    private matches;
    private globMatch;
}
