/**
 * 密码过期检查用例
 */
import type { PasswordUserInfo, IServerRepository, ISSHClient } from '../config/schemas';
/**
 * 密码检查结果
 */
export interface PasswordCheckResult {
    server: string;
    status: 'ok' | 'warning' | 'critical';
    details: string;
    users: PasswordUserInfo[];
}
/**
 * 密码过期检查用例
 */
export declare class PasswordCheckUseCase {
    private serverRepo;
    private ssh;
    constructor(serverRepo: IServerRepository, ssh: ISSHClient);
    /**
     * 执行密码过期检查
     */
    execute(tags?: string[]): Promise<PasswordCheckResult[]>;
    /**
     * 检查单台服务器的密码
     */
    private checkServerPasswords;
    /**
     * 获取单个用户的密码信息
     */
    private getUserPasswordInfo;
    /**
     * 从 chage 输出中提取值
     */
    private extractValue;
    /**
     * 评估服务器整体状态
     */
    private evaluateServerStatus;
    /**
     * 解析服务器列表
     */
    private resolveServers;
}
//# sourceMappingURL=PasswordCheckUseCase.d.ts.map