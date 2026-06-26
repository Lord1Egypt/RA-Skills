/**
 * 常量定义
 * 集中管理所有配置参数
 */
export declare const WS_CONFIG: {
    readonly DEFAULT_URL: "wss://global.powpow.online:8080";
    readonly RECONNECT_INTERVAL: 3000;
    readonly MAX_RECONNECT_ATTEMPTS: 10;
    readonly HEARTBEAT_INTERVAL: 30000;
    readonly CONNECTION_TIMEOUT: 10000;
};
export declare const MESSAGE_CONFIG: {
    readonly MAX_LENGTH: 2000;
    readonly QUEUE_SIZE: 100;
    readonly BATCH_SIZE: 10;
};
export declare const VALIDATION_CONFIG: {
    readonly DIGITAL_HUMAN_ID_MIN: 1;
    readonly DIGITAL_HUMAN_ID_MAX: 100;
    readonly USER_ID_MIN: 1;
    readonly USER_ID_MAX: 100;
};
export declare const CONTENT_TYPES: {
    readonly TEXT: "text";
    readonly VOICE: "voice";
    readonly IMAGE: "image";
};
export declare const SENDER_TYPES: {
    readonly USER: "user";
    readonly OPENCLAW: "openclaw";
};
export declare const WS_MESSAGE_TYPES: {
    readonly CHAT_MESSAGE: "chat_message";
    readonly CHAT_MESSAGE_ACK: "chat_message_ack";
    readonly CONNECTED: "connected";
    readonly ERROR: "error";
    readonly PING: "ping";
    readonly PONG: "pong";
};
//# sourceMappingURL=constants.d.ts.map