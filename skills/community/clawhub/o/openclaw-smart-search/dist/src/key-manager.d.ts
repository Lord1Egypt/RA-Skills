/**
 * 加密 Key 管理器
 * 使用 AES-256-GCM 加密存储 API Keys
 */
import { SecretConfig } from './types';
export declare class SecretManager {
    private readonly keyFile;
    private masterKey;
    private configCache;
    constructor();
    /**
     * 初始化主密钥（使用存储的随机盐）
     *
     * 安全要求：
     * - 主密钥必须通过环境变量 OPENCLAW_MASTER_KEY 提供
     * - 盐值随机生成并存储在配置文件中
     * - 不使用硬编码默认值，防止意外暴露
     * - 生产环境必须设置此环境变量
     *
     * @throws Error 如果 OPENCLAW_MASTER_KEY 未设置
     */
    private initMasterKey;
    private _currentSalt;
    /**
     * 派生主密钥（PBKDF2）- 同步版本，用于向后兼容
     *
     * @deprecated 使用 initMasterKey() 替代
     * @throws Error 如果 OPENCLAW_MASTER_KEY 未设置
     */
    private deriveMasterKey;
    /**
     * 读取并解密配置
     */
    readConfig(): Promise<SecretConfig>;
    /**
     * 写入加密配置
     */
    writeConfig(config: SecretConfig): Promise<void>;
    /**
     * 初始化配置（首次使用）
     */
    initConfig(apiKeys: Record<string, string>): Promise<void>;
    /**
     * 获取单个引擎的 Key
     */
    getEngineKey(engine: string): Promise<string>;
    /**
     * 设置单个引擎的 Key
     */
    setEngineKey(engine: string, apiKey: string): Promise<void>;
    /**
     * 轮换 Key
     */
    rotateKey(engine: string, newApiKey?: string): Promise<void>;
    /**
     * 列出所有引擎
     */
    listEngines(): Promise<void>;
    /**
     * 显示详细状态
     */
    showStatus(): Promise<void>;
    /**
     * 记录访问日志
     */
    private logAccess;
    /**
     * 获取配置文件路径
     */
    getKeyFilePath(): string;
    /**
     * 检查配置是否存在
     */
    configExists(): boolean;
    /**
     * 清除缓存
     */
    clearCache(): void;
}
//# sourceMappingURL=key-manager.d.ts.map