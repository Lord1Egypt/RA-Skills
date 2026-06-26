export type CacheMissReason = 'system_prompt_changed' | 'identity_block_changed' | 'tool_schema_changed' | 'volatile_tail_moved' | 'model_changed' | 'temperature_changed' | 'attachments_changed' | 'message_order_changed' | 'memory_injection_changed' | 'agent_list_changed' | 'fork_policy_changed' | 'response_format_changed' | 'safety_prefix_changed' | 'uncached_zone_mutated';
export declare class CostGovernor {
    private calls;
    recordCall(call: {
        id: string;
        cached: boolean;
        tokens: number;
        invalid: boolean;
        missReason?: CacheMissReason;
    }): void;
    summarize(): {
        totalCalls: number;
        invalidCalls: number;
        cachedCalls: number;
        missReasons: Partial<Record<CacheMissReason, number>>;
        totalTokens: number;
    };
    getMissReasonCatalog(): CacheMissReason[];
}
export default CostGovernor;
