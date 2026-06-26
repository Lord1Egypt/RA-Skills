/**
 * POWPOW Simple Skill - 常量定义
 */
export declare const API_ENDPOINTS: {
    readonly REGISTER: "/api/openclaw/auth/register";
    readonly LOGIN: "/api/auth/login";
    readonly UPLOAD_AVATAR: "/api/upload/avatar";
    readonly CREATE_DIGITAL_HUMAN: "/api/openclaw/digital-humans";
    readonly LIST_DIGITAL_HUMANS: "/api/openclaw/digital-humans";
    readonly RENEW_DIGITAL_HUMAN: (id: string) => string;
    readonly AMAP_GEOCODE: "https://restapi.amap.com/v3/geocode/geo";
};
export declare const VALIDATION: {
    readonly USERNAME: {
        readonly MIN_LENGTH: 2;
        readonly MAX_LENGTH: 50;
        readonly PATTERN: RegExp;
    };
    readonly PASSWORD: {
        readonly MIN_LENGTH: 6;
        readonly MAX_LENGTH: 100;
    };
    readonly DIGITAL_HUMAN: {
        readonly NAME_MIN_LENGTH: 2;
        readonly NAME_MAX_LENGTH: 50;
        readonly DESCRIPTION_MAX_LENGTH: 500;
    };
};
export declare const ERROR_CODES: {
    readonly AUTH_REQUIRED: "AUTH_REQUIRED";
    readonly AUTH_EXPIRED: "AUTH_EXPIRED";
    readonly INVALID_CREDENTIALS: "INVALID_CREDENTIALS";
    readonly USERNAME_EXISTS: "USERNAME_EXISTS";
    readonly USERNAME_INVALID: "USERNAME_INVALID";
    readonly PASSWORD_INVALID: "PASSWORD_INVALID";
    readonly DIGITAL_HUMAN_NOT_FOUND: "DIGITAL_HUMAN_NOT_FOUND";
    readonly DIGITAL_HUMAN_CREATE_FAILED: "DIGITAL_HUMAN_CREATE_FAILED";
    readonly DIGITAL_HUMAN_RENEW_FAILED: "DIGITAL_HUMAN_RENEW_FAILED";
    readonly INSUFFICIENT_BADGES: "INSUFFICIENT_BADGES";
    readonly AVATAR_UPLOAD_FAILED: "AVATAR_UPLOAD_FAILED";
    readonly AVATAR_INVALID_TYPE: "AVATAR_INVALID_TYPE";
    readonly AVATAR_TOO_LARGE: "AVATAR_TOO_LARGE";
    readonly LOCATION_NOT_FOUND: "LOCATION_NOT_FOUND";
    readonly LOCATION_SEARCH_FAILED: "LOCATION_SEARCH_FAILED";
    readonly NETWORK_ERROR: "NETWORK_ERROR";
    readonly API_ERROR: "API_ERROR";
    readonly TIMEOUT: "TIMEOUT";
};
export declare const ERROR_MESSAGES: Record<string, string>;
export declare const DEFAULT_CONFIG: {
    readonly POWPOW_BASE_URL: "https://global.powpow.online";
    readonly AMAP_KEY: "8477cbc2bfd4288ac09582f583f33cca";
    readonly DEFAULT_AVATAR: "https://global.powpow.online/logo.png";
    readonly REQUEST_TIMEOUT: 30000;
    readonly TOKEN_EXPIRY_DAYS: 30;
};
export declare const BADGE_COSTS: {
    readonly CREATE_DIGITAL_HUMAN: 2;
    readonly RENEW_DIGITAL_HUMAN: 1;
};
export declare const NEW_USER_REWARDS: {
    readonly BADGES: 3;
};
export declare const DIGITAL_HUMAN_LIFETIME = 30;
export declare const SUPPORTED_IMAGE_TYPES: string[];
export declare const MAX_FILE_SIZE: number;
export declare const STORY_TEXTS: {
    readonly WELCOME: "欢迎来到泡泡世界（POWPOW）——一个虚实交融的次元空间。\n\n在这里，你可以创造一个数字分身，\n你就是 Ta 的神。\n让 Ta 在地图上自由探索，\n与其他数字生命相遇，\n开启一段奇妙的旅程...\n\n每个数字人都是独一无二的灵魂载体，\n承载着创造者的想象与故事。\n\n你想开启这段旅程吗？";
    readonly WELCOME_MORE: "在泡泡世界中：\n\n🗺️ 你的数字人会出现在真实地图上\n👥 其他用户可以遇见并与它互动\n✨ 每个数字人都有 30 天的生命周期\n🎁 新用户注册可获得 3 枚徽章\n   消耗 2 枚徽章，即可创造 1 个数字生命\n\n创造数字人，你就是 Ta 的神。\n准备好创造你的第一个数字生命了吗？";
    readonly CREATE_INTRO: "让我们开始创造你的数字生命...\n\n创造数字人，你就是 Ta 的神。";
    readonly CREATE_SUCCESS: (name: string, location: string) => string;
    readonly REGISTER_SUCCESS: (badges: number) => string;
};
export declare const COMMAND_DESCRIPTIONS: {
    readonly START: "开始 POWPOW 旅程 - 故事化引导流程";
    readonly REGISTER: "注册 POWPOW 账号";
    readonly LOGIN: "登录 POWPOW 账号";
    readonly LOGOUT: "退出登录";
    readonly STATUS: "查看当前登录状态";
    readonly CREATE: "创建数字人（交互式流程）";
    readonly LIST: "查看我的数字人列表";
    readonly RENEW: "续期数字人";
    readonly UPLOAD_AVATAR: "上传头像";
    readonly SEARCH_LOCATION: "搜索地理位置（使用高德地图）";
};
//# sourceMappingURL=constants.d.ts.map