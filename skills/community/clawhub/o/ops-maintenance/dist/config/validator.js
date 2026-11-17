"use strict";
/**
 * 配置验证器
 * 使用 Zod 进行运行时验证
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.EnvConfigSchema = exports.ServersConfigSchema = void 0;
exports.validateSSHConfig = validateSSHConfig;
exports.validateServersList = validateServersList;
const zod_1 = require("zod");
/**
 * SSH 配置验证 Schema
 */
const SSHConfigSchema = zod_1.z.object({
    host: zod_1.z.string().min(1).max(255),
    port: zod_1.z.number().int().positive().max(65535).optional().default(22),
    user: zod_1.z.string().min(1).max(100).optional().default('root'),
    password: zod_1.z.string().optional(),
    keyFile: zod_1.z.string().optional(),
    name: zod_1.z.string().min(1).max(200).optional(),
    tags: zod_1.z.array(zod_1.z.string()).optional().default([])
});
/**
 * 服务器列表验证 Schema
 */
exports.ServersConfigSchema = zod_1.z.array(SSHConfigSchema);
/**
 * 验证单个 SSH 配置
 */
function validateSSHConfig(config) {
    try {
        const result = SSHConfigSchema.parse(config);
        // 密码或密钥必须提供一个
        if (!result.password && !result.keyFile) {
            throw new ConfigValidationError('必须提供 password 或 keyFile 中的一个进行认证', 'auth', config);
        }
        return result;
    }
    catch (error) {
        if (error instanceof zod_1.z.ZodError) {
            const issue = error.issues[0];
            throw new ConfigValidationError(`配置验证失败: ${issue.message}`, issue.path.join('.'), issue.path[0]);
        }
        throw error;
    }
}
/**
 * 验证服务器列表
 */
function validateServersList(data) {
    if (!Array.isArray(data)) {
        throw new ConfigValidationError('配置必须是数组', 'root', typeof data);
    }
    const results = [];
    for (let i = 0; i < data.length; i++) {
        try {
            const validated = validateSSHConfig(data[i]);
            results.push(validated);
        }
        catch (error) {
            if (error instanceof ConfigValidationError) {
                throw new ConfigValidationError(`服务器列表第 ${i + 1} 项验证失败: ${error.message}`, error.field, error.value);
            }
            throw error;
        }
    }
    return results;
}
/**
 * 环境变量配置 Schema（可选）
 */
exports.EnvConfigSchema = zod_1.z.object({
    OPS_CONFIG_PATH: zod_1.z.string().optional(),
    OPS_CACHE_TTL: zod_1.z.number().int().positive().optional().default(30),
    OPS_SSH_TIMEOUT: zod_1.z.number().int().positive().optional().default(10000),
    OPS_MAX_CONCURRENT: zod_1.z.number().int().positive().optional().default(10),
    OPS_LOG_LEVEL: zod_1.z.enum(['debug', 'info', 'warn', 'error']).optional().default('info')
});
//# sourceMappingURL=validator.js.map