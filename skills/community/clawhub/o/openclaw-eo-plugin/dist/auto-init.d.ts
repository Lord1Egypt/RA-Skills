/**
 * EO Auto-Init Module
 *
 * Automatically configures all agent workspaces with EO-Enhanced SOUL.md
 * Runs on plugin installation/load to enable full EO capabilities
 */
export interface EOConfigOptions {
    force?: boolean;
    dryRun?: boolean;
    agentIds?: string[];
}
export interface InitResult {
    agentId: string;
    workspace: string;
    status: 'success' | 'skipped' | 'failed';
    reason?: string;
    error?: string;
}
export interface AutoInitResults {
    total: number;
    success: number;
    skipped: number;
    failed: number;
    results: InitResult[];
}
/**
 * Run auto-initialization for all agent workspaces
 */
export declare function runAutoInit(api: any, options?: EOConfigOptions): Promise<AutoInitResults>;
/**
 * Check if auto-init has been run before
 */
export declare function isAutoInitDone(): boolean;
//# sourceMappingURL=auto-init.d.ts.map