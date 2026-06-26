/**
 * POWPOW Simple Skill - 常量定义
 */
// API 端点
export const API_ENDPOINTS = {
    // POWPOW API
    REGISTER: '/api/openclaw/auth/register',
    LOGIN: '/api/auth/login',
    UPLOAD_AVATAR: '/api/upload/avatar',
    CREATE_DIGITAL_HUMAN: '/api/openclaw/digital-humans',
    LIST_DIGITAL_HUMANS: '/api/openclaw/digital-humans',
    RENEW_DIGITAL_HUMAN: (id) => `/api/openclaw/digital-humans/${id}/renew`,
    // 高德地图 API
    AMAP_GEOCODE: 'https://restapi.amap.com/v3/geocode/geo',
};
// 验证规则
export const VALIDATION = {
    USERNAME: {
        MIN_LENGTH: 2,
        MAX_LENGTH: 50,
        PATTERN: /^[a-zA-Z0-9_\u4e00-\u9fa5]+$/, // 支持中文、英文、数字、下划线
    },
    PASSWORD: {
        MIN_LENGTH: 6,
        MAX_LENGTH: 100,
    },
    DIGITAL_HUMAN: {
        NAME_MIN_LENGTH: 2,
        NAME_MAX_LENGTH: 50,
        DESCRIPTION_MAX_LENGTH: 500,
    },
};
// 错误码
export const ERROR_CODES = {
    // 认证错误
    AUTH_REQUIRED: 'AUTH_REQUIRED',
    AUTH_EXPIRED: 'AUTH_EXPIRED',
    INVALID_CREDENTIALS: 'INVALID_CREDENTIALS',
    USERNAME_EXISTS: 'USERNAME_EXISTS',
    USERNAME_INVALID: 'USERNAME_INVALID',
    PASSWORD_INVALID: 'PASSWORD_INVALID',
    // 数字人错误
    DIGITAL_HUMAN_NOT_FOUND: 'DIGITAL_HUMAN_NOT_FOUND',
    DIGITAL_HUMAN_CREATE_FAILED: 'DIGITAL_HUMAN_CREATE_FAILED',
    DIGITAL_HUMAN_RENEW_FAILED: 'DIGITAL_HUMAN_RENEW_FAILED',
    INSUFFICIENT_BADGES: 'INSUFFICIENT_BADGES',
    // 头像错误
    AVATAR_UPLOAD_FAILED: 'AVATAR_UPLOAD_FAILED',
    AVATAR_INVALID_TYPE: 'AVATAR_INVALID_TYPE',
    AVATAR_TOO_LARGE: 'AVATAR_TOO_LARGE',
    // 位置错误
    LOCATION_NOT_FOUND: 'LOCATION_NOT_FOUND',
    LOCATION_SEARCH_FAILED: 'LOCATION_SEARCH_FAILED',
    // 网络错误
    NETWORK_ERROR: 'NETWORK_ERROR',
    API_ERROR: 'API_ERROR',
    TIMEOUT: 'TIMEOUT',
};
// 错误消息
export const ERROR_MESSAGES = {
    [ERROR_CODES.AUTH_REQUIRED]: '请先登录 POWPOW 账号',
    [ERROR_CODES.AUTH_EXPIRED]: '登录已过期，请重新登录',
    [ERROR_CODES.INVALID_CREDENTIALS]: '用户名或密码错误',
    [ERROR_CODES.USERNAME_EXISTS]: '用户名已存在',
    [ERROR_CODES.USERNAME_INVALID]: '用户名格式不正确（2-50个字符，支持中文、英文、数字、下划线）',
    [ERROR_CODES.PASSWORD_INVALID]: '密码长度至少6位',
    [ERROR_CODES.DIGITAL_HUMAN_NOT_FOUND]: '找不到该数字人',
    [ERROR_CODES.DIGITAL_HUMAN_CREATE_FAILED]: '创建数字人失败',
    [ERROR_CODES.DIGITAL_HUMAN_RENEW_FAILED]: '续期数字人失败',
    [ERROR_CODES.INSUFFICIENT_BADGES]: '徽章不足，需要更多徽章才能执行此操作',
    [ERROR_CODES.AVATAR_UPLOAD_FAILED]: '头像上传失败',
    [ERROR_CODES.AVATAR_INVALID_TYPE]: '头像格式不正确（仅支持 JPG、PNG、GIF、WebP）',
    [ERROR_CODES.AVATAR_TOO_LARGE]: '头像文件过大（最大5MB）',
    [ERROR_CODES.LOCATION_NOT_FOUND]: '找不到该位置',
    [ERROR_CODES.LOCATION_SEARCH_FAILED]: '位置搜索失败',
    [ERROR_CODES.NETWORK_ERROR]: '网络连接失败',
    [ERROR_CODES.API_ERROR]: 'API 调用失败',
    [ERROR_CODES.TIMEOUT]: '请求超时',
};
// 默认配置
export const DEFAULT_CONFIG = {
    POWPOW_BASE_URL: 'https://global.powpow.online',
    AMAP_KEY: '8477cbc2bfd4288ac09582f583f33cca',
    DEFAULT_AVATAR: 'https://global.powpow.online/logo.png',
    REQUEST_TIMEOUT: 30000, // 30秒
    TOKEN_EXPIRY_DAYS: 30,
};
// 徽章消耗
export const BADGE_COSTS = {
    CREATE_DIGITAL_HUMAN: 2,
    RENEW_DIGITAL_HUMAN: 1,
};
// 新用户奖励
export const NEW_USER_REWARDS = {
    BADGES: 3,
};
// 数字人有效期（天）
export const DIGITAL_HUMAN_LIFETIME = 30;
// 支持的图片格式
export const SUPPORTED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
];
// 最大文件大小（5MB）
export const MAX_FILE_SIZE = 5 * 1024 * 1024;
// 故事化文案
export const STORY_TEXTS = {
    WELCOME: `欢迎来到泡泡世界（POWPOW）——一个虚实交融的次元空间。

在这里，你可以创造一个数字分身，
你就是 Ta 的神。
让 Ta 在地图上自由探索，
与其他数字生命相遇，
开启一段奇妙的旅程...

每个数字人都是独一无二的灵魂载体，
承载着创造者的想象与故事。

你想开启这段旅程吗？`,
    WELCOME_MORE: `在泡泡世界中：

🗺️ 你的数字人会出现在真实地图上
👥 其他用户可以遇见并与它互动
✨ 每个数字人都有 30 天的生命周期
🎁 新用户注册可获得 3 枚徽章
   消耗 2 枚徽章，即可创造 1 个数字生命

创造数字人，你就是 Ta 的神。
准备好创造你的第一个数字生命了吗？`,
    CREATE_INTRO: `让我们开始创造你的数字生命...

创造数字人，你就是 Ta 的神。`,
    CREATE_SUCCESS: (name, location) => `🎉 恭喜！你的数字生命已成功诞生！

创造数字人，你就是 Ta 的神。

✨ ${name} 现在出现在 ${location}
   它将在泡泡世界存在 30 天

💡 提示：
   - 其他用户现在可以在地图上找到它
   - 到期前可以续期（消耗 1 徽章）
   - 使用英伟达 API 支撑智能交互`,
    REGISTER_SUCCESS: (badges) => `✨ 注册成功！欢迎加入泡泡世界！

🎁 新用户福利：你已获得 ${badges} 枚徽章
   消耗 2 枚徽章，即可创造 1 个数字生命

你的账号已准备就绪，现在让我们创造你的第一个数字生命吧！`,
};
// 命令描述
export const COMMAND_DESCRIPTIONS = {
    START: '开始 POWPOW 旅程 - 故事化引导流程',
    REGISTER: '注册 POWPOW 账号',
    LOGIN: '登录 POWPOW 账号',
    LOGOUT: '退出登录',
    STATUS: '查看当前登录状态',
    CREATE: '创建数字人（交互式流程）',
    LIST: '查看我的数字人列表',
    RENEW: '续期数字人',
    UPLOAD_AVATAR: '上传头像',
    SEARCH_LOCATION: '搜索地理位置（使用高德地图）',
};
//# sourceMappingURL=constants.js.map