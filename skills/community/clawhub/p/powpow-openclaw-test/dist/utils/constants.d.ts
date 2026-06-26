/**
 * 常量定义
 */
export declare const API_CONFIG: {
    readonly DEFAULT_URL: "https://global.powpow.online";
    readonly REQUEST_TIMEOUT: 30000;
};
export declare const VALIDATION_CONFIG: {
    readonly DIGITAL_HUMAN_ID_MIN: 1;
    readonly DIGITAL_HUMAN_ID_MAX: 100;
    readonly USER_ID_MIN: 1;
    readonly USER_ID_MAX: 100;
    readonly USERNAME_MIN: 3;
    readonly USERNAME_MAX: 20;
    readonly PASSWORD_MIN: 6;
    readonly PASSWORD_MAX: 50;
};
export declare const API_ENDPOINTS: {
    readonly REGISTER: "/api/auth/register";
    readonly LOGIN: "/api/auth/login";
    readonly DIGITAL_HUMANS: "/api/openclaw/digital-humans";
    readonly CHAT_SEND: "/api/openclaw/chat/send";
    readonly CHAT_HISTORY: "/api/openclaw/chat/history";
};
