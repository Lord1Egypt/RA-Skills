/**
 * Dream Trigger Hook
 * Triggers dream module for self-evolution based on conditions
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
export interface DreamTriggerConfig {
    enabled: boolean;
    afterSessions: number;
    afterHours: number;
}
export declare function configureDreamTrigger(cfg: Partial<DreamTriggerConfig>): void;
export declare function incrementSession(): void;
export declare function shouldTriggerDream(): boolean;
export declare function triggerDream(api: OpenClawPluginApi): Promise<void>;
export declare function createDreamTriggerHook(api: OpenClawPluginApi): {
    id: string;
    name: string;
    description: string;
    handle: (event: any) => Promise<void>;
};
//# sourceMappingURL=dream-trigger.d.ts.map