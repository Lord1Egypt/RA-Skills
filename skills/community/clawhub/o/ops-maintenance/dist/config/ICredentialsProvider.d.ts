/**
 * 凭据提供者接口
 * 为 SSH 连接提供密码或密钥
 */
import type { Server } from './schemas';
/**
 * SSH 凭据
 */
export interface SSHCredentials {
    /** 密码（如果使用密码认证） */
    password?: string;
    /** 私钥文件路径（如果使用密钥认证） */
    keyFile?: string;
    /** 私钥内容（可选，直接提供密钥内容） */
    keyContent?: string;
}
/**
 * 凭据提供者接口
 */
export interface ICredentialsProvider {
    /**
     * 获取服务器的 SSH 凭据
     */
    getCredentials(server: Server): Promise<SSHCredentials | null>;
    /**
     * 更新或存储服务器的凭据
     */
    setCredentials(server: Server, credentials: SSHCredentials): Promise<void>;
}
//# sourceMappingURL=ICredentialsProvider.d.ts.map