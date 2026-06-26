/**
 * Proactive Monitor Hook v2
 * Monitors user messages and detects when EO assistance might be helpful
 *
 *主动感知核心：当检测到高置信度意图时，发送建议给用户
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
export interface ProactiveMonitorConfig {
    enabled: boolean;
    threshold: number;
    autoSuggestThreshold: number;
    feishuChatId?: string;
}
export declare function configureProactiveMonitor(cfg: Partial<ProactiveMonitorConfig>): void;
export declare function checkMessage(api: OpenClawPluginApi, message: string): Promise<string | null>;
export declare function createProactiveMonitorHook(api: OpenClawPluginApi): {
    id: string;
    name: string;
    description: string;
    handle: (event: any) => Promise<void>;
};
//# sourceMappingURL=proactive-monitor.d.ts.map