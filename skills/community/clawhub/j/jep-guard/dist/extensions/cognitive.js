"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const CognitiveExtension = {
    name: 'ext.cognitive_attestation',
    version: '1.0',
    async init(guard) {
        console.log('[JEP Guard] ext.cognitive_attestation v1.0 loaded');
    },
    async evaluate(request) {
        if (request.type === 'model_inference') {
            return { action: 'allow', rule_matched: 'cognitive_not_configured' };
        }
        return { action: 'allow', rule_matched: 'not_applicable' };
    }
};
exports.default = CognitiveExtension;
//# sourceMappingURL=cognitive.js.map