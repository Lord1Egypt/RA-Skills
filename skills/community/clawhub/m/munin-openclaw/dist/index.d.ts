export declare function createOpenClawMuninAdapter(config: {
    baseUrl: string;
    apiKey?: string;
    timeoutMs?: number;
}): {
    execute: (projectId: string, action: string, payload: Record<string, unknown>) => Promise<import("@kalera/munin-sdk").MuninResponse<unknown>>;
    capabilities: () => Promise<import("@kalera/munin-sdk").MuninCapabilities>;
};
