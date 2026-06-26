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
import * as fs from 'fs';
import * as path from 'path';
import { PLUGIN_VERSION } from '../config.js';
// Registry path for tracking known conversations
const SESSION_REGISTRY_PATH = '.openclaw/session-registry.json';
const OPENCLAW_CONFIG_PATH = '.openclaw/openclaw.json';
/**
 * Get workspace root from environment or default
 */
function getWorkspaceRoot() {
    return process.env.OPENCLAW_WORKSPACE_ROOT || process.cwd() || '/home/zzy/.openclaw/workspace/workspace-jisu';
}
/**
 * Load existing known conversations from registry
 */
function loadKnownConversations(workspaceRoot) {
    const known = new Set();
    try {
        // Check session-registry.json
        const registryPath = path.join(workspaceRoot, '..', SESSION_REGISTRY_PATH);
        if (fs.existsSync(registryPath)) {
            const content = fs.readFileSync(registryPath, 'utf-8');
            const data = JSON.parse(content);
            if (data.bindings) {
                for (const [, binding] of data.bindings) {
                    const b = binding;
                    if (b.peerId)
                        known.add(b.peerId);
                    if (b.peer?.id)
                        known.add(b.peer.id);
                }
            }
        }
    }
    catch {
        // Registry doesn't exist yet
    }
    try {
        // Check openclaw.json bindings
        const configPath = path.join(workspaceRoot, '..', '..', OPENCLAW_CONFIG_PATH);
        if (fs.existsSync(configPath)) {
            const content = fs.readFileSync(configPath, 'utf-8');
            const config = JSON.parse(content);
            const bindings = config.bindings || [];
            for (const binding of bindings) {
                if (binding.match?.peer?.id) {
                    known.add(binding.match.peer.id);
                }
            }
        }
    }
    catch {
        // Config doesn't exist yet
    }
    return known;
}
/**
 * Extract peer info from message event
 */
function extractPeerInfo(event) {
    // Try various possible structures based on OpenClaw event format
    const peerId = event?.context?.peer?.id ||
        event?.peer?.id ||
        event?.message?.peer?.id ||
        event?.chat_id ||
        event?.context?.chat_id ||
        undefined;
    const peerType = event?.context?.peer?.kind ||
        event?.peer?.kind ||
        event?.peerType ||
        undefined;
    const channel = event?.context?.channel ||
        event?.channel ||
        'feishu';
    const sessionId = event?.sessionId ||
        event?.context?.sessionId ||
        undefined;
    return { peerId, peerType, channel, sessionId };
}
/**
 * Infer project name from conversation context
 */
function inferProjectName(event) {
    // Try group name/subject
    const groupName = event?.context?.groupSubject ||
        event?.groupSubject ||
        event?.message?.groupSubject ||
        event?.context?.roomName ||
        event?.roomName ||
        undefined;
    if (groupName) {
        // Clean up the name - keep Chinese and alphanumeric
        const cleaned = groupName.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]+/g, '-').replace(/-+/g, '-');
        return cleaned.slice(0, 30);
    }
    // Try from peer ID pattern (e.g., "oc_xxx" → extract hint)
    const peerId = event?.context?.peer?.id || event?.peer?.id || '';
    if (peerId.startsWith('oc_')) {
        return `群组-${peerId.slice(0, 8)}`;
    }
    return undefined;
}
/**
 * Create the new conversation detection hook
 */
export function createNewConversationHook(api) {
    return {
        id: 'eo_new_conversation',
        name: 'EO New Conversation Detector',
        description: 'Detects new conversations and triggers workspace allocation',
        version: PLUGIN_VERSION,
        // Use onMessage hook for detection (fires for every message)
        hookType: 'on_message',
        handle: async (event) => {
            const peerInfo = extractPeerInfo(event);
            // Skip if no peer info
            if (!peerInfo.peerId) {
                api.logger.debug('[EO NewConversation] No peer info, skipping');
                return;
            }
            // Skip if not a Feishu channel (only auto-allocate Feishu for now)
            if (peerInfo.channel !== 'feishu') {
                return;
            }
            // Load known conversations
            const workspaceRoot = getWorkspaceRoot();
            const knownConversations = loadKnownConversations(workspaceRoot);
            const isNew = !knownConversations.has(peerInfo.peerId);
            api.logger.debug(`[EO NewConversation v${PLUGIN_VERSION}] peer=${peerInfo.peerId}, isNew=${isNew}`);
            if (isNew) {
                // This is a NEW conversation - inject allocation context
                const suggestedName = inferProjectName(event);
                const allocationContext = {
                    isNewConversation: true,
                    peerId: peerInfo.peerId,
                    peerType: peerInfo.peerType || 'group',
                    channel: peerInfo.channel,
                    sessionId: peerInfo.sessionId,
                    needsAllocation: true,
                    suggestedProjectName: suggestedName,
                };
                // Inject into event context
                event.context = event.context || {};
                event.context.eoNewConversation = allocationContext;
                // Also set a flag that the agent can check
                event.context.eoNeedsAllocation = true;
                event.context.eoAllocationHint = {
                    peerId: peerInfo.peerId,
                    suggestedName: suggestedName,
                };
                api.logger.info(`[EO NewConversation] New conversation detected: ${peerInfo.peerId}, suggested: ${suggestedName}`);
            }
            else {
                // Existing conversation - just mark as known
                api.logger.debug(`[EO NewConversation] Known conversation: ${peerInfo.peerId}`);
                event.context = event.context || {};
                event.context.eoNewConversation = {
                    isNewConversation: false,
                    needsAllocation: false,
                };
            }
        },
    };
}
/**
 * Helper function to check if a conversation needs allocation
 */
export function needsAllocation(event) {
    return event?.context?.eoNeedsAllocation === true;
}
/**
 * Get allocation hint from event
 */
export function getAllocationHint(event) {
    if (!needsAllocation(event))
        return null;
    return {
        peerId: event.context.eoAllocationHint.peerId,
        suggestedName: event.context.eoAllocationHint.suggestedName,
    };
}
//# sourceMappingURL=new-conversation.js.map