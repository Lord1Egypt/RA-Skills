"use strict";
/**
 * 加密 Key 管理器
 * 使用 AES-256-GCM 加密存储 API Keys
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.SecretManager = void 0;
const crypto = __importStar(require("crypto"));
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const os = __importStar(require("os"));
const types_1 = require("./types");
class SecretManager {
    constructor() {
        this.masterKey = null;
        this.configCache = null;
        // 临时存储当前盐值
        this._currentSalt = null;
        this.keyFile = path.join(os.homedir(), '.openclaw', 'secrets', 'smart-search.json.enc');
        // 主密钥延迟初始化，在首次使用时从配置文件读取盐值
    }
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
    async initMasterKey() {
        if (this.masterKey) {
            return; // 已经初始化
        }
        const masterKeyStr = process.env.OPENCLAW_MASTER_KEY;
        if (!masterKeyStr) {
            throw new Error('OPENCLAW_MASTER_KEY environment variable is required.\n' +
                'Please set it in your environment:\n' +
                '  export OPENCLAW_MASTER_KEY="your-secure-master-key"\n' +
                'Or add it to your .env file.\n' +
                'See .env.example for details.');
        }
        // 密钥最小长度检查（至少 32 字符）
        if (masterKeyStr.length < 32) {
            throw new Error('OPENCLAW_MASTER_KEY must be at least 32 characters long for security.\n' +
                `Current length: ${masterKeyStr.length} characters.`);
        }
        // 读取存储的盐值
        let salt;
        try {
            const encryptedData = fs.readFileSync(this.keyFile, 'utf8');
            const data = JSON.parse(encryptedData);
            if (!data.salt) {
                throw new Error('Salt not found in config file. Config may be corrupted.');
            }
            salt = Buffer.from(data.salt, 'hex');
        }
        catch (error) {
            if (error.code === 'ENOENT') {
                // 配置文件不存在，生成新的随机盐（将在 writeConfig 时存储）
                salt = crypto.randomBytes(16);
            }
            else {
                throw error;
            }
        }
        // 派生主密钥
        this.masterKey = crypto.pbkdf2Sync(masterKeyStr, salt, 100000, // 10万轮迭代
        32, // 256位密钥
        'sha256');
        // 存储盐值以便后续使用
        this._currentSalt = salt;
    }
    /**
     * 派生主密钥（PBKDF2）- 同步版本，用于向后兼容
     *
     * @deprecated 使用 initMasterKey() 替代
     * @throws Error 如果 OPENCLAW_MASTER_KEY 未设置
     */
    deriveMasterKey() {
        const masterKey = process.env.OPENCLAW_MASTER_KEY;
        if (!masterKey) {
            throw new Error('OPENCLAW_MASTER_KEY environment variable is required.\n' +
                'Please set it in your environment:\n' +
                '  export OPENCLAW_MASTER_KEY="your-secure-master-key"\n' +
                'Or add it to your .env file.\n' +
                'See .env.example for details.');
        }
        // 密钥最小长度检查（至少 32 字符）
        if (masterKey.length < 32) {
            throw new Error('OPENCLAW_MASTER_KEY must be at least 32 characters long for security.\n' +
                `Current length: ${masterKey.length} characters.`);
        }
        // 使用固定的迁移盐（用于读取旧配置）
        // 新配置将使用随机盐
        const migrationSalt = 'smart-search-skill-salt-v1';
        return crypto.pbkdf2Sync(masterKey, migrationSalt, 100000, // 10万轮迭代
        32, // 256位密钥
        'sha256');
    }
    /**
     * 读取并解密配置
     */
    async readConfig() {
        // 使用缓存
        if (this.configCache) {
            return this.configCache;
        }
        // 确保主密钥已初始化
        await this.initMasterKey();
        try {
            const encryptedData = fs.readFileSync(this.keyFile, 'utf8');
            const data = JSON.parse(encryptedData);
            // 检查配置版本，决定使用哪种盐
            const salt = data.salt
                ? Buffer.from(data.salt, 'hex') // 新版本：使用存储的随机盐
                : Buffer.from('smart-search-skill-salt-v1'); // 旧版本：使用固定盐（迁移）
            // 重新派生主密钥（使用正确的盐）
            const masterKeyStr = process.env.OPENCLAW_MASTER_KEY;
            const derivedKey = crypto.pbkdf2Sync(masterKeyStr, salt, 100000, 32, 'sha256');
            const decipher = crypto.createDecipheriv('aes-256-gcm', derivedKey, Buffer.from(data.iv, 'hex'));
            decipher.setAuthTag(Buffer.from(data.authTag, 'hex'));
            let decrypted = decipher.update(data.encryptedData, 'base64', 'utf8');
            decrypted += decipher.final('utf8');
            this.configCache = JSON.parse(decrypted);
            return this.configCache;
        }
        catch (error) {
            if (error.code === 'ENOENT') {
                throw new Error('Secret config not found. Run "npm run setup" or "npm run key:init" first.');
            }
            throw error;
        }
    }
    /**
     * 写入加密配置
     */
    async writeConfig(config) {
        const masterKeyStr = process.env.OPENCLAW_MASTER_KEY;
        if (!masterKeyStr || masterKeyStr.length < 32) {
            throw new Error('OPENCLAW_MASTER_KEY must be set and at least 32 characters long.');
        }
        // 使用现有盐值或生成新的随机盐
        let salt;
        try {
            const existingData = fs.readFileSync(this.keyFile, 'utf8');
            const existing = JSON.parse(existingData);
            salt = existing.salt
                ? Buffer.from(existing.salt, 'hex')
                : crypto.randomBytes(16);
        }
        catch {
            // 新配置，生成随机盐
            salt = crypto.randomBytes(16);
        }
        // 派生密钥
        const derivedKey = crypto.pbkdf2Sync(masterKeyStr, salt, 100000, 32, 'sha256');
        const iv = crypto.randomBytes(16);
        const cipher = crypto.createCipheriv('aes-256-gcm', derivedKey, iv);
        let encrypted = cipher.update(JSON.stringify(config), 'utf8', 'base64');
        encrypted += cipher.final('base64');
        const authTag = cipher.getAuthTag();
        const encryptedData = {
            version: '2.0', // 升级版本号，表示使用随机盐
            algorithm: 'aes-256-gcm',
            salt: salt.toString('hex'), // 存储随机盐
            createdAt: config.metadata.createdAt,
            updatedAt: new Date().toISOString(),
            encryptedData: encrypted,
            authTag: authTag.toString('hex'),
            iv: iv.toString('hex')
        };
        // 确保目录存在
        const secretsDir = path.dirname(this.keyFile);
        fs.mkdirSync(secretsDir, { recursive: true, mode: 0o700 });
        // 写入文件（权限设置为仅所有者可读写）
        fs.writeFileSync(this.keyFile, JSON.stringify(encryptedData, null, 2), {
            mode: 0o600
        });
        // 更新缓存
        this.configCache = config;
        console.log(`✅ Config written to: ${this.keyFile}`);
    }
    /**
     * 初始化配置（首次使用）
     */
    async initConfig(apiKeys) {
        const config = {
            engines: {},
            metadata: {
                owner: 'smart-search-skill',
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
                accessLog: []
            }
        };
        // 添加引擎配置
        for (const [engine, apiKey] of Object.entries(apiKeys)) {
            if (!apiKey || !apiKey.trim())
                continue;
            const engineType = engine;
            config.engines[engine] = {
                apiKey: apiKey.trim(),
                enabled: true,
                priority: types_1.ENGINE_PRIORITIES[engineType] || 99,
                quotaLimit: types_1.ENGINE_QUOTAS[engineType] || 0,
                quotaUsed: 0,
                lastRotated: new Date().toISOString()
            };
            // 记录访问日志
            config.metadata.accessLog.push({
                engine,
                timestamp: new Date().toISOString(),
                action: 'init'
            });
        }
        await this.writeConfig(config);
        console.log(`✅ Config initialized with ${Object.keys(apiKeys).length} engines`);
    }
    /**
     * 获取单个引擎的 Key
     */
    async getEngineKey(engine) {
        const config = await this.readConfig();
        const engineConfig = config.engines[engine];
        if (!engineConfig) {
            throw new Error(`Engine "${engine}" is not configured. Run "npm run key:set ${engine}" to add it.`);
        }
        if (!engineConfig.enabled) {
            throw new Error(`Engine "${engine}" is disabled. Run "npm run key:rotate ${engine}" to re-enable it.`);
        }
        // 记录访问日志
        await this.logAccess(engine, 'read');
        return engineConfig.apiKey;
    }
    /**
     * 设置单个引擎的 Key
     */
    async setEngineKey(engine, apiKey) {
        let config;
        try {
            config = await this.readConfig();
        }
        catch {
            // 配置不存在，创建新配置
            config = {
                engines: {},
                metadata: {
                    owner: 'smart-search-skill',
                    createdAt: new Date().toISOString(),
                    updatedAt: new Date().toISOString(),
                    accessLog: []
                }
            };
        }
        const engineType = engine;
        config.engines[engine] = {
            apiKey: apiKey.trim(),
            enabled: true,
            priority: types_1.ENGINE_PRIORITIES[engineType] || 99,
            quotaLimit: types_1.ENGINE_QUOTAS[engineType] || 0,
            quotaUsed: config.engines[engine]?.quotaUsed || 0,
            lastRotated: new Date().toISOString()
        };
        // 记录访问日志
        config.metadata.accessLog.push({
            engine,
            timestamp: new Date().toISOString(),
            action: 'set'
        });
        await this.writeConfig(config);
        console.log(`✅ API Key set for engine: ${engine}`);
    }
    /**
     * 轮换 Key
     */
    async rotateKey(engine, newApiKey) {
        const config = await this.readConfig();
        const engineConfig = config.engines[engine];
        if (!engineConfig) {
            throw new Error(`Engine "${engine}" is not configured.`);
        }
        // 如果没有提供新 Key，则切换启用状态
        if (!newApiKey) {
            engineConfig.enabled = !engineConfig.enabled;
            console.log(`${engineConfig.enabled ? '✅' : '❌'} Engine "${engine}" ${engineConfig.enabled ? 'enabled' : 'disabled'}`);
        }
        else {
            engineConfig.apiKey = newApiKey.trim();
            engineConfig.lastRotated = new Date().toISOString();
            console.log(`✅ API Key rotated for engine: ${engine}`);
        }
        config.metadata.accessLog.push({
            engine,
            timestamp: new Date().toISOString(),
            action: 'rotate'
        });
        await this.writeConfig(config);
    }
    /**
     * 列出所有引擎
     */
    async listEngines() {
        const config = await this.readConfig();
        console.log('\n📊 Configured Engines:');
        console.log('='.repeat(50));
        for (const [name, engine] of Object.entries(config.engines)) {
            const status = engine.enabled ? '✅' : '❌';
            const quotaPercent = engine.quotaLimit > 0
                ? Math.round((engine.quotaUsed / engine.quotaLimit) * 100)
                : 0;
            console.log(`${status} ${name.padEnd(12)} | Priority: ${engine.priority} | Quota: ${engine.quotaUsed}/${engine.quotaLimit} (${quotaPercent}%)`);
        }
        console.log('='.repeat(50));
    }
    /**
     * 显示详细状态
     */
    async showStatus() {
        const config = await this.readConfig();
        console.log('\n🔐 Smart Search Secret Status');
        console.log('='.repeat(50));
        console.log(`Created: ${config.metadata.createdAt}`);
        console.log(`Updated: ${config.metadata.updatedAt}`);
        console.log(`Total Engines: ${Object.keys(config.engines).length}`);
        console.log('');
        for (const [name, engine] of Object.entries(config.engines)) {
            console.log(`${name}:`);
            const keyPreview = engine.apiKey.length > 20
                ? `${engine.apiKey.substring(0, 12)}...${engine.apiKey.substring(engine.apiKey.length - 8)}`
                : engine.apiKey;
            console.log(`  API Key: ${keyPreview}`);
            console.log(`  Enabled: ${engine.enabled}`);
            console.log(`  Priority: ${engine.priority}`);
            console.log(`  Quota: ${engine.quotaUsed}/${engine.quotaLimit}`);
            console.log(`  Last Rotated: ${engine.lastRotated}`);
            console.log('');
        }
    }
    /**
     * 记录访问日志
     */
    async logAccess(engine, action) {
        try {
            const config = await this.readConfig();
            config.metadata.accessLog.push({
                engine,
                timestamp: new Date().toISOString(),
                action
            });
            config.metadata.updatedAt = new Date().toISOString();
            // 只保留最近 100 条日志
            if (config.metadata.accessLog.length > 100) {
                config.metadata.accessLog = config.metadata.accessLog.slice(-100);
            }
            // 异步写入，不阻塞主流程
            this.writeConfig(config).catch(err => {
                console.warn('Failed to update access log:', err.message);
            });
        }
        catch (error) {
            // 忽略日志写入错误
        }
    }
    /**
     * 获取配置文件路径
     */
    getKeyFilePath() {
        return this.keyFile;
    }
    /**
     * 检查配置是否存在
     */
    configExists() {
        return fs.existsSync(this.keyFile);
    }
    /**
     * 清除缓存
     */
    clearCache() {
        this.configCache = null;
    }
}
exports.SecretManager = SecretManager;
// CLI 入口
async function main() {
    const secretManager = new SecretManager();
    const command = process.argv[2];
    const args = process.argv.slice(3);
    try {
        switch (command) {
            case 'init':
                // 初始化配置（从环境变量或交互式输入）
                const apiKeys = {};
                const engines = ['bailian', 'tavily', 'serper', 'exa', 'firecrawl'];
                console.log('\n🔐 Smart Search API Key Setup');
                console.log('================================\n');
                for (const engine of engines) {
                    const envKey = process.env[`${engine.toUpperCase()}_API_KEY`];
                    if (envKey) {
                        apiKeys[engine] = envKey;
                        console.log(`✅ Found ${engine} key in environment`);
                    }
                }
                if (Object.keys(apiKeys).length === 0) {
                    console.log('⚠️  No API keys found in environment variables.');
                    console.log('Set environment variables like: BAILIAN_API_KEY=xxx');
                    console.log('Or use: npm run setup (interactive setup)');
                    process.exit(1);
                }
                await secretManager.initConfig(apiKeys);
                break;
            case 'list':
                await secretManager.listEngines();
                break;
            case 'get':
                if (!args[0]) {
                    console.error('Usage: ts-node manage-keys.ts get <engine>');
                    console.error('Engines: bailian, tavily, serper, exa, firecrawl');
                    process.exit(1);
                }
                const key = await secretManager.getEngineKey(args[0]);
                console.log(`${args[0]}: ${key}`);
                break;
            case 'status':
                await secretManager.showStatus();
                break;
            case 'rotate':
                if (!args[0]) {
                    console.error('Usage: ts-node manage-keys.ts rotate <engine> [newApiKey]');
                    process.exit(1);
                }
                await secretManager.rotateKey(args[0], args[1]);
                break;
            default:
                console.log('Usage: ts-node manage-keys.ts <command>');
                console.log('Commands: init, list, get, status, rotate');
                console.log('');
                console.log('Examples:');
                console.log('  ts-node manage-keys.ts init');
                console.log('  ts-node manage-keys.ts list');
                console.log('  ts-node manage-keys.ts get bailian');
                console.log('  ts-node manage-keys.ts status');
                console.log('  ts-node manage-keys.ts rotate bailian');
        }
    }
    catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}
// 如果直接运行则执行 main
if (require.main === module) {
    main();
}
//# sourceMappingURL=key-manager.js.map