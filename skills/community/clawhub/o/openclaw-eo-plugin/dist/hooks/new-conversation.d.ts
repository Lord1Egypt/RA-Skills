/**
 * New Conversation Hook v1.0.0
 *
 * Detects new Feishu conversations and triggers automatic workspace allocation.
 * Works with Auto Workspace Manager to provide seamless multi-project support.
 *
 * Flow:
 * 1. on_message fires → check if peer_id is registered
 * 2. If NEW → mark context as "needsAllocation" → inject into context
 * 3. Agent sees "needsAllocation" → asks user what project this is
 * 4. User answers → agent calls setupNewSession() to complete allocation
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
export interface NewConversationContext {
    isNewConversation: boolean;
    peerId?: string;
    peerType?: 'group' | 'channel' | 'user';
    channel?: string;
    sessionId?: string;
    needsAllocation: boolean;
    suggestedProjectName?: string;
}
/**
 * Create the new conversation detection hook
 */
export declare function createNewConversationHook(api: OpenClawPluginApi): {
    id: string;
    name: string;
    description: string;
    version: string;
    hookType: "on_message";
    handle: (event: any) => Promise<void>;
};
/**
 * Helper function to check if a conversation needs allocation
 */
export declare function needsAllocation(event: any): boolean;
/**
 * Get allocation hint from event
 */
export declare function getAllocationHint(event: any): {
    peerId: string;
    suggestedName?: string;
} | null;
//# sourceMappingURL=new-conversation.d.ts.map