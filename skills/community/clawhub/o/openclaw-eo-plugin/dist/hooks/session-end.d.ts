/**
 * Session End Hook
 * Analyzes session, triggers continuous learning loop
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
export interface SessionEndData {
    toolsUsed: string[];
    messageCount: number;
    lastMessage: string;
    feishuChatId?: string;
}
export declare function onSessionEnd(api: OpenClawPluginApi, data: SessionEndData): Promise<void>;
export declare function createSessionEndHook(api: OpenClawPluginApi): {
    id: string;
    name: string;
    description: string;
    handle: (event: any) => Promise<void>;
};
//# sourceMappingURL=session-end.d.ts.map