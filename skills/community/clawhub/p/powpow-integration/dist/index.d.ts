/**
 * OpenClaw POWPOW Integration Skill v2.1.10
 *
 * WebSocket-based real-time bidirectional chat with POWPOW digital humans
 */
import { EventEmitter } from 'events';
import { logger } from './utils/logger';
interface PowPowConfig {
    wsUrl: string;
    digitalHumanId: string;
    openclawUserId: string;
    autoReconnect?: boolean;
    reconnectInterval?: number;
    maxReconnectAttempts?: number;
}
declare class PowPowSkill extends EventEmitter {
    private ws;
    private config;
    private isConnected;
    private reconnectTimer;
    private heartbeatTimer;
    private messageQueue;
    private connectionStartTime;
    private reconnectAttempts;
    private connectionTimeout;
    constructor(config: PowPowConfig);
    /**
     * Connect to POWPOW WebSocket server
     */
    connect(): Promise<void>;
    /**
     * Disconnect from WebSocket server
     */
    disconnect(): void;
    /**
     * Cleanup resources
     */
    private cleanup;
    /**
     * Start heartbeat
     */
    private startHeartbeat;
    /**
     * Send chat message
     */
    sendMessage(content: string, contentType?: 'text' | 'voice' | 'image', options?: {
        mediaUrl?: string;
        duration?: number;
    }): boolean;
    /**
     * Quick reply
     */
    reply(content: string): boolean;
    /**
     * Send voice message
     */
    sendVoice(content: string, mediaUrl: string, duration: number): boolean;
    /**
     * Send image message
     */
    sendImage(content: string, mediaUrl: string): boolean;
    /**
     * Get connection status
     */
    getConnectionStatus(): {
        connected: boolean;
        digitalHumanId: string;
        duration?: number;
        reconnectAttempts: number;
    };
    /**
     * Handle incoming messages
     */
    private handleMessage;
    /**
     * Flush queued messages
     */
    private flushMessageQueue;
    /**
     * Schedule reconnection
     */
    private scheduleReconnect;
}
interface OpenClawContext {
    userId: string;
    config: any;
    powpowSkill?: PowPowSkill;
    emit: (event: string, data: any) => void;
}
declare const powpowSkillPlugin: {
    name: string;
    version: string;
    description: string;
    init(context: any): void;
    destroy(): void;
    commands: {
        /**
         * Connect to POWPOW
         */
        connect(params: {
            digitalHumanId: string;
            wsUrl?: string;
        }, context: OpenClawContext): Promise<{
            success: boolean;
            error: string | undefined;
            message?: undefined;
            digitalHumanId?: undefined;
        } | {
            success: boolean;
            message: string;
            digitalHumanId: string;
            error?: undefined;
        }>;
        /**
         * Disconnect from POWPOW
         */
        disconnect(params: {}, context: OpenClawContext): {
            success: boolean;
            message: string;
            error?: undefined;
        } | {
            success: boolean;
            error: string;
            message?: undefined;
        };
        /**
         * Get connection status
         */
        status(params: {}, context: OpenClawContext): {
            success: boolean;
            status: string;
            message: string;
            digitalHumanId?: undefined;
            duration?: undefined;
            reconnectAttempts?: undefined;
        } | {
            success: boolean;
            status: string;
            digitalHumanId: string;
            duration: number | undefined;
            reconnectAttempts: number;
            message: string;
        };
        /**
         * Send message
         */
        send(params: {
            message: string;
            contentType?: string;
        }, context: OpenClawContext): {
            success: boolean;
            error: string;
            message?: undefined;
        } | {
            success: boolean;
            message: string;
            error?: undefined;
        };
        /**
         * Quick reply
         */
        reply(params: {
            message: string;
        }, context: OpenClawContext): {
            success: boolean;
            error: string;
            message?: undefined;
        } | {
            success: boolean;
            message: string;
            error?: undefined;
        };
        /**
         * Send voice message
         */
        sendVoice(params: {
            content: string;
            mediaUrl: string;
            duration: number;
        }, context: OpenClawContext): {
            success: boolean;
            error: string;
            message?: undefined;
        } | {
            success: boolean;
            message: string;
            error?: undefined;
        };
        /**
         * Send image message
         */
        sendImage(params: {
            content: string;
            mediaUrl: string;
        }, context: OpenClawContext): {
            success: boolean;
            error: string;
            message?: undefined;
        } | {
            success: boolean;
            message: string;
            error?: undefined;
        };
        /**
         * Start listening for messages
         */
        listen(params: {
            autoReply?: boolean;
        }, context: OpenClawContext): {
            success: boolean;
            error: string;
            message?: undefined;
        } | {
            success: boolean;
            message: string;
            error?: undefined;
        };
        /**
         * Stop listening for messages
         */
        stopListen(params: {}, context: OpenClawContext): {
            success: boolean;
            message: string;
            error?: undefined;
        } | {
            success: boolean;
            error: string;
            message?: undefined;
        };
    };
};
export { PowPowSkill, powpowSkillPlugin, logger };
export default powpowSkillPlugin;
//# sourceMappingURL=index.d.ts.map