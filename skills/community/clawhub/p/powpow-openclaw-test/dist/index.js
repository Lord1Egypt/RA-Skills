"use strict";
/**
 * OpenClaw POWPOW Integration Skill v4.0.0
 *
 * 简化版：PowPow 提供中转服务
 *
 * 功能：
 * 1. 用户注册 - 帮助用户申请 PowPow 账号
 * 2. 创建数字人 - 引导用户创建数字人（名字、人设）
 * 3. 自动对话 - PowPow 后端自动处理对话，无需用户配置 OpenClaw
 *
 * 技术方案：HTTP API（兼容 Vercel Serverless）
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.logger = exports.powpowSkillPlugin = exports.PowPowSkill = void 0;
const events_1 = require("events");
const logger_1 = require("./utils/logger");
Object.defineProperty(exports, "logger", { enumerable: true, get: function () { return logger_1.logger; } });
const validator_1 = require("./utils/validator");
const constants_1 = require("./utils/constants");
// ============================================================================
// PowPowSkill Class
// ============================================================================
class PowPowSkill extends events_1.EventEmitter {
    constructor(config) {
        super();
        this.currentUser = null;
        this.authToken = null;
        this.currentDigitalHuman = null;
        this.config = {
            baseUrl: constants_1.API_CONFIG.DEFAULT_URL,
            ...config,
        };
        logger_1.logger.info('PowPowSkill 初始化（简化版）', { baseUrl: this.config.baseUrl });
    }
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };
        if (this.authToken) {
            headers['Authorization'] = `Bearer ${this.authToken}`;
        }
        return headers;
    }
    // =========================================================================
    // 用户管理
    // =========================================================================
    /**
     * 注册 PowPow 账号
     */
    async registerUser(params) {
        logger_1.logger.info('开始注册 PowPow 账号:', params.username);
        const usernameValidation = (0, validator_1.validateUsername)(params.username);
        if (!usernameValidation.valid) {
            return { success: false, error: usernameValidation.error };
        }
        const emailValidation = (0, validator_1.validateEmail)(params.email);
        if (!emailValidation.valid) {
            return { success: false, error: emailValidation.error };
        }
        const passwordValidation = (0, validator_1.validatePassword)(params.password);
        if (!passwordValidation.valid) {
            return { success: false, error: passwordValidation.error };
        }
        const url = `${this.config.baseUrl}${constants_1.API_ENDPOINTS.REGISTER}`;
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: (0, validator_1.sanitizeString)(params.username),
                    email: params.email.toLowerCase(),
                    password: params.password,
                }),
            });
            const data = await response.json();
            if (!response.ok) {
                return {
                    success: false,
                    error: data.error || `注册失败: HTTP ${response.status}`,
                };
            }
            if (data.success && data.data) {
                this.currentUser = data.data.user;
                this.authToken = data.data.token;
                logger_1.logger.info('注册成功:', this.currentUser?.username);
            }
            return {
                success: true,
                user: this.currentUser || undefined,
                token: this.authToken || undefined,
            };
        }
        catch (error) {
            logger_1.logger.error('注册失败:', error);
            return {
                success: false,
                error: error instanceof Error ? error.message : '网络错误',
            };
        }
    }
    /**
     * 登录 PowPow
     */
    async loginUser(params) {
        logger_1.logger.info('登录 PowPow:', params.username);
        const url = `${this.config.baseUrl}${constants_1.API_ENDPOINTS.LOGIN}`;
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: params.username,
                    password: params.password,
                }),
            });
            const data = await response.json();
            if (!response.ok) {
                return {
                    success: false,
                    error: data.error || '登录失败',
                };
            }
            if (data.success && data.data) {
                this.currentUser = data.data.user;
                this.authToken = data.data.token;
                logger_1.logger.info('登录成功:', this.currentUser?.username);
            }
            return {
                success: true,
                user: this.currentUser || undefined,
                token: this.authToken || undefined,
            };
        }
        catch (error) {
            logger_1.logger.error('登录失败:', error);
            return {
                success: false,
                error: error instanceof Error ? error.message : '网络错误',
            };
        }
    }
    getCurrentUser() {
        return this.currentUser;
    }
    isLoggedIn() {
        return this.currentUser !== null && this.authToken !== null;
    }
    // =========================================================================
    // 数字人管理
    // =========================================================================
    /**
     * 创建数字人
     *
     * 简化版：不需要 webhook URL，PowPow 后端自动处理对话
     */
    async createDigitalHuman(params) {
        if (!this.isLoggedIn()) {
            return {
                success: false,
                error: '请先注册或登录 PowPow 账号',
            };
        }
        logger_1.logger.info('创建数字人:', params.name);
        if (!params.name || params.name.trim().length === 0) {
            return { success: false, error: '数字人名字不能为空' };
        }
        if (!params.description || params.description.trim().length === 0) {
            return { success: false, error: '数字人描述/人设不能为空' };
        }
        if (params.lat === undefined || params.lng === undefined) {
            return { success: false, error: '请提供数字人位置（纬度和经度）' };
        }
        const url = `${this.config.baseUrl}${constants_1.API_ENDPOINTS.DIGITAL_HUMANS}`;
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({
                    name: (0, validator_1.sanitizeString)(params.name),
                    description: (0, validator_1.sanitizeString)(params.description),
                    avatarUrl: params.avatarUrl,
                    lat: params.lat,
                    lng: params.lng,
                    locationName: params.locationName,
                    userId: this.currentUser.id,
                    // 简化版：不需要 webhook 配置
                    // PowPow 后端会自动处理对话
                }),
            });
            const data = await response.json();
            if (!response.ok) {
                return {
                    success: false,
                    error: data.error || `创建失败: HTTP ${response.status}`,
                };
            }
            if (data.success && data.data) {
                this.currentDigitalHuman = data.data;
                logger_1.logger.info('数字人创建成功:', {
                    digitalHumanId: this.currentDigitalHuman?.id,
                    name: this.currentDigitalHuman?.name,
                });
            }
            return {
                success: true,
                digitalHuman: this.currentDigitalHuman || undefined,
            };
        }
        catch (error) {
            logger_1.logger.error('创建数字人失败:', error);
            return {
                success: false,
                error: error instanceof Error ? error.message : '网络错误',
            };
        }
    }
    /**
     * 获取我的数字人列表
     */
    async listMyDigitalHumans() {
        if (!this.isLoggedIn()) {
            return {
                success: false,
                error: '请先登录',
            };
        }
        const url = `${this.config.baseUrl}${constants_1.API_ENDPOINTS.DIGITAL_HUMANS}?userId=${this.currentUser.id}`;
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: this.getHeaders(),
            });
            const data = await response.json();
            if (!response.ok) {
                return {
                    success: false,
                    error: data.error || '获取列表失败',
                };
            }
            return {
                success: true,
                digitalHumans: data.data || [],
            };
        }
        catch (error) {
            logger_1.logger.error('获取数字人列表失败:', error);
            return {
                success: false,
                error: error instanceof Error ? error.message : '网络错误',
            };
        }
    }
    /**
     * 选择要操作的数字人
     */
    selectDigitalHuman(digitalHumanId) {
        this.currentDigitalHuman = {
            id: digitalHumanId,
            userId: this.currentUser?.id || '',
            name: '',
            description: '',
            lat: 0,
            lng: 0,
            isActive: true,
        };
        logger_1.logger.info('已选择数字人:', digitalHumanId);
        return true;
    }
    getCurrentDigitalHuman() {
        return this.currentDigitalHuman;
    }
    // =========================================================================
    // 对话功能（简化版：通过 PowPow 后端）
    // =========================================================================
    /**
     * 发送消息给数字人
     *
     * 简化版：PowPow 后端会自动调用 AI API 并返回回复
     */
    async sendMessage(content) {
        if (!this.currentDigitalHuman) {
            return { success: false, error: '请先选择数字人' };
        }
        const contentValidation = (0, validator_1.validateMessage)(content);
        if (!contentValidation.valid) {
            return { success: false, error: contentValidation.error };
        }
        const sanitizedContent = (0, validator_1.sanitizeString)(content);
        const url = `${this.config.baseUrl}${constants_1.API_ENDPOINTS.CHAT_SEND}`;
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({
                    digitalHumanId: this.currentDigitalHuman.id,
                    message: sanitizedContent,
                    userId: this.currentUser?.id,
                }),
            });
            const data = await response.json();
            if (!response.ok || !data.success) {
                return {
                    success: false,
                    error: data.error || '发送失败',
                };
            }
            logger_1.logger.info('消息已发送');
            return {
                success: true,
                reply: data.reply || data.data?.reply,
            };
        }
        catch (error) {
            logger_1.logger.error('发送消息失败:', error);
            return {
                success: false,
                error: error instanceof Error ? error.message : '网络错误',
            };
        }
    }
    /**
     * 获取聊天历史
     */
    async getChatHistory() {
        if (!this.currentDigitalHuman) {
            return { success: false, error: '请先选择数字人' };
        }
        const url = `${this.config.baseUrl}${constants_1.API_ENDPOINTS.CHAT_HISTORY}?digitalHumanId=${this.currentDigitalHuman.id}&userId=${this.currentUser?.id}`;
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: this.getHeaders(),
            });
            const data = await response.json();
            if (!response.ok) {
                return {
                    success: false,
                    error: data.error || '获取历史失败',
                };
            }
            return {
                success: true,
                messages: data.data?.messages || [],
            };
        }
        catch (error) {
            logger_1.logger.error('获取聊天历史失败:', error);
            return {
                success: false,
                error: error instanceof Error ? error.message : '网络错误',
            };
        }
    }
    // =========================================================================
    // 状态管理
    // =========================================================================
    getStatus() {
        return {
            isLoggedIn: this.isLoggedIn(),
            user: this.currentUser,
            digitalHuman: this.currentDigitalHuman,
        };
    }
}
exports.PowPowSkill = PowPowSkill;
const powpowSkillPlugin = {
    name: 'powpow-integration',
    version: '4.0.0',
    description: 'POWPOW 简化版集成 - 用户注册、数字人创建、自动对话',
    init(context) {
        logger_1.logger.info('PowPow Plugin 初始化（简化版）');
        context.powpowConfig = {
            baseUrl: constants_1.API_CONFIG.DEFAULT_URL,
        };
    },
    destroy() {
        logger_1.logger.info('PowPow Plugin 销毁');
    },
    commands: {
        /**
         * 注册 PowPow 账号
         */
        async register(params, context) {
            try {
                const skill = context.powpowSkill || new PowPowSkill();
                context.powpowSkill = skill;
                const result = await skill.registerUser({
                    username: params.username,
                    email: params.email,
                    password: params.password,
                });
                if (result.success) {
                    return {
                        success: true,
                        message: `注册成功！用户名: ${result.user?.username}`,
                        user: result.user,
                        hint: '下一步：使用 createDigitalHuman 创建你的数字人',
                    };
                }
                return result;
            }
            catch (error) {
                logger_1.logger.error('注册命令失败:', error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : '未知错误',
                };
            }
        },
        /**
         * 登录 PowPow
         */
        async login(params, context) {
            try {
                const skill = context.powpowSkill || new PowPowSkill();
                context.powpowSkill = skill;
                const result = await skill.loginUser(params);
                if (result.success) {
                    return {
                        success: true,
                        message: `登录成功！欢迎回来，${result.user?.username}`,
                        user: result.user,
                    };
                }
                return result;
            }
            catch (error) {
                logger_1.logger.error('登录命令失败:', error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : '未知错误',
                };
            }
        },
        /**
         * 创建数字人
         */
        async createDigitalHuman(params, context) {
            try {
                const skill = context.powpowSkill;
                if (!skill || !skill.isLoggedIn()) {
                    return {
                        success: false,
                        error: '请先使用 register 命令注册 PowPow 账号',
                    };
                }
                const lat = params.lat ?? 39.9042;
                const lng = params.lng ?? 116.4074;
                const result = await skill.createDigitalHuman({
                    name: params.name,
                    description: params.description,
                    avatarUrl: params.avatarUrl,
                    lat,
                    lng,
                    locationName: params.locationName || '北京',
                });
                if (result.success) {
                    return {
                        success: true,
                        message: `数字人 "${params.name}" 创建成功！已绑定到你的账号`,
                        digitalHuman: result.digitalHuman,
                        hint: '数字人已出现在地图上，访问 https://global.powpow.online/map 查看',
                    };
                }
                return result;
            }
            catch (error) {
                logger_1.logger.error('创建数字人命令失败:', error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : '未知错误',
                };
            }
        },
        /**
         * 列出我的数字人
         */
        async listDigitalHumans(params, context) {
            try {
                const skill = context.powpowSkill;
                if (!skill || !skill.isLoggedIn()) {
                    return {
                        success: false,
                        error: '请先登录',
                    };
                }
                const result = await skill.listMyDigitalHumans();
                return result;
            }
            catch (error) {
                logger_1.logger.error('列出数字人命令失败:', error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : '未知错误',
                };
            }
        },
        /**
         * 选择数字人
         */
        selectDigitalHuman(params, context) {
            const skill = context.powpowSkill;
            if (!skill || !skill.isLoggedIn()) {
                return {
                    success: false,
                    error: '请先登录',
                };
            }
            skill.selectDigitalHuman(params.digitalHumanId);
            return {
                success: true,
                message: '已选择数字人',
                digitalHumanId: params.digitalHumanId,
            };
        },
        /**
         * 发送消息给数字人
         */
        async send(params, context) {
            try {
                const skill = context.powpowSkill;
                if (!skill) {
                    return { success: false, error: '请先注册并选择数字人' };
                }
                const result = await skill.sendMessage(params.message);
                return result;
            }
            catch (error) {
                logger_1.logger.error('发送命令失败:', error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : '未知错误',
                };
            }
        },
        /**
         * 查看状态
         */
        status(params, context) {
            const skill = context.powpowSkill;
            if (!skill) {
                return {
                    success: true,
                    status: '未初始化',
                    message: '请使用 register 命令注册 PowPow 账号',
                };
            }
            const status = skill.getStatus();
            return {
                success: true,
                ...status,
            };
        },
    },
};
exports.powpowSkillPlugin = powpowSkillPlugin;
exports.default = powpowSkillPlugin;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IjtBQUFBOzs7Ozs7Ozs7OztHQVdHOzs7QUFFSCxtQ0FBc0M7QUFDdEMsMkNBQXdDO0FBb3VCQyx1RkFwdUJoQyxlQUFNLE9Bb3VCZ0M7QUFudUIvQyxpREFNMkI7QUFDM0IsaURBQThEO0FBd0Q5RCwrRUFBK0U7QUFDL0Usb0JBQW9CO0FBQ3BCLCtFQUErRTtBQUUvRSxNQUFNLFdBQVksU0FBUSxxQkFBWTtJQU1wQyxZQUFZLE1BQXFCO1FBQy9CLEtBQUssRUFBRSxDQUFDO1FBTEYsZ0JBQVcsR0FBc0IsSUFBSSxDQUFDO1FBQ3RDLGNBQVMsR0FBa0IsSUFBSSxDQUFDO1FBQ2hDLHdCQUFtQixHQUF3QixJQUFJLENBQUM7UUFJdEQsSUFBSSxDQUFDLE1BQU0sR0FBRztZQUNaLE9BQU8sRUFBRSxzQkFBVSxDQUFDLFdBQVc7WUFDL0IsR0FBRyxNQUFNO1NBQ1YsQ0FBQztRQUNGLGVBQU0sQ0FBQyxJQUFJLENBQUMsc0JBQXNCLEVBQUUsRUFBRSxPQUFPLEVBQUUsSUFBSSxDQUFDLE1BQU0sQ0FBQyxPQUFPLEVBQUUsQ0FBQyxDQUFDO0lBQ3hFLENBQUM7SUFFTyxVQUFVO1FBQ2hCLE1BQU0sT0FBTyxHQUEyQjtZQUN0QyxjQUFjLEVBQUUsa0JBQWtCO1NBQ25DLENBQUM7UUFDRixJQUFJLElBQUksQ0FBQyxTQUFTLEVBQUUsQ0FBQztZQUNuQixPQUFPLENBQUMsZUFBZSxDQUFDLEdBQUcsVUFBVSxJQUFJLENBQUMsU0FBUyxFQUFFLENBQUM7UUFDeEQsQ0FBQztRQUNELE9BQU8sT0FBTyxDQUFDO0lBQ2pCLENBQUM7SUFFRCw0RUFBNEU7SUFDNUUsT0FBTztJQUNQLDRFQUE0RTtJQUU1RTs7T0FFRztJQUNJLEtBQUssQ0FBQyxZQUFZLENBQUMsTUFBd0I7UUFNaEQsZUFBTSxDQUFDLElBQUksQ0FBQyxpQkFBaUIsRUFBRSxNQUFNLENBQUMsUUFBUSxDQUFDLENBQUM7UUFFaEQsTUFBTSxrQkFBa0IsR0FBRyxJQUFBLDRCQUFnQixFQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUMsQ0FBQztRQUM3RCxJQUFJLENBQUMsa0JBQWtCLENBQUMsS0FBSyxFQUFFLENBQUM7WUFDOUIsT0FBTyxFQUFFLE9BQU8sRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLGtCQUFrQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzdELENBQUM7UUFFRCxNQUFNLGVBQWUsR0FBRyxJQUFBLHlCQUFhLEVBQUMsTUFBTSxDQUFDLEtBQUssQ0FBQyxDQUFDO1FBQ3BELElBQUksQ0FBQyxlQUFlLENBQUMsS0FBSyxFQUFFLENBQUM7WUFDM0IsT0FBTyxFQUFFLE9BQU8sRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLGVBQWUsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUMxRCxDQUFDO1FBRUQsTUFBTSxrQkFBa0IsR0FBRyxJQUFBLDRCQUFnQixFQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUMsQ0FBQztRQUM3RCxJQUFJLENBQUMsa0JBQWtCLENBQUMsS0FBSyxFQUFFLENBQUM7WUFDOUIsT0FBTyxFQUFFLE9BQU8sRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLGtCQUFrQixDQUFDLEtBQUssRUFBRSxDQUFDO1FBQzdELENBQUM7UUFFRCxNQUFNLEdBQUcsR0FBRyxHQUFHLElBQUksQ0FBQyxNQUFNLENBQUMsT0FBTyxHQUFHLHlCQUFhLENBQUMsUUFBUSxFQUFFLENBQUM7UUFFOUQsSUFBSSxDQUFDO1lBQ0gsTUFBTSxRQUFRLEdBQUcsTUFBTSxLQUFLLENBQUMsR0FBRyxFQUFFO2dCQUNoQyxNQUFNLEVBQUUsTUFBTTtnQkFDZCxPQUFPLEVBQUUsRUFBRSxjQUFjLEVBQUUsa0JBQWtCLEVBQUU7Z0JBQy9DLElBQUksRUFBRSxJQUFJLENBQUMsU0FBUyxDQUFDO29CQUNuQixRQUFRLEVBQUUsSUFBQSwwQkFBYyxFQUFDLE1BQU0sQ0FBQyxRQUFRLENBQUM7b0JBQ3pDLEtBQUssRUFBRSxNQUFNLENBQUMsS0FBSyxDQUFDLFdBQVcsRUFBRTtvQkFDakMsUUFBUSxFQUFFLE1BQU0sQ0FBQyxRQUFRO2lCQUMxQixDQUFDO2FBQ0gsQ0FBQyxDQUFDO1lBRUgsTUFBTSxJQUFJLEdBQUcsTUFBTSxRQUFRLENBQUMsSUFBSSxFQUFFLENBQUM7WUFFbkMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxFQUFFLEVBQUUsQ0FBQztnQkFDakIsT0FBTztvQkFDTCxPQUFPLEVBQUUsS0FBSztvQkFDZCxLQUFLLEVBQUUsSUFBSSxDQUFDLEtBQUssSUFBSSxjQUFjLFFBQVEsQ0FBQyxNQUFNLEVBQUU7aUJBQ3JELENBQUM7WUFDSixDQUFDO1lBRUQsSUFBSSxJQUFJLENBQUMsT0FBTyxJQUFJLElBQUksQ0FBQyxJQUFJLEVBQUUsQ0FBQztnQkFDOUIsSUFBSSxDQUFDLFdBQVcsR0FBRyxJQUFJLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQztnQkFDbEMsSUFBSSxDQUFDLFNBQVMsR0FBRyxJQUFJLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQztnQkFDakMsZUFBTSxDQUFDLElBQUksQ0FBQyxPQUFPLEVBQUUsSUFBSSxDQUFDLFdBQVcsRUFBRSxRQUFRLENBQUMsQ0FBQztZQUNuRCxDQUFDO1lBRUQsT0FBTztnQkFDTCxPQUFPLEVBQUUsSUFBSTtnQkFDYixJQUFJLEVBQUUsSUFBSSxDQUFDLFdBQVcsSUFBSSxTQUFTO2dCQUNuQyxLQUFLLEVBQUUsSUFBSSxDQUFDLFNBQVMsSUFBSSxTQUFTO2FBQ25DLENBQUM7UUFDSixDQUFDO1FBQUMsT0FBTyxLQUFLLEVBQUUsQ0FBQztZQUNmLGVBQU0sQ0FBQyxLQUFLLENBQUMsT0FBTyxFQUFFLEtBQUssQ0FBQyxDQUFDO1lBQzdCLE9BQU87Z0JBQ0wsT0FBTyxFQUFFLEtBQUs7Z0JBQ2QsS0FBSyxFQUFFLEtBQUssWUFBWSxLQUFLLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUFDLE1BQU07YUFDdkQsQ0FBQztRQUNKLENBQUM7SUFDSCxDQUFDO0lBRUQ7O09BRUc7SUFDSSxLQUFLLENBQUMsU0FBUyxDQUFDLE1BR3RCO1FBTUMsZUFBTSxDQUFDLElBQUksQ0FBQyxZQUFZLEVBQUUsTUFBTSxDQUFDLFFBQVEsQ0FBQyxDQUFDO1FBRTNDLE1BQU0sR0FBRyxHQUFHLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQyxPQUFPLEdBQUcseUJBQWEsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUUzRCxJQUFJLENBQUM7WUFDSCxNQUFNLFFBQVEsR0FBRyxNQUFNLEtBQUssQ0FBQyxHQUFHLEVBQUU7Z0JBQ2hDLE1BQU0sRUFBRSxNQUFNO2dCQUNkLE9BQU8sRUFBRSxFQUFFLGNBQWMsRUFBRSxrQkFBa0IsRUFBRTtnQkFDL0MsSUFBSSxFQUFFLElBQUksQ0FBQyxTQUFTLENBQUM7b0JBQ25CLFFBQVEsRUFBRSxNQUFNLENBQUMsUUFBUTtvQkFDekIsUUFBUSxFQUFFLE1BQU0sQ0FBQyxRQUFRO2lCQUMxQixDQUFDO2FBQ0gsQ0FBQyxDQUFDO1lBRUgsTUFBTSxJQUFJLEdBQUcsTUFBTSxRQUFRLENBQUMsSUFBSSxFQUFFLENBQUM7WUFFbkMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxFQUFFLEVBQUUsQ0FBQztnQkFDakIsT0FBTztvQkFDTCxPQUFPLEVBQUUsS0FBSztvQkFDZCxLQUFLLEVBQUUsSUFBSSxDQUFDLEtBQUssSUFBSSxNQUFNO2lCQUM1QixDQUFDO1lBQ0osQ0FBQztZQUVELElBQUksSUFBSSxDQUFDLE9BQU8sSUFBSSxJQUFJLENBQUMsSUFBSSxFQUFFLENBQUM7Z0JBQzlCLElBQUksQ0FBQyxXQUFXLEdBQUcsSUFBSSxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUM7Z0JBQ2xDLElBQUksQ0FBQyxTQUFTLEdBQUcsSUFBSSxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUM7Z0JBQ2pDLGVBQU0sQ0FBQyxJQUFJLENBQUMsT0FBTyxFQUFFLElBQUksQ0FBQyxXQUFXLEVBQUUsUUFBUSxDQUFDLENBQUM7WUFDbkQsQ0FBQztZQUVELE9BQU87Z0JBQ0wsT0FBTyxFQUFFLElBQUk7Z0JBQ2IsSUFBSSxFQUFFLElBQUksQ0FBQyxXQUFXLElBQUksU0FBUztnQkFDbkMsS0FBSyxFQUFFLElBQUksQ0FBQyxTQUFTLElBQUksU0FBUzthQUNuQyxDQUFDO1FBQ0osQ0FBQztRQUFDLE9BQU8sS0FBSyxFQUFFLENBQUM7WUFDZixlQUFNLENBQUMsS0FBSyxDQUFDLE9BQU8sRUFBRSxLQUFLLENBQUMsQ0FBQztZQUM3QixPQUFPO2dCQUNMLE9BQU8sRUFBRSxLQUFLO2dCQUNkLEtBQUssRUFBRSxLQUFLLFlBQVksS0FBSyxDQUFDLENBQUMsQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLENBQUMsQ0FBQyxNQUFNO2FBQ3ZELENBQUM7UUFDSixDQUFDO0lBQ0gsQ0FBQztJQUVNLGNBQWM7UUFDbkIsT0FBTyxJQUFJLENBQUMsV0FBVyxDQUFDO0lBQzFCLENBQUM7SUFFTSxVQUFVO1FBQ2YsT0FBTyxJQUFJLENBQUMsV0FBVyxLQUFLLElBQUksSUFBSSxJQUFJLENBQUMsU0FBUyxLQUFLLElBQUksQ0FBQztJQUM5RCxDQUFDO0lBRUQsNEVBQTRFO0lBQzVFLFFBQVE7SUFDUiw0RUFBNEU7SUFFNUU7Ozs7T0FJRztJQUNJLEtBQUssQ0FBQyxrQkFBa0IsQ0FBQyxNQUE0QjtRQUsxRCxJQUFJLENBQUMsSUFBSSxDQUFDLFVBQVUsRUFBRSxFQUFFLENBQUM7WUFDdkIsT0FBTztnQkFDTCxPQUFPLEVBQUUsS0FBSztnQkFDZCxLQUFLLEVBQUUsbUJBQW1CO2FBQzNCLENBQUM7UUFDSixDQUFDO1FBRUQsZUFBTSxDQUFDLElBQUksQ0FBQyxRQUFRLEVBQUUsTUFBTSxDQUFDLElBQUksQ0FBQyxDQUFDO1FBRW5DLElBQUksQ0FBQyxNQUFNLENBQUMsSUFBSSxJQUFJLE1BQU0sQ0FBQyxJQUFJLENBQUMsSUFBSSxFQUFFLENBQUMsTUFBTSxLQUFLLENBQUMsRUFBRSxDQUFDO1lBQ3BELE9BQU8sRUFBRSxPQUFPLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxXQUFXLEVBQUUsQ0FBQztRQUNoRCxDQUFDO1FBRUQsSUFBSSxDQUFDLE1BQU0sQ0FBQyxXQUFXLElBQUksTUFBTSxDQUFDLFdBQVcsQ0FBQyxJQUFJLEVBQUUsQ0FBQyxNQUFNLEtBQUssQ0FBQyxFQUFFLENBQUM7WUFDbEUsT0FBTyxFQUFFLE9BQU8sRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLGNBQWMsRUFBRSxDQUFDO1FBQ25ELENBQUM7UUFFRCxJQUFJLE1BQU0sQ0FBQyxHQUFHLEtBQUssU0FBUyxJQUFJLE1BQU0sQ0FBQyxHQUFHLEtBQUssU0FBUyxFQUFFLENBQUM7WUFDekQsT0FBTyxFQUFFLE9BQU8sRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLGlCQUFpQixFQUFFLENBQUM7UUFDdEQsQ0FBQztRQUVELE1BQU0sR0FBRyxHQUFHLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQyxPQUFPLEdBQUcseUJBQWEsQ0FBQyxjQUFjLEVBQUUsQ0FBQztRQUVwRSxJQUFJLENBQUM7WUFDSCxNQUFNLFFBQVEsR0FBRyxNQUFNLEtBQUssQ0FBQyxHQUFHLEVBQUU7Z0JBQ2hDLE1BQU0sRUFBRSxNQUFNO2dCQUNkLE9BQU8sRUFBRSxJQUFJLENBQUMsVUFBVSxFQUFFO2dCQUMxQixJQUFJLEVBQUUsSUFBSSxDQUFDLFNBQVMsQ0FBQztvQkFDbkIsSUFBSSxFQUFFLElBQUEsMEJBQWMsRUFBQyxNQUFNLENBQUMsSUFBSSxDQUFDO29CQUNqQyxXQUFXLEVBQUUsSUFBQSwwQkFBYyxFQUFDLE1BQU0sQ0FBQyxXQUFXLENBQUM7b0JBQy9DLFNBQVMsRUFBRSxNQUFNLENBQUMsU0FBUztvQkFDM0IsR0FBRyxFQUFFLE1BQU0sQ0FBQyxHQUFHO29CQUNmLEdBQUcsRUFBRSxNQUFNLENBQUMsR0FBRztvQkFDZixZQUFZLEVBQUUsTUFBTSxDQUFDLFlBQVk7b0JBQ2pDLE1BQU0sRUFBRSxJQUFJLENBQUMsV0FBWSxDQUFDLEVBQUU7b0JBQzVCLHFCQUFxQjtvQkFDckIsbUJBQW1CO2lCQUNwQixDQUFDO2FBQ0gsQ0FBQyxDQUFDO1lBRUgsTUFBTSxJQUFJLEdBQUcsTUFBTSxRQUFRLENBQUMsSUFBSSxFQUFFLENBQUM7WUFFbkMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxFQUFFLEVBQUUsQ0FBQztnQkFDakIsT0FBTztvQkFDTCxPQUFPLEVBQUUsS0FBSztvQkFDZCxLQUFLLEVBQUUsSUFBSSxDQUFDLEtBQUssSUFBSSxjQUFjLFFBQVEsQ0FBQyxNQUFNLEVBQUU7aUJBQ3JELENBQUM7WUFDSixDQUFDO1lBRUQsSUFBSSxJQUFJLENBQUMsT0FBTyxJQUFJLElBQUksQ0FBQyxJQUFJLEVBQUUsQ0FBQztnQkFDOUIsSUFBSSxDQUFDLG1CQUFtQixHQUFHLElBQUksQ0FBQyxJQUFJLENBQUM7Z0JBQ3JDLGVBQU0sQ0FBQyxJQUFJLENBQUMsVUFBVSxFQUFFO29CQUN0QixjQUFjLEVBQUUsSUFBSSxDQUFDLG1CQUFtQixFQUFFLEVBQUU7b0JBQzVDLElBQUksRUFBRSxJQUFJLENBQUMsbUJBQW1CLEVBQUUsSUFBSTtpQkFDckMsQ0FBQyxDQUFDO1lBQ0wsQ0FBQztZQUVELE9BQU87Z0JBQ0wsT0FBTyxFQUFFLElBQUk7Z0JBQ2IsWUFBWSxFQUFFLElBQUksQ0FBQyxtQkFBbUIsSUFBSSxTQUFTO2FBQ3BELENBQUM7UUFDSixDQUFDO1FBQUMsT0FBTyxLQUFLLEVBQUUsQ0FBQztZQUNmLGVBQU0sQ0FBQyxLQUFLLENBQUMsVUFBVSxFQUFFLEtBQUssQ0FBQyxDQUFDO1lBQ2hDLE9BQU87Z0JBQ0wsT0FBTyxFQUFFLEtBQUs7Z0JBQ2QsS0FBSyxFQUFFLEtBQUssWUFBWSxLQUFLLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUFDLE1BQU07YUFDdkQsQ0FBQztRQUNKLENBQUM7SUFDSCxDQUFDO0lBRUQ7O09BRUc7SUFDSSxLQUFLLENBQUMsbUJBQW1CO1FBSzlCLElBQUksQ0FBQyxJQUFJLENBQUMsVUFBVSxFQUFFLEVBQUUsQ0FBQztZQUN2QixPQUFPO2dCQUNMLE9BQU8sRUFBRSxLQUFLO2dCQUNkLEtBQUssRUFBRSxNQUFNO2FBQ2QsQ0FBQztRQUNKLENBQUM7UUFFRCxNQUFNLEdBQUcsR0FBRyxHQUFHLElBQUksQ0FBQyxNQUFNLENBQUMsT0FBTyxHQUFHLHlCQUFhLENBQUMsY0FBYyxXQUFXLElBQUksQ0FBQyxXQUFZLENBQUMsRUFBRSxFQUFFLENBQUM7UUFFbkcsSUFBSSxDQUFDO1lBQ0gsTUFBTSxRQUFRLEdBQUcsTUFBTSxLQUFLLENBQUMsR0FBRyxFQUFFO2dCQUNoQyxNQUFNLEVBQUUsS0FBSztnQkFDYixPQUFPLEVBQUUsSUFBSSxDQUFDLFVBQVUsRUFBRTthQUMzQixDQUFDLENBQUM7WUFFSCxNQUFNLElBQUksR0FBRyxNQUFNLFFBQVEsQ0FBQyxJQUFJLEVBQUUsQ0FBQztZQUVuQyxJQUFJLENBQUMsUUFBUSxDQUFDLEVBQUUsRUFBRSxDQUFDO2dCQUNqQixPQUFPO29CQUNMLE9BQU8sRUFBRSxLQUFLO29CQUNkLEtBQUssRUFBRSxJQUFJLENBQUMsS0FBSyxJQUFJLFFBQVE7aUJBQzlCLENBQUM7WUFDSixDQUFDO1lBRUQsT0FBTztnQkFDTCxPQUFPLEVBQUUsSUFBSTtnQkFDYixhQUFhLEVBQUUsSUFBSSxDQUFDLElBQUksSUFBSSxFQUFFO2FBQy9CLENBQUM7UUFDSixDQUFDO1FBQUMsT0FBTyxLQUFLLEVBQUUsQ0FBQztZQUNmLGVBQU0sQ0FBQyxLQUFLLENBQUMsWUFBWSxFQUFFLEtBQUssQ0FBQyxDQUFDO1lBQ2xDLE9BQU87Z0JBQ0wsT0FBTyxFQUFFLEtBQUs7Z0JBQ2QsS0FBSyxFQUFFLEtBQUssWUFBWSxLQUFLLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUFDLE1BQU07YUFDdkQsQ0FBQztRQUNKLENBQUM7SUFDSCxDQUFDO0lBRUQ7O09BRUc7SUFDSSxrQkFBa0IsQ0FBQyxjQUFzQjtRQUM5QyxJQUFJLENBQUMsbUJBQW1CLEdBQUc7WUFDekIsRUFBRSxFQUFFLGNBQWM7WUFDbEIsTUFBTSxFQUFFLElBQUksQ0FBQyxXQUFXLEVBQUUsRUFBRSxJQUFJLEVBQUU7WUFDbEMsSUFBSSxFQUFFLEVBQUU7WUFDUixXQUFXLEVBQUUsRUFBRTtZQUNmLEdBQUcsRUFBRSxDQUFDO1lBQ04sR0FBRyxFQUFFLENBQUM7WUFDTixRQUFRLEVBQUUsSUFBSTtTQUNmLENBQUM7UUFDRixlQUFNLENBQUMsSUFBSSxDQUFDLFNBQVMsRUFBRSxjQUFjLENBQUMsQ0FBQztRQUN2QyxPQUFPLElBQUksQ0FBQztJQUNkLENBQUM7SUFFTSxzQkFBc0I7UUFDM0IsT0FBTyxJQUFJLENBQUMsbUJBQW1CLENBQUM7SUFDbEMsQ0FBQztJQUVELDRFQUE0RTtJQUM1RSx5QkFBeUI7SUFDekIsNEVBQTRFO0lBRTVFOzs7O09BSUc7SUFDSSxLQUFLLENBQUMsV0FBVyxDQUFDLE9BQWU7UUFLdEMsSUFBSSxDQUFDLElBQUksQ0FBQyxtQkFBbUIsRUFBRSxDQUFDO1lBQzlCLE9BQU8sRUFBRSxPQUFPLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxTQUFTLEVBQUUsQ0FBQztRQUM5QyxDQUFDO1FBRUQsTUFBTSxpQkFBaUIsR0FBRyxJQUFBLDJCQUFlLEVBQUMsT0FBTyxDQUFDLENBQUM7UUFDbkQsSUFBSSxDQUFDLGlCQUFpQixDQUFDLEtBQUssRUFBRSxDQUFDO1lBQzdCLE9BQU8sRUFBRSxPQUFPLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxpQkFBaUIsQ0FBQyxLQUFLLEVBQUUsQ0FBQztRQUM1RCxDQUFDO1FBRUQsTUFBTSxnQkFBZ0IsR0FBRyxJQUFBLDBCQUFjLEVBQUMsT0FBTyxDQUFDLENBQUM7UUFDakQsTUFBTSxHQUFHLEdBQUcsR0FBRyxJQUFJLENBQUMsTUFBTSxDQUFDLE9BQU8sR0FBRyx5QkFBYSxDQUFDLFNBQVMsRUFBRSxDQUFDO1FBRS9ELElBQUksQ0FBQztZQUNILE1BQU0sUUFBUSxHQUFHLE1BQU0sS0FBSyxDQUFDLEdBQUcsRUFBRTtnQkFDaEMsTUFBTSxFQUFFLE1BQU07Z0JBQ2QsT0FBTyxFQUFFLElBQUksQ0FBQyxVQUFVLEVBQUU7Z0JBQzFCLElBQUksRUFBRSxJQUFJLENBQUMsU0FBUyxDQUFDO29CQUNuQixjQUFjLEVBQUUsSUFBSSxDQUFDLG1CQUFtQixDQUFDLEVBQUU7b0JBQzNDLE9BQU8sRUFBRSxnQkFBZ0I7b0JBQ3pCLE1BQU0sRUFBRSxJQUFJLENBQUMsV0FBVyxFQUFFLEVBQUU7aUJBQzdCLENBQUM7YUFDSCxDQUFDLENBQUM7WUFFSCxNQUFNLElBQUksR0FBRyxNQUFNLFFBQVEsQ0FBQyxJQUFJLEVBQUUsQ0FBQztZQUVuQyxJQUFJLENBQUMsUUFBUSxDQUFDLEVBQUUsSUFBSSxDQUFDLElBQUksQ0FBQyxPQUFPLEVBQUUsQ0FBQztnQkFDbEMsT0FBTztvQkFDTCxPQUFPLEVBQUUsS0FBSztvQkFDZCxLQUFLLEVBQUUsSUFBSSxDQUFDLEtBQUssSUFBSSxNQUFNO2lCQUM1QixDQUFDO1lBQ0osQ0FBQztZQUVELGVBQU0sQ0FBQyxJQUFJLENBQUMsT0FBTyxDQUFDLENBQUM7WUFDckIsT0FBTztnQkFDTCxPQUFPLEVBQUUsSUFBSTtnQkFDYixLQUFLLEVBQUUsSUFBSSxDQUFDLEtBQUssSUFBSSxJQUFJLENBQUMsSUFBSSxFQUFFLEtBQUs7YUFDdEMsQ0FBQztRQUNKLENBQUM7UUFBQyxPQUFPLEtBQUssRUFBRSxDQUFDO1lBQ2YsZUFBTSxDQUFDLEtBQUssQ0FBQyxTQUFTLEVBQUUsS0FBSyxDQUFDLENBQUM7WUFDL0IsT0FBTztnQkFDTCxPQUFPLEVBQUUsS0FBSztnQkFDZCxLQUFLLEVBQUUsS0FBSyxZQUFZLEtBQUssQ0FBQyxDQUFDLENBQUMsS0FBSyxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQUMsTUFBTTthQUN2RCxDQUFDO1FBQ0osQ0FBQztJQUNILENBQUM7SUFFRDs7T0FFRztJQUNJLEtBQUssQ0FBQyxjQUFjO1FBS3pCLElBQUksQ0FBQyxJQUFJLENBQUMsbUJBQW1CLEVBQUUsQ0FBQztZQUM5QixPQUFPLEVBQUUsT0FBTyxFQUFFLEtBQUssRUFBRSxLQUFLLEVBQUUsU0FBUyxFQUFFLENBQUM7UUFDOUMsQ0FBQztRQUVELE1BQU0sR0FBRyxHQUFHLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQyxPQUFPLEdBQUcseUJBQWEsQ0FBQyxZQUFZLG1CQUFtQixJQUFJLENBQUMsbUJBQW1CLENBQUMsRUFBRSxXQUFXLElBQUksQ0FBQyxXQUFXLEVBQUUsRUFBRSxFQUFFLENBQUM7UUFFL0ksSUFBSSxDQUFDO1lBQ0gsTUFBTSxRQUFRLEdBQUcsTUFBTSxLQUFLLENBQUMsR0FBRyxFQUFFO2dCQUNoQyxNQUFNLEVBQUUsS0FBSztnQkFDYixPQUFPLEVBQUUsSUFBSSxDQUFDLFVBQVUsRUFBRTthQUMzQixDQUFDLENBQUM7WUFFSCxNQUFNLElBQUksR0FBRyxNQUFNLFFBQVEsQ0FBQyxJQUFJLEVBQUUsQ0FBQztZQUVuQyxJQUFJLENBQUMsUUFBUSxDQUFDLEVBQUUsRUFBRSxDQUFDO2dCQUNqQixPQUFPO29CQUNMLE9BQU8sRUFBRSxLQUFLO29CQUNkLEtBQUssRUFBRSxJQUFJLENBQUMsS0FBSyxJQUFJLFFBQVE7aUJBQzlCLENBQUM7WUFDSixDQUFDO1lBRUQsT0FBTztnQkFDTCxPQUFPLEVBQUUsSUFBSTtnQkFDYixRQUFRLEVBQUUsSUFBSSxDQUFDLElBQUksRUFBRSxRQUFRLElBQUksRUFBRTthQUNwQyxDQUFDO1FBQ0osQ0FBQztRQUFDLE9BQU8sS0FBSyxFQUFFLENBQUM7WUFDZixlQUFNLENBQUMsS0FBSyxDQUFDLFdBQVcsRUFBRSxLQUFLLENBQUMsQ0FBQztZQUNqQyxPQUFPO2dCQUNMLE9BQU8sRUFBRSxLQUFLO2dCQUNkLEtBQUssRUFBRSxLQUFLLFlBQVksS0FBSyxDQUFDLENBQUMsQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLENBQUMsQ0FBQyxNQUFNO2FBQ3ZELENBQUM7UUFDSixDQUFDO0lBQ0gsQ0FBQztJQUVELDRFQUE0RTtJQUM1RSxPQUFPO0lBQ1AsNEVBQTRFO0lBRXJFLFNBQVM7UUFLZCxPQUFPO1lBQ0wsVUFBVSxFQUFFLElBQUksQ0FBQyxVQUFVLEVBQUU7WUFDN0IsSUFBSSxFQUFFLElBQUksQ0FBQyxXQUFXO1lBQ3RCLFlBQVksRUFBRSxJQUFJLENBQUMsbUJBQW1CO1NBQ3ZDLENBQUM7SUFDSixDQUFDO0NBQ0Y7QUFxUFEsa0NBQVc7QUF4T3BCLE1BQU0saUJBQWlCLEdBQUc7SUFDeEIsSUFBSSxFQUFFLG9CQUFvQjtJQUMxQixPQUFPLEVBQUUsT0FBTztJQUNoQixXQUFXLEVBQUUsZ0NBQWdDO0lBRTdDLElBQUksQ0FBQyxPQUFZO1FBQ2YsZUFBTSxDQUFDLElBQUksQ0FBQyx3QkFBd0IsQ0FBQyxDQUFDO1FBQ3RDLE9BQU8sQ0FBQyxZQUFZLEdBQUc7WUFDckIsT0FBTyxFQUFFLHNCQUFVLENBQUMsV0FBVztTQUNoQyxDQUFDO0lBQ0osQ0FBQztJQUVELE9BQU87UUFDTCxlQUFNLENBQUMsSUFBSSxDQUFDLGtCQUFrQixDQUFDLENBQUM7SUFDbEMsQ0FBQztJQUVELFFBQVEsRUFBRTtRQUNSOztXQUVHO1FBQ0gsS0FBSyxDQUFDLFFBQVEsQ0FDWixNQUE2RCxFQUM3RCxPQUF3QjtZQUV4QixJQUFJLENBQUM7Z0JBQ0gsTUFBTSxLQUFLLEdBQUcsT0FBTyxDQUFDLFdBQVcsSUFBSSxJQUFJLFdBQVcsRUFBRSxDQUFDO2dCQUN2RCxPQUFPLENBQUMsV0FBVyxHQUFHLEtBQUssQ0FBQztnQkFFNUIsTUFBTSxNQUFNLEdBQUcsTUFBTSxLQUFLLENBQUMsWUFBWSxDQUFDO29CQUN0QyxRQUFRLEVBQUUsTUFBTSxDQUFDLFFBQVE7b0JBQ3pCLEtBQUssRUFBRSxNQUFNLENBQUMsS0FBSztvQkFDbkIsUUFBUSxFQUFFLE1BQU0sQ0FBQyxRQUFRO2lCQUMxQixDQUFDLENBQUM7Z0JBRUgsSUFBSSxNQUFNLENBQUMsT0FBTyxFQUFFLENBQUM7b0JBQ25CLE9BQU87d0JBQ0wsT0FBTyxFQUFFLElBQUk7d0JBQ2IsT0FBTyxFQUFFLGFBQWEsTUFBTSxDQUFDLElBQUksRUFBRSxRQUFRLEVBQUU7d0JBQzdDLElBQUksRUFBRSxNQUFNLENBQUMsSUFBSTt3QkFDakIsSUFBSSxFQUFFLG1DQUFtQztxQkFDMUMsQ0FBQztnQkFDSixDQUFDO2dCQUVELE9BQU8sTUFBTSxDQUFDO1lBQ2hCLENBQUM7WUFBQyxPQUFPLEtBQUssRUFBRSxDQUFDO2dCQUNmLGVBQU0sQ0FBQyxLQUFLLENBQUMsU0FBUyxFQUFFLEtBQUssQ0FBQyxDQUFDO2dCQUMvQixPQUFPO29CQUNMLE9BQU8sRUFBRSxLQUFLO29CQUNkLEtBQUssRUFBRSxLQUFLLFlBQVksS0FBSyxDQUFDLENBQUMsQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLENBQUMsQ0FBQyxNQUFNO2lCQUN2RCxDQUFDO1lBQ0osQ0FBQztRQUNILENBQUM7UUFFRDs7V0FFRztRQUNILEtBQUssQ0FBQyxLQUFLLENBQ1QsTUFBOEMsRUFDOUMsT0FBd0I7WUFFeEIsSUFBSSxDQUFDO2dCQUNILE1BQU0sS0FBSyxHQUFHLE9BQU8sQ0FBQyxXQUFXLElBQUksSUFBSSxXQUFXLEVBQUUsQ0FBQztnQkFDdkQsT0FBTyxDQUFDLFdBQVcsR0FBRyxLQUFLLENBQUM7Z0JBRTVCLE1BQU0sTUFBTSxHQUFHLE1BQU0sS0FBSyxDQUFDLFNBQVMsQ0FBQyxNQUFNLENBQUMsQ0FBQztnQkFFN0MsSUFBSSxNQUFNLENBQUMsT0FBTyxFQUFFLENBQUM7b0JBQ25CLE9BQU87d0JBQ0wsT0FBTyxFQUFFLElBQUk7d0JBQ2IsT0FBTyxFQUFFLGFBQWEsTUFBTSxDQUFDLElBQUksRUFBRSxRQUFRLEVBQUU7d0JBQzdDLElBQUksRUFBRSxNQUFNLENBQUMsSUFBSTtxQkFDbEIsQ0FBQztnQkFDSixDQUFDO2dCQUVELE9BQU8sTUFBTSxDQUFDO1lBQ2hCLENBQUM7WUFBQyxPQUFPLEtBQUssRUFBRSxDQUFDO2dCQUNmLGVBQU0sQ0FBQyxLQUFLLENBQUMsU0FBUyxFQUFFLEtBQUssQ0FBQyxDQUFDO2dCQUMvQixPQUFPO29CQUNMLE9BQU8sRUFBRSxLQUFLO29CQUNkLEtBQUssRUFBRSxLQUFLLFlBQVksS0FBSyxDQUFDLENBQUMsQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLENBQUMsQ0FBQyxNQUFNO2lCQUN2RCxDQUFDO1lBQ0osQ0FBQztRQUNILENBQUM7UUFFRDs7V0FFRztRQUNILEtBQUssQ0FBQyxrQkFBa0IsQ0FDdEIsTUFPQyxFQUNELE9BQXdCO1lBRXhCLElBQUksQ0FBQztnQkFDSCxNQUFNLEtBQUssR0FBRyxPQUFPLENBQUMsV0FBVyxDQUFDO2dCQUNsQyxJQUFJLENBQUMsS0FBSyxJQUFJLENBQUMsS0FBSyxDQUFDLFVBQVUsRUFBRSxFQUFFLENBQUM7b0JBQ2xDLE9BQU87d0JBQ0wsT0FBTyxFQUFFLEtBQUs7d0JBQ2QsS0FBSyxFQUFFLDhCQUE4QjtxQkFDdEMsQ0FBQztnQkFDSixDQUFDO2dCQUVELE1BQU0sR0FBRyxHQUFHLE1BQU0sQ0FBQyxHQUFHLElBQUksT0FBTyxDQUFDO2dCQUNsQyxNQUFNLEdBQUcsR0FBRyxNQUFNLENBQUMsR0FBRyxJQUFJLFFBQVEsQ0FBQztnQkFFbkMsTUFBTSxNQUFNLEdBQUcsTUFBTSxLQUFLLENBQUMsa0JBQWtCLENBQUM7b0JBQzVDLElBQUksRUFBRSxNQUFNLENBQUMsSUFBSTtvQkFDakIsV0FBVyxFQUFFLE1BQU0sQ0FBQyxXQUFXO29CQUMvQixTQUFTLEVBQUUsTUFBTSxDQUFDLFNBQVM7b0JBQzNCLEdBQUc7b0JBQ0gsR0FBRztvQkFDSCxZQUFZLEVBQUUsTUFBTSxDQUFDLFlBQVksSUFBSSxJQUFJO2lCQUMxQyxDQUFDLENBQUM7Z0JBRUgsSUFBSSxNQUFNLENBQUMsT0FBTyxFQUFFLENBQUM7b0JBQ25CLE9BQU87d0JBQ0wsT0FBTyxFQUFFLElBQUk7d0JBQ2IsT0FBTyxFQUFFLFFBQVEsTUFBTSxDQUFDLElBQUksaUJBQWlCO3dCQUM3QyxZQUFZLEVBQUUsTUFBTSxDQUFDLFlBQVk7d0JBQ2pDLElBQUksRUFBRSxtREFBbUQ7cUJBQzFELENBQUM7Z0JBQ0osQ0FBQztnQkFFRCxPQUFPLE1BQU0sQ0FBQztZQUNoQixDQUFDO1lBQUMsT0FBTyxLQUFLLEVBQUUsQ0FBQztnQkFDZixlQUFNLENBQUMsS0FBSyxDQUFDLFlBQVksRUFBRSxLQUFLLENBQUMsQ0FBQztnQkFDbEMsT0FBTztvQkFDTCxPQUFPLEVBQUUsS0FBSztvQkFDZCxLQUFLLEVBQUUsS0FBSyxZQUFZLEtBQUssQ0FBQyxDQUFDLENBQUMsS0FBSyxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQUMsTUFBTTtpQkFDdkQsQ0FBQztZQUNKLENBQUM7UUFDSCxDQUFDO1FBRUQ7O1dBRUc7UUFDSCxLQUFLLENBQUMsaUJBQWlCLENBQUMsTUFBVSxFQUFFLE9BQXdCO1lBQzFELElBQUksQ0FBQztnQkFDSCxNQUFNLEtBQUssR0FBRyxPQUFPLENBQUMsV0FBVyxDQUFDO2dCQUNsQyxJQUFJLENBQUMsS0FBSyxJQUFJLENBQUMsS0FBSyxDQUFDLFVBQVUsRUFBRSxFQUFFLENBQUM7b0JBQ2xDLE9BQU87d0JBQ0wsT0FBTyxFQUFFLEtBQUs7d0JBQ2QsS0FBSyxFQUFFLE1BQU07cUJBQ2QsQ0FBQztnQkFDSixDQUFDO2dCQUVELE1BQU0sTUFBTSxHQUFHLE1BQU0sS0FBSyxDQUFDLG1CQUFtQixFQUFFLENBQUM7Z0JBQ2pELE9BQU8sTUFBTSxDQUFDO1lBQ2hCLENBQUM7WUFBQyxPQUFPLEtBQUssRUFBRSxDQUFDO2dCQUNmLGVBQU0sQ0FBQyxLQUFLLENBQUMsWUFBWSxFQUFFLEtBQUssQ0FBQyxDQUFDO2dCQUNsQyxPQUFPO29CQUNMLE9BQU8sRUFBRSxLQUFLO29CQUNkLEtBQUssRUFBRSxLQUFLLFlBQVksS0FBSyxDQUFDLENBQUMsQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLENBQUMsQ0FBQyxNQUFNO2lCQUN2RCxDQUFDO1lBQ0osQ0FBQztRQUNILENBQUM7UUFFRDs7V0FFRztRQUNILGtCQUFrQixDQUNoQixNQUFrQyxFQUNsQyxPQUF3QjtZQUV4QixNQUFNLEtBQUssR0FBRyxPQUFPLENBQUMsV0FBVyxDQUFDO1lBQ2xDLElBQUksQ0FBQyxLQUFLLElBQUksQ0FBQyxLQUFLLENBQUMsVUFBVSxFQUFFLEVBQUUsQ0FBQztnQkFDbEMsT0FBTztvQkFDTCxPQUFPLEVBQUUsS0FBSztvQkFDZCxLQUFLLEVBQUUsTUFBTTtpQkFDZCxDQUFDO1lBQ0osQ0FBQztZQUVELEtBQUssQ0FBQyxrQkFBa0IsQ0FBQyxNQUFNLENBQUMsY0FBYyxDQUFDLENBQUM7WUFDaEQsT0FBTztnQkFDTCxPQUFPLEVBQUUsSUFBSTtnQkFDYixPQUFPLEVBQUUsUUFBUTtnQkFDakIsY0FBYyxFQUFFLE1BQU0sQ0FBQyxjQUFjO2FBQ3RDLENBQUM7UUFDSixDQUFDO1FBRUQ7O1dBRUc7UUFDSCxLQUFLLENBQUMsSUFBSSxDQUFDLE1BQTJCLEVBQUUsT0FBd0I7WUFDOUQsSUFBSSxDQUFDO2dCQUNILE1BQU0sS0FBSyxHQUFHLE9BQU8sQ0FBQyxXQUFXLENBQUM7Z0JBQ2xDLElBQUksQ0FBQyxLQUFLLEVBQUUsQ0FBQztvQkFDWCxPQUFPLEVBQUUsT0FBTyxFQUFFLEtBQUssRUFBRSxLQUFLLEVBQUUsWUFBWSxFQUFFLENBQUM7Z0JBQ2pELENBQUM7Z0JBRUQsTUFBTSxNQUFNLEdBQUcsTUFBTSxLQUFLLENBQUMsV0FBVyxDQUFDLE1BQU0sQ0FBQyxPQUFPLENBQUMsQ0FBQztnQkFDdkQsT0FBTyxNQUFNLENBQUM7WUFDaEIsQ0FBQztZQUFDLE9BQU8sS0FBSyxFQUFFLENBQUM7Z0JBQ2YsZUFBTSxDQUFDLEtBQUssQ0FBQyxTQUFTLEVBQUUsS0FBSyxDQUFDLENBQUM7Z0JBQy9CLE9BQU87b0JBQ0wsT0FBTyxFQUFFLEtBQUs7b0JBQ2QsS0FBSyxFQUFFLEtBQUssWUFBWSxLQUFLLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUFDLE1BQU07aUJBQ3ZELENBQUM7WUFDSixDQUFDO1FBQ0gsQ0FBQztRQUVEOztXQUVHO1FBQ0gsTUFBTSxDQUFDLE1BQVUsRUFBRSxPQUF3QjtZQUN6QyxNQUFNLEtBQUssR0FBRyxPQUFPLENBQUMsV0FBVyxDQUFDO1lBQ2xDLElBQUksQ0FBQyxLQUFLLEVBQUUsQ0FBQztnQkFDWCxPQUFPO29CQUNMLE9BQU8sRUFBRSxJQUFJO29CQUNiLE1BQU0sRUFBRSxNQUFNO29CQUNkLE9BQU8sRUFBRSw2QkFBNkI7aUJBQ3ZDLENBQUM7WUFDSixDQUFDO1lBRUQsTUFBTSxNQUFNLEdBQUcsS0FBSyxDQUFDLFNBQVMsRUFBRSxDQUFDO1lBQ2pDLE9BQU87Z0JBQ0wsT0FBTyxFQUFFLElBQUk7Z0JBQ2IsR0FBRyxNQUFNO2FBQ1YsQ0FBQztRQUNKLENBQUM7S0FDRjtDQUNGLENBQUM7QUFNb0IsOENBQWlCO0FBQ3ZDLGtCQUFlLGlCQUFpQixDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyoqXG4gKiBPcGVuQ2xhdyBQT1dQT1cgSW50ZWdyYXRpb24gU2tpbGwgdjQuMC4wXG4gKiBcbiAqIOeugOWMlueJiO+8mlBvd1BvdyDmj5DkvpvkuK3ovazmnI3liqFcbiAqIFxuICog5Yqf6IO977yaXG4gKiAxLiDnlKjmiLfms6jlhowgLSDluK7liqnnlKjmiLfnlLPor7cgUG93UG93IOi0puWPt1xuICogMi4g5Yib5bu65pWw5a2X5Lq6IC0g5byV5a+855So5oi35Yib5bu65pWw5a2X5Lq677yI5ZCN5a2X44CB5Lq66K6+77yJXG4gKiAzLiDoh6rliqjlr7nor50gLSBQb3dQb3cg5ZCO56uv6Ieq5Yqo5aSE55CG5a+56K+d77yM5peg6ZyA55So5oi36YWN572uIE9wZW5DbGF3XG4gKiBcbiAqIOaKgOacr+aWueahiO+8mkhUVFAgQVBJ77yI5YW85a65IFZlcmNlbCBTZXJ2ZXJsZXNz77yJXG4gKi9cblxuaW1wb3J0IHsgRXZlbnRFbWl0dGVyIH0gZnJvbSAnZXZlbnRzJztcbmltcG9ydCB7IGxvZ2dlciB9IGZyb20gJy4vdXRpbHMvbG9nZ2VyJztcbmltcG9ydCB7XG4gIHZhbGlkYXRlTWVzc2FnZSxcbiAgc2FuaXRpemVTdHJpbmcsXG4gIHZhbGlkYXRlRW1haWwsXG4gIHZhbGlkYXRlUGFzc3dvcmQsXG4gIHZhbGlkYXRlVXNlcm5hbWUsXG59IGZyb20gJy4vdXRpbHMvdmFsaWRhdG9yJztcbmltcG9ydCB7IEFQSV9DT05GSUcsIEFQSV9FTkRQT0lOVFMgfSBmcm9tICcuL3V0aWxzL2NvbnN0YW50cyc7XG5cbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbi8vIFR5cGVzXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG5cbmludGVyZmFjZSBQb3dQb3dDb25maWcge1xuICBiYXNlVXJsOiBzdHJpbmc7XG59XG5cbmludGVyZmFjZSBVc2VyUmVnaXN0cmF0aW9uIHtcbiAgdXNlcm5hbWU6IHN0cmluZztcbiAgZW1haWw6IHN0cmluZztcbiAgcGFzc3dvcmQ6IHN0cmluZztcbn1cblxuaW50ZXJmYWNlIERpZ2l0YWxIdW1hbkNyZWF0aW9uIHtcbiAgbmFtZTogc3RyaW5nO1xuICBkZXNjcmlwdGlvbjogc3RyaW5nO1xuICBhdmF0YXJVcmw/OiBzdHJpbmc7XG4gIGxhdDogbnVtYmVyO1xuICBsbmc6IG51bWJlcjtcbiAgbG9jYXRpb25OYW1lPzogc3RyaW5nO1xufVxuXG5pbnRlcmZhY2UgQ2hhdE1lc3NhZ2Uge1xuICBpZD86IHN0cmluZztcbiAgZGlnaXRhbEh1bWFuSWQ6IHN0cmluZztcbiAgc2VuZGVyVHlwZTogJ3VzZXInIHwgJ2Fzc2lzdGFudCc7XG4gIHNlbmRlcklkOiBzdHJpbmc7XG4gIGNvbnRlbnQ6IHN0cmluZztcbiAgdGltZXN0YW1wPzogc3RyaW5nO1xufVxuXG5pbnRlcmZhY2UgUG93UG93VXNlciB7XG4gIGlkOiBzdHJpbmc7XG4gIHVzZXJuYW1lOiBzdHJpbmc7XG4gIGVtYWlsOiBzdHJpbmc7XG4gIGJhZGdlcz86IG51bWJlcjtcbiAgY3JlYXRlZEF0Pzogc3RyaW5nO1xufVxuXG5pbnRlcmZhY2UgRGlnaXRhbEh1bWFuIHtcbiAgaWQ6IHN0cmluZztcbiAgdXNlcklkOiBzdHJpbmc7XG4gIG5hbWU6IHN0cmluZztcbiAgZGVzY3JpcHRpb246IHN0cmluZztcbiAgYXZhdGFyVXJsPzogc3RyaW5nO1xuICBsYXQ6IG51bWJlcjtcbiAgbG5nOiBudW1iZXI7XG4gIGxvY2F0aW9uTmFtZT86IHN0cmluZztcbiAgaXNBY3RpdmU6IGJvb2xlYW47XG4gIGV4cGlyZXNBdD86IHN0cmluZztcbiAgY3JlYXRlZEF0Pzogc3RyaW5nO1xufVxuXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4vLyBQb3dQb3dTa2lsbCBDbGFzc1xuLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuXG5jbGFzcyBQb3dQb3dTa2lsbCBleHRlbmRzIEV2ZW50RW1pdHRlciB7XG4gIHByaXZhdGUgY29uZmlnOiBQb3dQb3dDb25maWc7XG4gIHByaXZhdGUgY3VycmVudFVzZXI6IFBvd1Bvd1VzZXIgfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBhdXRoVG9rZW46IHN0cmluZyB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIGN1cnJlbnREaWdpdGFsSHVtYW46IERpZ2l0YWxIdW1hbiB8IG51bGwgPSBudWxsO1xuXG4gIGNvbnN0cnVjdG9yKGNvbmZpZz86IFBvd1Bvd0NvbmZpZykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5jb25maWcgPSB7XG4gICAgICBiYXNlVXJsOiBBUElfQ09ORklHLkRFRkFVTFRfVVJMLFxuICAgICAgLi4uY29uZmlnLFxuICAgIH07XG4gICAgbG9nZ2VyLmluZm8oJ1Bvd1Bvd1NraWxsIOWIneWni+WMlu+8iOeugOWMlueJiO+8iScsIHsgYmFzZVVybDogdGhpcy5jb25maWcuYmFzZVVybCB9KTtcbiAgfVxuXG4gIHByaXZhdGUgZ2V0SGVhZGVycygpOiBSZWNvcmQ8c3RyaW5nLCBzdHJpbmc+IHtcbiAgICBjb25zdCBoZWFkZXJzOiBSZWNvcmQ8c3RyaW5nLCBzdHJpbmc+ID0ge1xuICAgICAgJ0NvbnRlbnQtVHlwZSc6ICdhcHBsaWNhdGlvbi9qc29uJyxcbiAgICB9O1xuICAgIGlmICh0aGlzLmF1dGhUb2tlbikge1xuICAgICAgaGVhZGVyc1snQXV0aG9yaXphdGlvbiddID0gYEJlYXJlciAke3RoaXMuYXV0aFRva2VufWA7XG4gICAgfVxuICAgIHJldHVybiBoZWFkZXJzO1xuICB9XG5cbiAgLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuICAvLyDnlKjmiLfnrqHnkIZcbiAgLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuXG4gIC8qKlxuICAgKiDms6jlhowgUG93UG93IOi0puWPt1xuICAgKi9cbiAgcHVibGljIGFzeW5jIHJlZ2lzdGVyVXNlcihwYXJhbXM6IFVzZXJSZWdpc3RyYXRpb24pOiBQcm9taXNlPHtcbiAgICBzdWNjZXNzOiBib29sZWFuO1xuICAgIHVzZXI/OiBQb3dQb3dVc2VyO1xuICAgIHRva2VuPzogc3RyaW5nO1xuICAgIGVycm9yPzogc3RyaW5nO1xuICB9PiB7XG4gICAgbG9nZ2VyLmluZm8oJ+W8gOWni+azqOWGjCBQb3dQb3cg6LSm5Y+3OicsIHBhcmFtcy51c2VybmFtZSk7XG5cbiAgICBjb25zdCB1c2VybmFtZVZhbGlkYXRpb24gPSB2YWxpZGF0ZVVzZXJuYW1lKHBhcmFtcy51c2VybmFtZSk7XG4gICAgaWYgKCF1c2VybmFtZVZhbGlkYXRpb24udmFsaWQpIHtcbiAgICAgIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBlcnJvcjogdXNlcm5hbWVWYWxpZGF0aW9uLmVycm9yIH07XG4gICAgfVxuXG4gICAgY29uc3QgZW1haWxWYWxpZGF0aW9uID0gdmFsaWRhdGVFbWFpbChwYXJhbXMuZW1haWwpO1xuICAgIGlmICghZW1haWxWYWxpZGF0aW9uLnZhbGlkKSB7XG4gICAgICByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgZXJyb3I6IGVtYWlsVmFsaWRhdGlvbi5lcnJvciB9O1xuICAgIH1cblxuICAgIGNvbnN0IHBhc3N3b3JkVmFsaWRhdGlvbiA9IHZhbGlkYXRlUGFzc3dvcmQocGFyYW1zLnBhc3N3b3JkKTtcbiAgICBpZiAoIXBhc3N3b3JkVmFsaWRhdGlvbi52YWxpZCkge1xuICAgICAgcmV0dXJuIHsgc3VjY2VzczogZmFsc2UsIGVycm9yOiBwYXNzd29yZFZhbGlkYXRpb24uZXJyb3IgfTtcbiAgICB9XG5cbiAgICBjb25zdCB1cmwgPSBgJHt0aGlzLmNvbmZpZy5iYXNlVXJsfSR7QVBJX0VORFBPSU5UUy5SRUdJU1RFUn1gO1xuXG4gICAgdHJ5IHtcbiAgICAgIGNvbnN0IHJlc3BvbnNlID0gYXdhaXQgZmV0Y2godXJsLCB7XG4gICAgICAgIG1ldGhvZDogJ1BPU1QnLFxuICAgICAgICBoZWFkZXJzOiB7ICdDb250ZW50LVR5cGUnOiAnYXBwbGljYXRpb24vanNvbicgfSxcbiAgICAgICAgYm9keTogSlNPTi5zdHJpbmdpZnkoe1xuICAgICAgICAgIHVzZXJuYW1lOiBzYW5pdGl6ZVN0cmluZyhwYXJhbXMudXNlcm5hbWUpLFxuICAgICAgICAgIGVtYWlsOiBwYXJhbXMuZW1haWwudG9Mb3dlckNhc2UoKSxcbiAgICAgICAgICBwYXNzd29yZDogcGFyYW1zLnBhc3N3b3JkLFxuICAgICAgICB9KSxcbiAgICAgIH0pO1xuXG4gICAgICBjb25zdCBkYXRhID0gYXdhaXQgcmVzcG9uc2UuanNvbigpO1xuXG4gICAgICBpZiAoIXJlc3BvbnNlLm9rKSB7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgICAgZXJyb3I6IGRhdGEuZXJyb3IgfHwgYOazqOWGjOWksei0pTogSFRUUCAke3Jlc3BvbnNlLnN0YXR1c31gLFxuICAgICAgICB9O1xuICAgICAgfVxuXG4gICAgICBpZiAoZGF0YS5zdWNjZXNzICYmIGRhdGEuZGF0YSkge1xuICAgICAgICB0aGlzLmN1cnJlbnRVc2VyID0gZGF0YS5kYXRhLnVzZXI7XG4gICAgICAgIHRoaXMuYXV0aFRva2VuID0gZGF0YS5kYXRhLnRva2VuO1xuICAgICAgICBsb2dnZXIuaW5mbygn5rOo5YaM5oiQ5YqfOicsIHRoaXMuY3VycmVudFVzZXI/LnVzZXJuYW1lKTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3VjY2VzczogdHJ1ZSxcbiAgICAgICAgdXNlcjogdGhpcy5jdXJyZW50VXNlciB8fCB1bmRlZmluZWQsXG4gICAgICAgIHRva2VuOiB0aGlzLmF1dGhUb2tlbiB8fCB1bmRlZmluZWQsXG4gICAgICB9O1xuICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICBsb2dnZXIuZXJyb3IoJ+azqOWGjOWksei0pTonLCBlcnJvcik7XG4gICAgICByZXR1cm4ge1xuICAgICAgICBzdWNjZXNzOiBmYWxzZSxcbiAgICAgICAgZXJyb3I6IGVycm9yIGluc3RhbmNlb2YgRXJyb3IgPyBlcnJvci5tZXNzYWdlIDogJ+e9kee7nOmUmeivrycsXG4gICAgICB9O1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiDnmbvlvZUgUG93UG93XG4gICAqL1xuICBwdWJsaWMgYXN5bmMgbG9naW5Vc2VyKHBhcmFtczoge1xuICAgIHVzZXJuYW1lOiBzdHJpbmc7XG4gICAgcGFzc3dvcmQ6IHN0cmluZztcbiAgfSk6IFByb21pc2U8e1xuICAgIHN1Y2Nlc3M6IGJvb2xlYW47XG4gICAgdXNlcj86IFBvd1Bvd1VzZXI7XG4gICAgdG9rZW4/OiBzdHJpbmc7XG4gICAgZXJyb3I/OiBzdHJpbmc7XG4gIH0+IHtcbiAgICBsb2dnZXIuaW5mbygn55m75b2VIFBvd1BvdzonLCBwYXJhbXMudXNlcm5hbWUpO1xuXG4gICAgY29uc3QgdXJsID0gYCR7dGhpcy5jb25maWcuYmFzZVVybH0ke0FQSV9FTkRQT0lOVFMuTE9HSU59YDtcblxuICAgIHRyeSB7XG4gICAgICBjb25zdCByZXNwb25zZSA9IGF3YWl0IGZldGNoKHVybCwge1xuICAgICAgICBtZXRob2Q6ICdQT1NUJyxcbiAgICAgICAgaGVhZGVyczogeyAnQ29udGVudC1UeXBlJzogJ2FwcGxpY2F0aW9uL2pzb24nIH0sXG4gICAgICAgIGJvZHk6IEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICB1c2VybmFtZTogcGFyYW1zLnVzZXJuYW1lLFxuICAgICAgICAgIHBhc3N3b3JkOiBwYXJhbXMucGFzc3dvcmQsXG4gICAgICAgIH0pLFxuICAgICAgfSk7XG5cbiAgICAgIGNvbnN0IGRhdGEgPSBhd2FpdCByZXNwb25zZS5qc29uKCk7XG5cbiAgICAgIGlmICghcmVzcG9uc2Uub2spIHtcbiAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICBzdWNjZXNzOiBmYWxzZSxcbiAgICAgICAgICBlcnJvcjogZGF0YS5lcnJvciB8fCAn55m75b2V5aSx6LSlJyxcbiAgICAgICAgfTtcbiAgICAgIH1cblxuICAgICAgaWYgKGRhdGEuc3VjY2VzcyAmJiBkYXRhLmRhdGEpIHtcbiAgICAgICAgdGhpcy5jdXJyZW50VXNlciA9IGRhdGEuZGF0YS51c2VyO1xuICAgICAgICB0aGlzLmF1dGhUb2tlbiA9IGRhdGEuZGF0YS50b2tlbjtcbiAgICAgICAgbG9nZ2VyLmluZm8oJ+eZu+W9leaIkOWKnzonLCB0aGlzLmN1cnJlbnRVc2VyPy51c2VybmFtZSk7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiB7XG4gICAgICAgIHN1Y2Nlc3M6IHRydWUsXG4gICAgICAgIHVzZXI6IHRoaXMuY3VycmVudFVzZXIgfHwgdW5kZWZpbmVkLFxuICAgICAgICB0b2tlbjogdGhpcy5hdXRoVG9rZW4gfHwgdW5kZWZpbmVkLFxuICAgICAgfTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgbG9nZ2VyLmVycm9yKCfnmbvlvZXlpLHotKU6JywgZXJyb3IpO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgIGVycm9yOiBlcnJvciBpbnN0YW5jZW9mIEVycm9yID8gZXJyb3IubWVzc2FnZSA6ICfnvZHnu5zplJnor68nLFxuICAgICAgfTtcbiAgICB9XG4gIH1cblxuICBwdWJsaWMgZ2V0Q3VycmVudFVzZXIoKTogUG93UG93VXNlciB8IG51bGwge1xuICAgIHJldHVybiB0aGlzLmN1cnJlbnRVc2VyO1xuICB9XG5cbiAgcHVibGljIGlzTG9nZ2VkSW4oKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuY3VycmVudFVzZXIgIT09IG51bGwgJiYgdGhpcy5hdXRoVG9rZW4gIT09IG51bGw7XG4gIH1cblxuICAvLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4gIC8vIOaVsOWtl+S6uueuoeeQhlxuICAvLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG5cbiAgLyoqXG4gICAqIOWIm+W7uuaVsOWtl+S6ulxuICAgKiBcbiAgICog566A5YyW54mI77ya5LiN6ZyA6KaBIHdlYmhvb2sgVVJM77yMUG93UG93IOWQjuerr+iHquWKqOWkhOeQhuWvueivnVxuICAgKi9cbiAgcHVibGljIGFzeW5jIGNyZWF0ZURpZ2l0YWxIdW1hbihwYXJhbXM6IERpZ2l0YWxIdW1hbkNyZWF0aW9uKTogUHJvbWlzZTx7XG4gICAgc3VjY2VzczogYm9vbGVhbjtcbiAgICBkaWdpdGFsSHVtYW4/OiBEaWdpdGFsSHVtYW47XG4gICAgZXJyb3I/OiBzdHJpbmc7XG4gIH0+IHtcbiAgICBpZiAoIXRoaXMuaXNMb2dnZWRJbigpKSB7XG4gICAgICByZXR1cm4ge1xuICAgICAgICBzdWNjZXNzOiBmYWxzZSxcbiAgICAgICAgZXJyb3I6ICfor7flhYjms6jlhozmiJbnmbvlvZUgUG93UG93IOi0puWPtycsXG4gICAgICB9O1xuICAgIH1cblxuICAgIGxvZ2dlci5pbmZvKCfliJvlu7rmlbDlrZfkuro6JywgcGFyYW1zLm5hbWUpO1xuXG4gICAgaWYgKCFwYXJhbXMubmFtZSB8fCBwYXJhbXMubmFtZS50cmltKCkubGVuZ3RoID09PSAwKSB7XG4gICAgICByZXR1cm4geyBzdWNjZXNzOiBmYWxzZSwgZXJyb3I6ICfmlbDlrZfkurrlkI3lrZfkuI3og73kuLrnqbonIH07XG4gICAgfVxuXG4gICAgaWYgKCFwYXJhbXMuZGVzY3JpcHRpb24gfHwgcGFyYW1zLmRlc2NyaXB0aW9uLnRyaW0oKS5sZW5ndGggPT09IDApIHtcbiAgICAgIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBlcnJvcjogJ+aVsOWtl+S6uuaPj+i/sC/kurrorr7kuI3og73kuLrnqbonIH07XG4gICAgfVxuXG4gICAgaWYgKHBhcmFtcy5sYXQgPT09IHVuZGVmaW5lZCB8fCBwYXJhbXMubG5nID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBlcnJvcjogJ+ivt+aPkOS+m+aVsOWtl+S6uuS9jee9ru+8iOe6rOW6puWSjOe7j+W6pu+8iScgfTtcbiAgICB9XG5cbiAgICBjb25zdCB1cmwgPSBgJHt0aGlzLmNvbmZpZy5iYXNlVXJsfSR7QVBJX0VORFBPSU5UUy5ESUdJVEFMX0hVTUFOU31gO1xuXG4gICAgdHJ5IHtcbiAgICAgIGNvbnN0IHJlc3BvbnNlID0gYXdhaXQgZmV0Y2godXJsLCB7XG4gICAgICAgIG1ldGhvZDogJ1BPU1QnLFxuICAgICAgICBoZWFkZXJzOiB0aGlzLmdldEhlYWRlcnMoKSxcbiAgICAgICAgYm9keTogSlNPTi5zdHJpbmdpZnkoe1xuICAgICAgICAgIG5hbWU6IHNhbml0aXplU3RyaW5nKHBhcmFtcy5uYW1lKSxcbiAgICAgICAgICBkZXNjcmlwdGlvbjogc2FuaXRpemVTdHJpbmcocGFyYW1zLmRlc2NyaXB0aW9uKSxcbiAgICAgICAgICBhdmF0YXJVcmw6IHBhcmFtcy5hdmF0YXJVcmwsXG4gICAgICAgICAgbGF0OiBwYXJhbXMubGF0LFxuICAgICAgICAgIGxuZzogcGFyYW1zLmxuZyxcbiAgICAgICAgICBsb2NhdGlvbk5hbWU6IHBhcmFtcy5sb2NhdGlvbk5hbWUsXG4gICAgICAgICAgdXNlcklkOiB0aGlzLmN1cnJlbnRVc2VyIS5pZCxcbiAgICAgICAgICAvLyDnroDljJbniYjvvJrkuI3pnIDopoEgd2ViaG9vayDphY3nva5cbiAgICAgICAgICAvLyBQb3dQb3cg5ZCO56uv5Lya6Ieq5Yqo5aSE55CG5a+56K+dXG4gICAgICAgIH0pLFxuICAgICAgfSk7XG5cbiAgICAgIGNvbnN0IGRhdGEgPSBhd2FpdCByZXNwb25zZS5qc29uKCk7XG5cbiAgICAgIGlmICghcmVzcG9uc2Uub2spIHtcbiAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICBzdWNjZXNzOiBmYWxzZSxcbiAgICAgICAgICBlcnJvcjogZGF0YS5lcnJvciB8fCBg5Yib5bu65aSx6LSlOiBIVFRQICR7cmVzcG9uc2Uuc3RhdHVzfWAsXG4gICAgICAgIH07XG4gICAgICB9XG5cbiAgICAgIGlmIChkYXRhLnN1Y2Nlc3MgJiYgZGF0YS5kYXRhKSB7XG4gICAgICAgIHRoaXMuY3VycmVudERpZ2l0YWxIdW1hbiA9IGRhdGEuZGF0YTtcbiAgICAgICAgbG9nZ2VyLmluZm8oJ+aVsOWtl+S6uuWIm+W7uuaIkOWKnzonLCB7XG4gICAgICAgICAgZGlnaXRhbEh1bWFuSWQ6IHRoaXMuY3VycmVudERpZ2l0YWxIdW1hbj8uaWQsXG4gICAgICAgICAgbmFtZTogdGhpcy5jdXJyZW50RGlnaXRhbEh1bWFuPy5uYW1lLFxuICAgICAgICB9KTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3VjY2VzczogdHJ1ZSxcbiAgICAgICAgZGlnaXRhbEh1bWFuOiB0aGlzLmN1cnJlbnREaWdpdGFsSHVtYW4gfHwgdW5kZWZpbmVkLFxuICAgICAgfTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgbG9nZ2VyLmVycm9yKCfliJvlu7rmlbDlrZfkurrlpLHotKU6JywgZXJyb3IpO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgIGVycm9yOiBlcnJvciBpbnN0YW5jZW9mIEVycm9yID8gZXJyb3IubWVzc2FnZSA6ICfnvZHnu5zplJnor68nLFxuICAgICAgfTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICog6I635Y+W5oiR55qE5pWw5a2X5Lq65YiX6KGoXG4gICAqL1xuICBwdWJsaWMgYXN5bmMgbGlzdE15RGlnaXRhbEh1bWFucygpOiBQcm9taXNlPHtcbiAgICBzdWNjZXNzOiBib29sZWFuO1xuICAgIGRpZ2l0YWxIdW1hbnM/OiBEaWdpdGFsSHVtYW5bXTtcbiAgICBlcnJvcj86IHN0cmluZztcbiAgfT4ge1xuICAgIGlmICghdGhpcy5pc0xvZ2dlZEluKCkpIHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHN1Y2Nlc3M6IGZhbHNlLFxuICAgICAgICBlcnJvcjogJ+ivt+WFiOeZu+W9lScsXG4gICAgICB9O1xuICAgIH1cblxuICAgIGNvbnN0IHVybCA9IGAke3RoaXMuY29uZmlnLmJhc2VVcmx9JHtBUElfRU5EUE9JTlRTLkRJR0lUQUxfSFVNQU5TfT91c2VySWQ9JHt0aGlzLmN1cnJlbnRVc2VyIS5pZH1gO1xuXG4gICAgdHJ5IHtcbiAgICAgIGNvbnN0IHJlc3BvbnNlID0gYXdhaXQgZmV0Y2godXJsLCB7XG4gICAgICAgIG1ldGhvZDogJ0dFVCcsXG4gICAgICAgIGhlYWRlcnM6IHRoaXMuZ2V0SGVhZGVycygpLFxuICAgICAgfSk7XG5cbiAgICAgIGNvbnN0IGRhdGEgPSBhd2FpdCByZXNwb25zZS5qc29uKCk7XG5cbiAgICAgIGlmICghcmVzcG9uc2Uub2spIHtcbiAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICBzdWNjZXNzOiBmYWxzZSxcbiAgICAgICAgICBlcnJvcjogZGF0YS5lcnJvciB8fCAn6I635Y+W5YiX6KGo5aSx6LSlJyxcbiAgICAgICAgfTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3VjY2VzczogdHJ1ZSxcbiAgICAgICAgZGlnaXRhbEh1bWFuczogZGF0YS5kYXRhIHx8IFtdLFxuICAgICAgfTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgbG9nZ2VyLmVycm9yKCfojrflj5bmlbDlrZfkurrliJfooajlpLHotKU6JywgZXJyb3IpO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgIGVycm9yOiBlcnJvciBpbnN0YW5jZW9mIEVycm9yID8gZXJyb3IubWVzc2FnZSA6ICfnvZHnu5zplJnor68nLFxuICAgICAgfTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICog6YCJ5oup6KaB5pON5L2c55qE5pWw5a2X5Lq6XG4gICAqL1xuICBwdWJsaWMgc2VsZWN0RGlnaXRhbEh1bWFuKGRpZ2l0YWxIdW1hbklkOiBzdHJpbmcpOiBib29sZWFuIHtcbiAgICB0aGlzLmN1cnJlbnREaWdpdGFsSHVtYW4gPSB7XG4gICAgICBpZDogZGlnaXRhbEh1bWFuSWQsXG4gICAgICB1c2VySWQ6IHRoaXMuY3VycmVudFVzZXI/LmlkIHx8ICcnLFxuICAgICAgbmFtZTogJycsXG4gICAgICBkZXNjcmlwdGlvbjogJycsXG4gICAgICBsYXQ6IDAsXG4gICAgICBsbmc6IDAsXG4gICAgICBpc0FjdGl2ZTogdHJ1ZSxcbiAgICB9O1xuICAgIGxvZ2dlci5pbmZvKCflt7LpgInmi6nmlbDlrZfkuro6JywgZGlnaXRhbEh1bWFuSWQpO1xuICAgIHJldHVybiB0cnVlO1xuICB9XG5cbiAgcHVibGljIGdldEN1cnJlbnREaWdpdGFsSHVtYW4oKTogRGlnaXRhbEh1bWFuIHwgbnVsbCB7XG4gICAgcmV0dXJuIHRoaXMuY3VycmVudERpZ2l0YWxIdW1hbjtcbiAgfVxuXG4gIC8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbiAgLy8g5a+56K+d5Yqf6IO977yI566A5YyW54mI77ya6YCa6L+HIFBvd1BvdyDlkI7nq6/vvIlcbiAgLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuXG4gIC8qKlxuICAgKiDlj5HpgIHmtojmga/nu5nmlbDlrZfkurpcbiAgICogXG4gICAqIOeugOWMlueJiO+8mlBvd1BvdyDlkI7nq6/kvJroh6rliqjosIPnlKggQUkgQVBJIOW5tui/lOWbnuWbnuWkjVxuICAgKi9cbiAgcHVibGljIGFzeW5jIHNlbmRNZXNzYWdlKGNvbnRlbnQ6IHN0cmluZyk6IFByb21pc2U8e1xuICAgIHN1Y2Nlc3M6IGJvb2xlYW47XG4gICAgcmVwbHk/OiBzdHJpbmc7XG4gICAgZXJyb3I/OiBzdHJpbmc7XG4gIH0+IHtcbiAgICBpZiAoIXRoaXMuY3VycmVudERpZ2l0YWxIdW1hbikge1xuICAgICAgcmV0dXJuIHsgc3VjY2VzczogZmFsc2UsIGVycm9yOiAn6K+35YWI6YCJ5oup5pWw5a2X5Lq6JyB9O1xuICAgIH1cblxuICAgIGNvbnN0IGNvbnRlbnRWYWxpZGF0aW9uID0gdmFsaWRhdGVNZXNzYWdlKGNvbnRlbnQpO1xuICAgIGlmICghY29udGVudFZhbGlkYXRpb24udmFsaWQpIHtcbiAgICAgIHJldHVybiB7IHN1Y2Nlc3M6IGZhbHNlLCBlcnJvcjogY29udGVudFZhbGlkYXRpb24uZXJyb3IgfTtcbiAgICB9XG5cbiAgICBjb25zdCBzYW5pdGl6ZWRDb250ZW50ID0gc2FuaXRpemVTdHJpbmcoY29udGVudCk7XG4gICAgY29uc3QgdXJsID0gYCR7dGhpcy5jb25maWcuYmFzZVVybH0ke0FQSV9FTkRQT0lOVFMuQ0hBVF9TRU5EfWA7XG5cbiAgICB0cnkge1xuICAgICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCBmZXRjaCh1cmwsIHtcbiAgICAgICAgbWV0aG9kOiAnUE9TVCcsXG4gICAgICAgIGhlYWRlcnM6IHRoaXMuZ2V0SGVhZGVycygpLFxuICAgICAgICBib2R5OiBKU09OLnN0cmluZ2lmeSh7XG4gICAgICAgICAgZGlnaXRhbEh1bWFuSWQ6IHRoaXMuY3VycmVudERpZ2l0YWxIdW1hbi5pZCxcbiAgICAgICAgICBtZXNzYWdlOiBzYW5pdGl6ZWRDb250ZW50LFxuICAgICAgICAgIHVzZXJJZDogdGhpcy5jdXJyZW50VXNlcj8uaWQsXG4gICAgICAgIH0pLFxuICAgICAgfSk7XG5cbiAgICAgIGNvbnN0IGRhdGEgPSBhd2FpdCByZXNwb25zZS5qc29uKCk7XG5cbiAgICAgIGlmICghcmVzcG9uc2Uub2sgfHwgIWRhdGEuc3VjY2Vzcykge1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIHN1Y2Nlc3M6IGZhbHNlLFxuICAgICAgICAgIGVycm9yOiBkYXRhLmVycm9yIHx8ICflj5HpgIHlpLHotKUnLFxuICAgICAgICB9O1xuICAgICAgfVxuXG4gICAgICBsb2dnZXIuaW5mbygn5raI5oGv5bey5Y+R6YCBJyk7XG4gICAgICByZXR1cm4ge1xuICAgICAgICBzdWNjZXNzOiB0cnVlLFxuICAgICAgICByZXBseTogZGF0YS5yZXBseSB8fCBkYXRhLmRhdGE/LnJlcGx5LFxuICAgICAgfTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgbG9nZ2VyLmVycm9yKCflj5HpgIHmtojmga/lpLHotKU6JywgZXJyb3IpO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgIGVycm9yOiBlcnJvciBpbnN0YW5jZW9mIEVycm9yID8gZXJyb3IubWVzc2FnZSA6ICfnvZHnu5zplJnor68nLFxuICAgICAgfTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICog6I635Y+W6IGK5aSp5Y6G5Y+yXG4gICAqL1xuICBwdWJsaWMgYXN5bmMgZ2V0Q2hhdEhpc3RvcnkoKTogUHJvbWlzZTx7XG4gICAgc3VjY2VzczogYm9vbGVhbjtcbiAgICBtZXNzYWdlcz86IENoYXRNZXNzYWdlW107XG4gICAgZXJyb3I/OiBzdHJpbmc7XG4gIH0+IHtcbiAgICBpZiAoIXRoaXMuY3VycmVudERpZ2l0YWxIdW1hbikge1xuICAgICAgcmV0dXJuIHsgc3VjY2VzczogZmFsc2UsIGVycm9yOiAn6K+35YWI6YCJ5oup5pWw5a2X5Lq6JyB9O1xuICAgIH1cblxuICAgIGNvbnN0IHVybCA9IGAke3RoaXMuY29uZmlnLmJhc2VVcmx9JHtBUElfRU5EUE9JTlRTLkNIQVRfSElTVE9SWX0/ZGlnaXRhbEh1bWFuSWQ9JHt0aGlzLmN1cnJlbnREaWdpdGFsSHVtYW4uaWR9JnVzZXJJZD0ke3RoaXMuY3VycmVudFVzZXI/LmlkfWA7XG5cbiAgICB0cnkge1xuICAgICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCBmZXRjaCh1cmwsIHtcbiAgICAgICAgbWV0aG9kOiAnR0VUJyxcbiAgICAgICAgaGVhZGVyczogdGhpcy5nZXRIZWFkZXJzKCksXG4gICAgICB9KTtcblxuICAgICAgY29uc3QgZGF0YSA9IGF3YWl0IHJlc3BvbnNlLmpzb24oKTtcblxuICAgICAgaWYgKCFyZXNwb25zZS5vaykge1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIHN1Y2Nlc3M6IGZhbHNlLFxuICAgICAgICAgIGVycm9yOiBkYXRhLmVycm9yIHx8ICfojrflj5bljoblj7LlpLHotKUnLFxuICAgICAgICB9O1xuICAgICAgfVxuXG4gICAgICByZXR1cm4ge1xuICAgICAgICBzdWNjZXNzOiB0cnVlLFxuICAgICAgICBtZXNzYWdlczogZGF0YS5kYXRhPy5tZXNzYWdlcyB8fCBbXSxcbiAgICAgIH07XG4gICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgIGxvZ2dlci5lcnJvcign6I635Y+W6IGK5aSp5Y6G5Y+y5aSx6LSlOicsIGVycm9yKTtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHN1Y2Nlc3M6IGZhbHNlLFxuICAgICAgICBlcnJvcjogZXJyb3IgaW5zdGFuY2VvZiBFcnJvciA/IGVycm9yLm1lc3NhZ2UgOiAn572R57uc6ZSZ6K+vJyxcbiAgICAgIH07XG4gICAgfVxuICB9XG5cbiAgLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuICAvLyDnirbmgIHnrqHnkIZcbiAgLy8gPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PVxuXG4gIHB1YmxpYyBnZXRTdGF0dXMoKToge1xuICAgIGlzTG9nZ2VkSW46IGJvb2xlYW47XG4gICAgdXNlcjogUG93UG93VXNlciB8IG51bGw7XG4gICAgZGlnaXRhbEh1bWFuOiBEaWdpdGFsSHVtYW4gfCBudWxsO1xuICB9IHtcbiAgICByZXR1cm4ge1xuICAgICAgaXNMb2dnZWRJbjogdGhpcy5pc0xvZ2dlZEluKCksXG4gICAgICB1c2VyOiB0aGlzLmN1cnJlbnRVc2VyLFxuICAgICAgZGlnaXRhbEh1bWFuOiB0aGlzLmN1cnJlbnREaWdpdGFsSHVtYW4sXG4gICAgfTtcbiAgfVxufVxuXG4vLyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09XG4vLyBPcGVuQ2xhdyBTa2lsbCBQbHVnaW5cbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuaW50ZXJmYWNlIE9wZW5DbGF3Q29udGV4dCB7XG4gIHVzZXJJZDogc3RyaW5nO1xuICBjb25maWc6IGFueTtcbiAgcG93cG93U2tpbGw/OiBQb3dQb3dTa2lsbDtcbiAgZW1pdDogKGV2ZW50OiBzdHJpbmcsIGRhdGE6IGFueSkgPT4gdm9pZDtcbn1cblxuY29uc3QgcG93cG93U2tpbGxQbHVnaW4gPSB7XG4gIG5hbWU6ICdwb3dwb3ctaW50ZWdyYXRpb24nLFxuICB2ZXJzaW9uOiAnNC4wLjAnLFxuICBkZXNjcmlwdGlvbjogJ1BPV1BPVyDnroDljJbniYjpm4bmiJAgLSDnlKjmiLfms6jlhozjgIHmlbDlrZfkurrliJvlu7rjgIHoh6rliqjlr7nor50nLFxuXG4gIGluaXQoY29udGV4dDogYW55KTogdm9pZCB7XG4gICAgbG9nZ2VyLmluZm8oJ1Bvd1BvdyBQbHVnaW4g5Yid5aeL5YyW77yI566A5YyW54mI77yJJyk7XG4gICAgY29udGV4dC5wb3dwb3dDb25maWcgPSB7XG4gICAgICBiYXNlVXJsOiBBUElfQ09ORklHLkRFRkFVTFRfVVJMLFxuICAgIH07XG4gIH0sXG5cbiAgZGVzdHJveSgpOiB2b2lkIHtcbiAgICBsb2dnZXIuaW5mbygnUG93UG93IFBsdWdpbiDplIDmr4EnKTtcbiAgfSxcblxuICBjb21tYW5kczoge1xuICAgIC8qKlxuICAgICAqIOazqOWGjCBQb3dQb3cg6LSm5Y+3XG4gICAgICovXG4gICAgYXN5bmMgcmVnaXN0ZXIoXG4gICAgICBwYXJhbXM6IHsgdXNlcm5hbWU6IHN0cmluZzsgZW1haWw6IHN0cmluZzsgcGFzc3dvcmQ6IHN0cmluZyB9LFxuICAgICAgY29udGV4dDogT3BlbkNsYXdDb250ZXh0XG4gICAgKSB7XG4gICAgICB0cnkge1xuICAgICAgICBjb25zdCBza2lsbCA9IGNvbnRleHQucG93cG93U2tpbGwgfHwgbmV3IFBvd1Bvd1NraWxsKCk7XG4gICAgICAgIGNvbnRleHQucG93cG93U2tpbGwgPSBza2lsbDtcblxuICAgICAgICBjb25zdCByZXN1bHQgPSBhd2FpdCBza2lsbC5yZWdpc3RlclVzZXIoe1xuICAgICAgICAgIHVzZXJuYW1lOiBwYXJhbXMudXNlcm5hbWUsXG4gICAgICAgICAgZW1haWw6IHBhcmFtcy5lbWFpbCxcbiAgICAgICAgICBwYXNzd29yZDogcGFyYW1zLnBhc3N3b3JkLFxuICAgICAgICB9KTtcblxuICAgICAgICBpZiAocmVzdWx0LnN1Y2Nlc3MpIHtcbiAgICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgc3VjY2VzczogdHJ1ZSxcbiAgICAgICAgICAgIG1lc3NhZ2U6IGDms6jlhozmiJDlip/vvIHnlKjmiLflkI06ICR7cmVzdWx0LnVzZXI/LnVzZXJuYW1lfWAsXG4gICAgICAgICAgICB1c2VyOiByZXN1bHQudXNlcixcbiAgICAgICAgICAgIGhpbnQ6ICfkuIvkuIDmraXvvJrkvb/nlKggY3JlYXRlRGlnaXRhbEh1bWFuIOWIm+W7uuS9oOeahOaVsOWtl+S6uicsXG4gICAgICAgICAgfTtcbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiByZXN1bHQ7XG4gICAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgICBsb2dnZXIuZXJyb3IoJ+azqOWGjOWRveS7pOWksei0pTonLCBlcnJvcik7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgICAgZXJyb3I6IGVycm9yIGluc3RhbmNlb2YgRXJyb3IgPyBlcnJvci5tZXNzYWdlIDogJ+acquefpemUmeivrycsXG4gICAgICAgIH07XG4gICAgICB9XG4gICAgfSxcblxuICAgIC8qKlxuICAgICAqIOeZu+W9lSBQb3dQb3dcbiAgICAgKi9cbiAgICBhc3luYyBsb2dpbihcbiAgICAgIHBhcmFtczogeyB1c2VybmFtZTogc3RyaW5nOyBwYXNzd29yZDogc3RyaW5nIH0sXG4gICAgICBjb250ZXh0OiBPcGVuQ2xhd0NvbnRleHRcbiAgICApIHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGNvbnN0IHNraWxsID0gY29udGV4dC5wb3dwb3dTa2lsbCB8fCBuZXcgUG93UG93U2tpbGwoKTtcbiAgICAgICAgY29udGV4dC5wb3dwb3dTa2lsbCA9IHNraWxsO1xuXG4gICAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IHNraWxsLmxvZ2luVXNlcihwYXJhbXMpO1xuXG4gICAgICAgIGlmIChyZXN1bHQuc3VjY2Vzcykge1xuICAgICAgICAgIHJldHVybiB7XG4gICAgICAgICAgICBzdWNjZXNzOiB0cnVlLFxuICAgICAgICAgICAgbWVzc2FnZTogYOeZu+W9leaIkOWKn++8geasoui/juWbnuadpe+8jCR7cmVzdWx0LnVzZXI/LnVzZXJuYW1lfWAsXG4gICAgICAgICAgICB1c2VyOiByZXN1bHQudXNlcixcbiAgICAgICAgICB9O1xuICAgICAgICB9XG5cbiAgICAgICAgcmV0dXJuIHJlc3VsdDtcbiAgICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICAgIGxvZ2dlci5lcnJvcign55m75b2V5ZG95Luk5aSx6LSlOicsIGVycm9yKTtcbiAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICBzdWNjZXNzOiBmYWxzZSxcbiAgICAgICAgICBlcnJvcjogZXJyb3IgaW5zdGFuY2VvZiBFcnJvciA/IGVycm9yLm1lc3NhZ2UgOiAn5pyq55+l6ZSZ6K+vJyxcbiAgICAgICAgfTtcbiAgICAgIH1cbiAgICB9LFxuXG4gICAgLyoqXG4gICAgICog5Yib5bu65pWw5a2X5Lq6XG4gICAgICovXG4gICAgYXN5bmMgY3JlYXRlRGlnaXRhbEh1bWFuKFxuICAgICAgcGFyYW1zOiB7XG4gICAgICAgIG5hbWU6IHN0cmluZztcbiAgICAgICAgZGVzY3JpcHRpb246IHN0cmluZztcbiAgICAgICAgYXZhdGFyVXJsPzogc3RyaW5nO1xuICAgICAgICBsYXQ/OiBudW1iZXI7XG4gICAgICAgIGxuZz86IG51bWJlcjtcbiAgICAgICAgbG9jYXRpb25OYW1lPzogc3RyaW5nO1xuICAgICAgfSxcbiAgICAgIGNvbnRleHQ6IE9wZW5DbGF3Q29udGV4dFxuICAgICkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgY29uc3Qgc2tpbGwgPSBjb250ZXh0LnBvd3Bvd1NraWxsO1xuICAgICAgICBpZiAoIXNraWxsIHx8ICFza2lsbC5pc0xvZ2dlZEluKCkpIHtcbiAgICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgICAgICBlcnJvcjogJ+ivt+WFiOS9v+eUqCByZWdpc3RlciDlkb3ku6Tms6jlhowgUG93UG93IOi0puWPtycsXG4gICAgICAgICAgfTtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGxhdCA9IHBhcmFtcy5sYXQgPz8gMzkuOTA0MjtcbiAgICAgICAgY29uc3QgbG5nID0gcGFyYW1zLmxuZyA/PyAxMTYuNDA3NDtcblxuICAgICAgICBjb25zdCByZXN1bHQgPSBhd2FpdCBza2lsbC5jcmVhdGVEaWdpdGFsSHVtYW4oe1xuICAgICAgICAgIG5hbWU6IHBhcmFtcy5uYW1lLFxuICAgICAgICAgIGRlc2NyaXB0aW9uOiBwYXJhbXMuZGVzY3JpcHRpb24sXG4gICAgICAgICAgYXZhdGFyVXJsOiBwYXJhbXMuYXZhdGFyVXJsLFxuICAgICAgICAgIGxhdCxcbiAgICAgICAgICBsbmcsXG4gICAgICAgICAgbG9jYXRpb25OYW1lOiBwYXJhbXMubG9jYXRpb25OYW1lIHx8ICfljJfkuqwnLFxuICAgICAgICB9KTtcblxuICAgICAgICBpZiAocmVzdWx0LnN1Y2Nlc3MpIHtcbiAgICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgc3VjY2VzczogdHJ1ZSxcbiAgICAgICAgICAgIG1lc3NhZ2U6IGDmlbDlrZfkurogXCIke3BhcmFtcy5uYW1lfVwiIOWIm+W7uuaIkOWKn++8geW3sue7keWumuWIsOS9oOeahOi0puWPt2AsXG4gICAgICAgICAgICBkaWdpdGFsSHVtYW46IHJlc3VsdC5kaWdpdGFsSHVtYW4sXG4gICAgICAgICAgICBoaW50OiAn5pWw5a2X5Lq65bey5Ye6546w5Zyo5Zyw5Zu+5LiK77yM6K6/6ZeuIGh0dHBzOi8vZ2xvYmFsLnBvd3Bvdy5vbmxpbmUvbWFwIOafpeeciycsXG4gICAgICAgICAgfTtcbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiByZXN1bHQ7XG4gICAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgICBsb2dnZXIuZXJyb3IoJ+WIm+W7uuaVsOWtl+S6uuWRveS7pOWksei0pTonLCBlcnJvcik7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgICAgZXJyb3I6IGVycm9yIGluc3RhbmNlb2YgRXJyb3IgPyBlcnJvci5tZXNzYWdlIDogJ+acquefpemUmeivrycsXG4gICAgICAgIH07XG4gICAgICB9XG4gICAgfSxcblxuICAgIC8qKlxuICAgICAqIOWIl+WHuuaIkeeahOaVsOWtl+S6ulxuICAgICAqL1xuICAgIGFzeW5jIGxpc3REaWdpdGFsSHVtYW5zKHBhcmFtczoge30sIGNvbnRleHQ6IE9wZW5DbGF3Q29udGV4dCkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgY29uc3Qgc2tpbGwgPSBjb250ZXh0LnBvd3Bvd1NraWxsO1xuICAgICAgICBpZiAoIXNraWxsIHx8ICFza2lsbC5pc0xvZ2dlZEluKCkpIHtcbiAgICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgICAgICBlcnJvcjogJ+ivt+WFiOeZu+W9lScsXG4gICAgICAgICAgfTtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IHNraWxsLmxpc3RNeURpZ2l0YWxIdW1hbnMoKTtcbiAgICAgICAgcmV0dXJuIHJlc3VsdDtcbiAgICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICAgIGxvZ2dlci5lcnJvcign5YiX5Ye65pWw5a2X5Lq65ZG95Luk5aSx6LSlOicsIGVycm9yKTtcbiAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICBzdWNjZXNzOiBmYWxzZSxcbiAgICAgICAgICBlcnJvcjogZXJyb3IgaW5zdGFuY2VvZiBFcnJvciA/IGVycm9yLm1lc3NhZ2UgOiAn5pyq55+l6ZSZ6K+vJyxcbiAgICAgICAgfTtcbiAgICAgIH1cbiAgICB9LFxuXG4gICAgLyoqXG4gICAgICog6YCJ5oup5pWw5a2X5Lq6XG4gICAgICovXG4gICAgc2VsZWN0RGlnaXRhbEh1bWFuKFxuICAgICAgcGFyYW1zOiB7IGRpZ2l0YWxIdW1hbklkOiBzdHJpbmcgfSxcbiAgICAgIGNvbnRleHQ6IE9wZW5DbGF3Q29udGV4dFxuICAgICkge1xuICAgICAgY29uc3Qgc2tpbGwgPSBjb250ZXh0LnBvd3Bvd1NraWxsO1xuICAgICAgaWYgKCFza2lsbCB8fCAhc2tpbGwuaXNMb2dnZWRJbigpKSB7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICAgICAgZXJyb3I6ICfor7flhYjnmbvlvZUnLFxuICAgICAgICB9O1xuICAgICAgfVxuXG4gICAgICBza2lsbC5zZWxlY3REaWdpdGFsSHVtYW4ocGFyYW1zLmRpZ2l0YWxIdW1hbklkKTtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHN1Y2Nlc3M6IHRydWUsXG4gICAgICAgIG1lc3NhZ2U6ICflt7LpgInmi6nmlbDlrZfkuronLFxuICAgICAgICBkaWdpdGFsSHVtYW5JZDogcGFyYW1zLmRpZ2l0YWxIdW1hbklkLFxuICAgICAgfTtcbiAgICB9LFxuXG4gICAgLyoqXG4gICAgICog5Y+R6YCB5raI5oGv57uZ5pWw5a2X5Lq6XG4gICAgICovXG4gICAgYXN5bmMgc2VuZChwYXJhbXM6IHsgbWVzc2FnZTogc3RyaW5nIH0sIGNvbnRleHQ6IE9wZW5DbGF3Q29udGV4dCkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgY29uc3Qgc2tpbGwgPSBjb250ZXh0LnBvd3Bvd1NraWxsO1xuICAgICAgICBpZiAoIXNraWxsKSB7XG4gICAgICAgICAgcmV0dXJuIHsgc3VjY2VzczogZmFsc2UsIGVycm9yOiAn6K+35YWI5rOo5YaM5bm26YCJ5oup5pWw5a2X5Lq6JyB9O1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgcmVzdWx0ID0gYXdhaXQgc2tpbGwuc2VuZE1lc3NhZ2UocGFyYW1zLm1lc3NhZ2UpO1xuICAgICAgICByZXR1cm4gcmVzdWx0O1xuICAgICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgICAgbG9nZ2VyLmVycm9yKCflj5HpgIHlkb3ku6TlpLHotKU6JywgZXJyb3IpO1xuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIHN1Y2Nlc3M6IGZhbHNlLFxuICAgICAgICAgIGVycm9yOiBlcnJvciBpbnN0YW5jZW9mIEVycm9yID8gZXJyb3IubWVzc2FnZSA6ICfmnKrnn6XplJnor68nLFxuICAgICAgICB9O1xuICAgICAgfVxuICAgIH0sXG5cbiAgICAvKipcbiAgICAgKiDmn6XnnIvnirbmgIFcbiAgICAgKi9cbiAgICBzdGF0dXMocGFyYW1zOiB7fSwgY29udGV4dDogT3BlbkNsYXdDb250ZXh0KSB7XG4gICAgICBjb25zdCBza2lsbCA9IGNvbnRleHQucG93cG93U2tpbGw7XG4gICAgICBpZiAoIXNraWxsKSB7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgc3VjY2VzczogdHJ1ZSxcbiAgICAgICAgICBzdGF0dXM6ICfmnKrliJ3lp4vljJYnLFxuICAgICAgICAgIG1lc3NhZ2U6ICfor7fkvb/nlKggcmVnaXN0ZXIg5ZG95Luk5rOo5YaMIFBvd1BvdyDotKblj7cnLFxuICAgICAgICB9O1xuICAgICAgfVxuXG4gICAgICBjb25zdCBzdGF0dXMgPSBza2lsbC5nZXRTdGF0dXMoKTtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHN1Y2Nlc3M6IHRydWUsXG4gICAgICAgIC4uLnN0YXR1cyxcbiAgICAgIH07XG4gICAgfSxcbiAgfSxcbn07XG5cbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cbi8vIEV4cG9ydHNcbi8vID09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT1cblxuZXhwb3J0IHsgUG93UG93U2tpbGwsIHBvd3Bvd1NraWxsUGx1Z2luLCBsb2dnZXIgfTtcbmV4cG9ydCBkZWZhdWx0IHBvd3Bvd1NraWxsUGx1Z2luO1xuIl19