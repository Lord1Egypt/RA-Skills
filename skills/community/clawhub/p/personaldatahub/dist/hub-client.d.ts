/**
 * Thin HTTP client wrapping the PersonalDataHub App API endpoints.
 * The skill does not know about manifests or policies — it simply
 * sends requests with a `purpose` string. The Hub resolves the policy internally.
 */
export interface PullParams {
    source: string;
    type?: string;
    params?: Record<string, unknown>;
    purpose: string;
}
export interface ProposeParams {
    source: string;
    action_type: string;
    action_data: Record<string, unknown>;
    purpose: string;
}
export interface PullResult {
    ok: boolean;
    data: Array<{
        source: string;
        source_item_id: string;
        type: string;
        timestamp: string;
        data: Record<string, unknown>;
    }>;
    meta?: Record<string, unknown>;
}
export interface ProposeResult {
    ok: boolean;
    actionId: string;
    status: string;
}
export interface HubClientConfig {
    hubUrl: string;
    apiKey: string;
}
export declare class HubClient {
    private hubUrl;
    private apiKey;
    constructor(config: HubClientConfig);
    /**
     * Pull data from a source through PersonalDataHub.
     * The Hub applies the owner's manifest/policy to filter, redact, and shape the data.
     */
    pull(params: PullParams): Promise<PullResult>;
    /**
     * Propose an outbound action through PersonalDataHub staging.
     * The action goes to the owner's staging queue for review before execution.
     */
    propose(params: ProposeParams): Promise<ProposeResult>;
}
export declare class HubApiError extends Error {
    readonly endpoint: string;
    readonly statusCode: number;
    readonly body: string;
    constructor(endpoint: string, statusCode: number, body: string);
}
