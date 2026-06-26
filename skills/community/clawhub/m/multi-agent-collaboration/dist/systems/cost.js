"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CostGovernor = void 0;
class CostGovernor {
    constructor() {
        this.calls = [];
    }
    recordCall(call) {
        this.calls.push(call);
    }
    summarize() {
        const missReasons = {};
        for (const call of this.calls) {
            if (call.missReason) {
                missReasons[call.missReason] = (missReasons[call.missReason] || 0) + 1;
            }
        }
        return {
            totalCalls: this.calls.length,
            invalidCalls: this.calls.filter((c) => c.invalid).length,
            cachedCalls: this.calls.filter((c) => c.cached).length,
            missReasons,
            totalTokens: this.calls.reduce((sum, c) => sum + c.tokens, 0)
        };
    }
    getMissReasonCatalog() {
        return [
            'system_prompt_changed',
            'identity_block_changed',
            'tool_schema_changed',
            'volatile_tail_moved',
            'model_changed',
            'temperature_changed',
            'attachments_changed',
            'message_order_changed',
            'memory_injection_changed',
            'agent_list_changed',
            'fork_policy_changed',
            'response_format_changed',
            'safety_prefix_changed',
            'uncached_zone_mutated'
        ];
    }
}
exports.CostGovernor = CostGovernor;
exports.default = CostGovernor;
