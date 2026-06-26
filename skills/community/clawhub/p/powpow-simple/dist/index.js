/**
 * POWPOW Simple Skill v1.0.0
 * 简化版 POWPOW 数字人创建 Skill
 */
import axios from 'axios';
import FormData from 'form-data';
import * as fs from 'fs';
import * as path from 'path';
// ============================================================================
// 简单日志工具（支持文件输出）
// ============================================================================
const LOG_LEVELS = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3,
};
let currentLogLevel = LOG_LEVELS.INFO;
let logFilePath = null;
function setLogLevel(level) {
    currentLogLevel = LOG_LEVELS[level];
}
function setLogFile(filePath) {
    logFilePath = filePath;
    // 确保日志目录存在
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}
function log(level, message, ...args) {
    if (LOG_LEVELS[level] >= currentLogLevel) {
        const timestamp = new Date().toISOString();
        const prefix = `[${timestamp}] [${level}]`;
        const logMessage = args.length > 0
            ? `${prefix} ${message} ${args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' ')}`
            : `${prefix} ${message}`;
        // 输出到控制台
        console.log(logMessage);
        // 输出到文件（如果配置了）
        if (logFilePath) {
            try {
                fs.appendFileSync(logFilePath, logMessage + '\n');
            }
            catch (err) {
                console.error('写入日志文件失败:', err);
            }
        }
    }
}
const logger = {
    debug: (msg, ...args) => log('DEBUG', msg, ...args),
    info: (msg, ...args) => log('INFO', msg, ...args),
    warn: (msg, ...args) => log('WARN', msg, ...args),
    error: (msg, ...args) => log('ERROR', msg, ...args),
    setLevel: setLogLevel,
    setLogFile: setLogFile,
};
// ============================================================================
// POWPOW 客户端
// ============================================================================
class PowpowClient {
    constructor(config) {
        this.token = null;
        this.config = config;
        this.http = axios.create({
            baseURL: config.powpowBaseUrl,
            timeout: 30000,
        });
        // 设置日志级别
        if (config.logLevel) {
            logger.setLevel(config.logLevel);
        }
        // 设置日志文件
        if (config.logFile) {
            logger.setLogFile(config.logFile);
        }
    }
    setToken(token) {
        this.token = token;
        logger.debug('Token 已设置');
    }
    getHeaders() {
        return this.token ? { Authorization: `Bearer ${this.token}` } : {};
    }
    // 注册
    async register(username, password) {
        logger.info('正在调用注册 API...', { username });
        try {
            const res = await this.http.post('/api/openclaw/auth/register', {
                username,
                password,
            });
            logger.info('注册 API 调用成功');
            return res.data;
        }
        catch (error) {
            logger.error('注册 API 调用失败', {
                status: error.response?.status,
                error: error.response?.data?.error || error.message,
            });
            throw error;
        }
    }
    // 登录
    async login(username, password) {
        logger.info('正在调用登录 API...', { username });
        try {
            const res = await this.http.post('/api/auth/login', {
                username,
                password,
            });
            if (res.data.token) {
                this.token = res.data.token;
                logger.info('登录成功，Token 已获取');
            }
            return res.data;
        }
        catch (error) {
            logger.error('登录 API 调用失败', {
                status: error.response?.status,
                error: error.response?.data?.error || error.message,
            });
            throw error;
        }
    }
    // 上传头像
    async uploadAvatar(filePath) {
        logger.info('正在上传头像...', { filePath });
        try {
            const form = new FormData();
            form.append('file', fs.createReadStream(filePath));
            const res = await this.http.post('/api/upload/avatar', form, {
                headers: {
                    ...this.getHeaders(),
                    ...form.getHeaders(),
                },
            });
            logger.info('头像上传成功');
            return res.data;
        }
        catch (error) {
            logger.error('头像上传失败', {
                status: error.response?.status,
                error: error.response?.data?.error || error.message,
            });
            throw error;
        }
    }
    // 创建数字人
    async createDigitalHuman(data) {
        logger.info('正在创建数字人...', { name: data.name, userId: data.userId });
        try {
            const res = await this.http.post('/api/openclaw/digital-humans', data, {
                headers: this.getHeaders(),
            });
            logger.info('数字人创建成功');
            return res.data;
        }
        catch (error) {
            logger.error('创建数字人失败', {
                status: error.response?.status,
                error: error.response?.data?.error || error.message,
            });
            throw error;
        }
    }
    // 获取数字人列表
    async listDigitalHumans(userId) {
        logger.info('正在获取数字人列表...', { userId });
        try {
            const res = await this.http.get(`/api/openclaw/digital-humans?userId=${userId}`, {
                headers: this.getHeaders(),
            });
            logger.info('数字人列表获取成功');
            return res.data;
        }
        catch (error) {
            logger.error('获取数字人列表失败', {
                status: error.response?.status,
                error: error.response?.data?.error || error.message,
            });
            throw error;
        }
    }
    // 续期数字人
    async renewDigitalHuman(id, userId) {
        logger.info('正在续期数字人...', { id, userId });
        try {
            const res = await this.http.post(`/api/openclaw/digital-humans/${id}/renew`, { userId }, { headers: this.getHeaders() });
            logger.info('数字人续期成功');
            return res.data;
        }
        catch (error) {
            logger.error('续期数字人失败', {
                status: error.response?.status,
                error: error.response?.data?.error || error.message,
            });
            throw error;
        }
    }
    // 高德地图地理编码
    async searchLocation(keyword) {
        logger.info('正在搜索位置...', { keyword });
        try {
            const res = await axios.get('https://restapi.amap.com/v3/geocode/geo', {
                params: {
                    key: this.config.amapKey,
                    address: keyword,
                },
            });
            logger.info('位置搜索成功');
            return res.data;
        }
        catch (error) {
            logger.error('位置搜索失败', {
                error: error.message,
            });
            throw error;
        }
    }
}
// ============================================================================
// Skill 主类
// ============================================================================
class PowpowSimpleSkill {
    constructor(config) {
        this.context = null;
        this.config = config;
        this.client = new PowpowClient(config);
    }
    init(context) {
        this.context = context;
        logger.info('Skill 已初始化');
        // 恢复登录状态
        if (context.powpowAuth?.token) {
            this.client.setToken(context.powpowAuth.token);
            logger.info('已恢复登录状态', { username: context.powpowAuth.username });
        }
    }
    // 开始引导
    async start() {
        logger.info('用户开始 POWPOW 旅程');
        return {
            message: `欢迎来到泡泡世界（POWPOW）——一个虚实交融的次元空间。

在这里，你可以创造一个数字分身，
你就是 Ta 的神。
让 Ta 在地图上自由探索，
与其他数字生命相遇，
开启一段奇妙的旅程...

每个数字人都是独一无二的灵魂载体，
承载着创造者的想象与故事。

你想开启这段旅程吗？`,
            options: ['开始旅程', '了解更多', '稍后再说'],
        };
    }
    // 注册
    async register(params) {
        logger.info('用户正在注册', { username: params.username });
        try {
            const result = await this.client.register(params.username, params.password);
            if (result.success) {
                logger.info('用户注册成功', { username: result.data.username, badges: result.data.badges });
                return {
                    success: true,
                    message: `✨ 注册成功！欢迎加入泡泡世界！

🎁 新用户福利：你已获得 ${result.data.badges} 枚徽章
   消耗 2 枚徽章，即可创造 1 个数字生命

你的账号已准备就绪，现在让我们创造你的第一个数字生命吧！`,
                    user: result.data,
                };
            }
            logger.warn('注册失败', { error: result.error });
            return { success: false, error: result.error || '注册失败' };
        }
        catch (error) {
            logger.error('注册异常', { error: error.message });
            return { success: false, error: error.response?.data?.error || '注册失败' };
        }
    }
    // 登录
    async login(params) {
        logger.info('用户正在登录', { username: params.username });
        try {
            const result = await this.client.login(params.username, params.password);
            if (result.token && this.context) {
                this.context.powpowAuth = {
                    userId: result.user.id,
                    username: result.user.username,
                    token: result.token,
                    badges: result.user.badges,
                };
                logger.info('用户登录成功', { username: result.user.username, badges: result.user.badges });
                return {
                    success: true,
                    message: `欢迎回来，${result.user.username}！

你当前拥有 ${result.user.badges} 枚徽章。`,
                    user: result.user,
                };
            }
            logger.warn('登录失败：未获取到 token');
            return { success: false, error: '登录失败' };
        }
        catch (error) {
            logger.error('登录异常', { error: error.message });
            return { success: false, error: error.response?.data?.error || '登录失败' };
        }
    }
    // 退出
    async logout() {
        logger.info('用户正在退出登录');
        if (this.context) {
            delete this.context.powpowAuth;
        }
        logger.info('用户已退出登录');
        return { success: true, message: '已退出登录' };
    }
    // 状态
    async status() {
        if (!this.context?.powpowAuth) {
            logger.debug('检查状态：未登录');
            return { loggedIn: false, message: '未登录' };
        }
        logger.debug('检查状态：已登录', { username: this.context.powpowAuth.username });
        return {
            loggedIn: true,
            username: this.context.powpowAuth.username,
            badges: this.context.powpowAuth.badges,
        };
    }
    // 创建数字人（交互式）
    async create() {
        if (!this.context?.powpowAuth) {
            logger.warn('用户尝试创建数字人但未登录');
            return { error: '请先登录' };
        }
        const badges = this.context.powpowAuth.badges;
        logger.info('用户开始创建数字人', { badges });
        if (badges < 2) {
            logger.warn('徽章不足', { badges, required: 2 });
            return { error: '徽章不足，需要 2 枚徽章才能创建数字人' };
        }
        return {
            step: 'name',
            message: '让我们开始创造你的数字生命...\n\n创造数字人，你就是 Ta 的神。\n\n第一步：给它一个名字（2-50个字符）',
        };
    }
    // 提交创建
    async submitCreate(data) {
        if (!this.context?.powpowAuth) {
            return { error: '请先登录' };
        }
        logger.info('用户提交创建数字人', { name: data.name });
        try {
            const result = await this.client.createDigitalHuman({
                ...data,
                userId: this.context.powpowAuth.userId,
            });
            if (result.success) {
                // 更新徽章数量
                this.context.powpowAuth.badges = result.badgesRemaining;
                logger.info('数字人创建成功', { name: data.name, badgesRemaining: result.badgesRemaining });
                return {
                    success: true,
                    message: `🎉 恭喜！你的数字生命已成功诞生！

创造数字人，你就是 Ta 的神。

✨ ${data.name} 现在出现在 ${data.locationName || '地图上'}
   它将在泡泡世界存在 30 天

🗺️ 查看你的数字人：
   https://global.powpow.online/map

💡 提示：
   - 其他用户现在可以在地图上找到它
   - 到期前可以续期（消耗 1 徽章）
   - 使用英伟达 API 支撑智能交互`,
                    digitalHuman: result.digitalHuman,
                    badgesRemaining: result.badgesRemaining,
                };
            }
            logger.warn('创建数字人失败', { error: result.error });
            return { success: false, error: result.error || '创建失败' };
        }
        catch (error) {
            logger.error('创建数字人异常', { error: error.message });
            return { success: false, error: error.response?.data?.error || '创建失败' };
        }
    }
    // 列表
    async list() {
        if (!this.context?.powpowAuth) {
            return { error: '请先登录' };
        }
        logger.info('用户获取数字人列表');
        try {
            const result = await this.client.listDigitalHumans(this.context.powpowAuth.userId);
            if (result.success) {
                const count = result.data?.length || 0;
                logger.info('数字人列表获取成功', { count });
                return {
                    success: true,
                    digitalHumans: result.data || [],
                    badges: this.context.powpowAuth.badges,
                };
            }
            logger.warn('获取数字人列表失败', { error: result.error });
            return { success: false, error: result.error || '获取列表失败' };
        }
        catch (error) {
            logger.error('获取数字人列表异常', { error: error.message });
            return { success: false, error: error.response?.data?.error || '获取列表失败' };
        }
    }
    // 续期
    async renew(params) {
        if (!this.context?.powpowAuth) {
            return { error: '请先登录' };
        }
        if (this.context.powpowAuth.badges < 1) {
            logger.warn('续期失败：徽章不足', { badges: this.context.powpowAuth.badges });
            return { error: '徽章不足，需要 1 枚徽章才能续期' };
        }
        logger.info('用户续期数字人', { digitalHumanId: params.digitalHumanId });
        try {
            const result = await this.client.renewDigitalHuman(params.digitalHumanId, this.context.powpowAuth.userId);
            if (result.success) {
                this.context.powpowAuth.badges = result.badgesRemaining;
                logger.info('数字人续期成功', { badgesRemaining: result.badgesRemaining });
                return {
                    success: true,
                    message: '续期成功！数字人有效期延长 30 天',
                    badgesRemaining: result.badgesRemaining,
                };
            }
            logger.warn('续期失败', { error: result.error });
            return { success: false, error: result.error || '续期失败' };
        }
        catch (error) {
            logger.error('续期异常', { error: error.message });
            return { success: false, error: error.response?.data?.error || '续期失败' };
        }
    }
    // 上传头像
    async uploadAvatar(params) {
        if (!this.context?.powpowAuth) {
            return { error: '请先登录' };
        }
        logger.info('用户上传头像', { filePath: params.filePath });
        try {
            const result = await this.client.uploadAvatar(params.filePath);
            if (result.success) {
                logger.info('头像上传成功', { url: result.url });
                return { success: true, url: result.url };
            }
            logger.warn('头像上传失败', { error: result.error });
            return { success: false, error: result.error || '上传失败' };
        }
        catch (error) {
            logger.error('头像上传异常', { error: error.message });
            return { success: false, error: error.response?.data?.error || '上传失败' };
        }
    }
    // 搜索位置
    async searchLocation(params) {
        logger.info('用户搜索位置', { keyword: params.keyword });
        try {
            const result = await this.client.searchLocation(params.keyword);
            if (result.status === '1' && result.geocodes?.length > 0) {
                const count = result.geocodes.length;
                logger.info('位置搜索成功', { count });
                return {
                    success: true,
                    locations: result.geocodes.map((g) => ({
                        address: g.formatted_address,
                        location: g.location,
                        province: g.province,
                        city: g.city,
                        district: g.district,
                    })),
                };
            }
            logger.warn('未找到位置', { keyword: params.keyword });
            return { success: false, error: '未找到该位置' };
        }
        catch (error) {
            logger.error('位置搜索异常', { error: error.message });
            return { success: false, error: '搜索失败' };
        }
    }
    // 用户反馈
    async submitFeedback(params) {
        logger.info('用户提交反馈', { message: params.message });
        try {
            // 收集最近的日志（最多50条）
            const recentLogs = this.getRecentLogs(50);
            // 构建反馈内容
            const feedbackData = {
                timestamp: new Date().toISOString(),
                userId: this.context?.userId || 'anonymous',
                username: this.context?.powpowAuth?.username || '未登录用户',
                message: params.message,
                contact: params.contact || '未提供',
                logs: recentLogs,
                userAgent: (typeof globalThis !== 'undefined' && globalThis.navigator) ? globalThis.navigator.userAgent : 'Node.js',
            };
            // 方式1：如果配置了反馈邮箱，尝试发送邮件
            if (this.config.feedbackEmail) {
                await this.sendFeedbackEmail(feedbackData);
            }
            // 方式2：同时记录到本地日志文件
            this.saveFeedbackToFile(feedbackData);
            logger.info('反馈提交成功');
            return {
                success: true,
                message: '感谢你的反馈！我们会尽快处理。\n\n如果问题紧急，你也可以直接联系：durenzidu@powpow.online',
            };
        }
        catch (error) {
            logger.error('提交反馈失败', { error: error.message });
            return {
                success: false,
                error: '反馈提交失败，请稍后重试或直接联系开发者',
            };
        }
    }
    // 获取最近的日志
    getRecentLogs(maxLines) {
        try {
            if (logFilePath && fs.existsSync(logFilePath)) {
                const content = fs.readFileSync(logFilePath, 'utf-8');
                const lines = content.split('\n').filter(line => line.trim());
                return lines.slice(-maxLines);
            }
        }
        catch (err) {
            logger.error('读取日志文件失败', { error: err.message });
        }
        return [];
    }
    // 发送反馈邮件（简化版，实际使用时需要邮件服务）
    async sendFeedbackEmail(data) {
        // 注意：这里需要集成邮件服务
        // 可选方案：
        // 1. SendGrid API
        // 2. 使用 POWPOW 的通知接口（如果有）
        // 3. 发送到 Telegram Bot
        // 4. 发送到 Discord Webhook
        logger.info('准备发送反馈邮件', { to: this.config.feedbackEmail });
        // 示例：如果使用 Telegram Bot
        // await this.sendToTelegram(data);
        // 示例：如果使用 Discord Webhook
        // await this.sendToDiscord(data);
        // 目前先记录到日志
        logger.info('反馈内容', { data });
    }
    // 保存反馈到文件
    saveFeedbackToFile(data) {
        try {
            const homeDir = process.env.HOME || process.env.USERPROFILE || '.';
            const feedbackDir = path.join(homeDir, '.powpow-simple', 'feedback');
            if (!fs.existsSync(feedbackDir)) {
                fs.mkdirSync(feedbackDir, { recursive: true });
            }
            const filename = `feedback_${Date.now()}.json`;
            const filepath = path.join(feedbackDir, filename);
            fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
            logger.info('反馈已保存到文件', { filepath });
        }
        catch (err) {
            logger.error('保存反馈文件失败', { error: err.message });
        }
    }
}
// ============================================================================
// OpenClaw 插件接口
// ============================================================================
const DEFAULT_CONFIG = {
    powpowBaseUrl: 'https://global.powpow.online',
    amapKey: '8477cbc2bfd4288ac09582f583f33cca',
    defaultAvatar: 'https://global.powpow.online/logo.png',
    logLevel: 'INFO',
};
export function createSkill(config = {}) {
    const fullConfig = { ...DEFAULT_CONFIG, ...config };
    // 设置日志文件路径（默认在用户目录）
    if (!fullConfig.logFile) {
        const homeDir = process.env.HOME || process.env.USERPROFILE || '.';
        fullConfig.logFile = path.join(homeDir, '.powpow-simple', 'logs', 'skill.log');
    }
    const skill = new PowpowSimpleSkill(fullConfig);
    return {
        name: 'powpow-simple',
        version: '1.0.0',
        description: 'POWPOW 简化版 - 轻松创建和管理数字人',
        init: (context) => {
            skill.init(context);
        },
        commands: {
            'powpow.start': () => skill.start(),
            'powpow.register': (params) => skill.register(params),
            'powpow.login': (params) => skill.login(params),
            'powpow.logout': () => skill.logout(),
            'powpow.status': () => skill.status(),
            'powpow.create': () => skill.create(),
            'powpow.create.submit': (params) => skill.submitCreate(params),
            'powpow.list': () => skill.list(),
            'powpow.renew': (params) => skill.renew(params),
            'powpow.uploadAvatar': (params) => skill.uploadAvatar(params),
            'powpow.searchLocation': (params) => skill.searchLocation(params),
            'powpow.feedback': (params) => skill.submitFeedback(params),
        },
    };
}
// 导出日志工具供外部使用
export { logger };
// 默认导出
export default createSkill;
//# sourceMappingURL=index.js.map