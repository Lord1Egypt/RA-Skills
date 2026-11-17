"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const extension = { name: 'ext.aegis', version: '2.0', async init() { }, async evaluate() { return { action: 'review', rule_matched: 'explicit_trusted_adapter_required' }; } };
exports.default = extension;
//# sourceMappingURL=aegis.js.map