"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const CrossAgentExtension = {
    name: 'ext.cross_agent',
    version: '2.0',
    async init(guard) {
        console.log('[JEP Guard] ext.cross_agent v2.0 loaded');
    },
    async evaluate(request) {
        if (request.type === 'skill_delegate') {
            return { action: 'allow', rule_matched: 'cross_agent_permitted' };
        }
        return { action: 'allow', rule_matched: 'not_applicable' };
    }
};
exports.default = CrossAgentExtension;
//# sourceMappingURL=cross-agent.js.map