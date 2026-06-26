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
import { EventEmitter } from 'events';
import { logger } from './utils/logger';
interface PowPowConfig {
    baseUrl: string;
}
interface UserRegistration {
    username: string;
    email: string;
    password: string;
}
interface DigitalHumanCreation {
    name: string;
    description: string;
    avatarUrl?: string;
    lat: number;
    lng: number;
    locationName?: string;
}
interface ChatMessage {
    id?: string;
    digitalHumanId: string;
    senderType: 'user' | 'assistant';
    senderId: string;
    content: string;
    timestamp?: string;
}
interface PowPowUser {
    id: string;
    username: string;
    email: string;
    badges?: number;
    createdAt?: string;
}
interface DigitalHuman {
    id: string;
    userId: string;
    name: string;
    description: string;
    avatarUrl?: string;
    lat: number;
    lng: number;
    locationName?: string;
    isActive: boolean;
    expiresAt?: string;
    createdAt?: string;
}
declare class PowPowSkill extends EventEmitter {
    private config;
    private currentUser;
    private authToken;
    private currentDigitalHuman;
    constructor(config?: PowPowConfig);
    private getHeaders;
    /**
     * 注册 PowPow 账号
     */
    registerUser(params: UserRegistration): Promise<{
        success: boolean;
        user?: PowPowUser;
        token?: string;
        error?: string;
    }>;
    /**
     * 登录 PowPow
     */
    loginUser(params: {
        username: string;
        password: string;
    }): Promise<{
        success: boolean;
        user?: PowPowUser;
        token?: string;
        error?: string;
    }>;
    getCurrentUser(): PowPowUser | null;
    isLoggedIn(): boolean;
    /**
     * 创建数字人
     *
     * 简化版：不需要 webhook URL，PowPow 后端自动处理对话
     */
    createDigitalHuman(params: DigitalHumanCreation): Promise<{
        success: boolean;
        digitalHuman?: DigitalHuman;
        error?: string;
    }>;
    /**
     * 获取我的数字人列表
     */
    listMyDigitalHumans(): Promise<{
        success: boolean;
        digitalHumans?: DigitalHuman[];
        error?: string;
    }>;
    /**
     * 选择要操作的数字人
     */
    selectDigitalHuman(digitalHumanId: string): boolean;
    getCurrentDigitalHuman(): DigitalHuman | null;
    /**
     * 发送消息给数字人
     *
     * 简化版：PowPow 后端会自动调用 AI API 并返回回复
     */
    sendMessage(content: string): Promise<{
        success: boolean;
        reply?: string;
        error?: string;
    }>;
    /**
     * 获取聊天历史
     */
    getChatHistory(): Promise<{
        success: boolean;
        messages?: ChatMessage[];
        error?: string;
    }>;
    getStatus(): {
        isLoggedIn: boolean;
        user: PowPowUser | null;
        digitalHuman: DigitalHuman | null;
    };
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
         * 注册 PowPow 账号
         */
        register(params: {
            username: string;
            email: string;
            password: string;
        }, context: OpenClawContext): Promise<{
            success: boolean;
            user?: PowPowUser;
            token?: string;
            error?: string;
        } | {
            success: boolean;
            message: string;
            user: PowPowUser | undefined;
            hint: string;
        }>;
        /**
         * 登录 PowPow
         */
        login(params: {
            username: string;
            password: string;
        }, context: OpenClawContext): Promise<{
            success: boolean;
            user?: PowPowUser;
            token?: string;
            error?: string;
        } | {
            success: boolean;
            message: string;
            user: PowPowUser | undefined;
        }>;
        /**
         * 创建数字人
         */
        createDigitalHuman(params: {
            name: string;
            description: string;
            avatarUrl?: string;
            lat?: number;
            lng?: number;
            locationName?: string;
        }, context: OpenClawContext): Promise<{
            success: boolean;
            digitalHuman?: DigitalHuman;
            error?: string;
        } | {
            success: boolean;
            message: string;
            digitalHuman: DigitalHuman | undefined;
            hint: string;
        }>;
        /**
         * 列出我的数字人
         */
        listDigitalHumans(params: {}, context: OpenClawContext): Promise<{
            success: boolean;
            digitalHumans?: DigitalHuman[];
            error?: string;
        }>;
        /**
         * 选择数字人
         */
        selectDigitalHuman(params: {
            digitalHumanId: string;
        }, context: OpenClawContext): {
            success: boolean;
            error: string;
            message?: undefined;
            digitalHumanId?: undefined;
        } | {
            success: boolean;
            message: string;
            digitalHumanId: string;
            error?: undefined;
        };
        /**
         * 发送消息给数字人
         */
        send(params: {
            message: string;
        }, context: OpenClawContext): Promise<{
            success: boolean;
            reply?: string;
            error?: string;
        }>;
        /**
         * 查看状态
         */
        status(params: {}, context: OpenClawContext): {
            success: boolean;
            status: string;
            message: string;
        } | {
            isLoggedIn: boolean;
            user: PowPowUser | null;
            digitalHuman: DigitalHuman | null;
            success: boolean;
            status?: undefined;
            message?: undefined;
        };
    };
};
export { PowPowSkill, powpowSkillPlugin, logger };
export default powpowSkillPlugin;
