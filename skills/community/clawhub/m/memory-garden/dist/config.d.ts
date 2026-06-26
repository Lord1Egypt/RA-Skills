export interface SkillConfig {
    daemonUrl: string;
    extraction: {
        enabled: boolean;
        confirmRequired: boolean;
    };
    sync: {
        enabled: boolean;
    };
    search: {
        enabled: boolean;
        limit: number;
    };
}
export declare function loadConfig(): SkillConfig;
export declare function validateConfig(config: SkillConfig): string[];
//# sourceMappingURL=config.d.ts.map