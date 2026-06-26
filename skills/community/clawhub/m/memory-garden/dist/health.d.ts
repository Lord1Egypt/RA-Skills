export interface HealthStatus {
    healthy: boolean;
    daemon: {
        running: boolean;
        url: string;
        version?: string;
        patternCount?: number;
    };
    skill: {
        version: string;
        searchEnabled: boolean;
        extractionEnabled: boolean;
        syncEnabled: boolean;
    };
}
export declare function checkHealth(daemonUrl: string, config: {
    searchEnabled: boolean;
    extractionEnabled: boolean;
    syncEnabled: boolean;
}): Promise<HealthStatus>;
export declare function formatHealthStatus(status: HealthStatus): string;
//# sourceMappingURL=health.d.ts.map