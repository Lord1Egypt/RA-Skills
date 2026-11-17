/**
 * 凭据仓库实现
 * 从配置文件读取凭据（密码或密钥）
 *
 * 注意：为安全起见，密码建议存储在系统密钥环（如 macOS Keychain、Linux Secret Service）
 * 或环境变量中。本实现从配置文件读取（生产环境不推荐）。
 */
import type { Server, SSHCredentials, ICredentialsProvider } from '../../config/schemas';
import { ConfigManager } from '../../config/loader';
/**
 * 基于 ConfigManager 的凭据提供者
 *
 * 凭据存储方案（按优先级）：
 * 1. 环境变量: OPS_CRED_<HOST>={user:password} 或 OPS_CRED_<HOST>_KEY 文件路径
 * 2. 配置文件附加字段（不推荐生产使用）
 * 3. SSH 默认密钥 (~/.ssh/id_rsa)
 */
export declare class ConfigManagerCredentialsProvider implements ICredentialsProvider {
    private configManager;
    constructor(configManager: ConfigManager);
    /**
     * 获取服务器凭据
     */
    getCredentials(server: Server): Promise<SSHCredentials | null>;
    /**
     * 从环境变量读取凭据
     *
     * 格式：
     * - OPS_CRED_<HOST>="username:password" 或 OPS_CRED_<HOST>="password"
     * - OPS_KEY_<HOST>=/path/to/private/key
     *
     * 示例：
     * - OPS_CRED_10_119_120_143="salt:Giten!#202501Tab*&"
     * - OPS_KEY_10_119_120_143=/home/user/.ssh/id_rsa
     */
    private getFromEnvironment;
    /**
     * 从配置文件获取凭据（扩展方案）
     *
     * 服务器配置文件扩展格式：
     * {
     *   "host": "10.119.120.143",
     *   "user": "salt",
     *   "password": "xxxxx",  // 密码（生产环境不推荐）
     *   "keyFile": "/path/to/key", // 密钥路径
     *   "keyContent": "-----BEGIN...", // 密钥内容（base64）
     *   "name": "...",
     *   "tags": [...]
     * }
     */
    private getFromConfigFile;
    /**
     * 获取默认 SSH 密钥路径
     */
    private getDefaultSSHKey;
    /**
     * 保存凭据（运行时添加）
     */
    setCredentials(server: Server, credentials: SSHCredentials): Promise<void>;
}
/**
 * 环境变量凭据提供者（最安全）
 * 所有凭据通过环境变量注入，不存储在文件中
 */
export declare class EnvironmentCredentialsProvider implements ICredentialsProvider {
    getCredentials(server: Server): Promise<SSHCredentials | null>;
    setCredentials(server: Server, credentials: SSHCredentials): Promise<void>;
    private getFromEnvironment;
}
//# sourceMappingURL=CredentialsRepository.d.ts.map