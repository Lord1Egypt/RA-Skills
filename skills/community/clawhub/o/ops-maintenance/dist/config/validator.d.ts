/**
 * 配置验证器
 * 使用 Zod 进行运行时验证
 */
import { z } from 'zod';
import type { SSHConfig } from './schemas';
/**
 * 服务器列表验证 Schema
 */
export declare const ServersConfigSchema: z.ZodArray<z.ZodObject<{
    host: z.ZodString;
    port: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    user: z.ZodDefault<z.ZodOptional<z.ZodString>>;
    password: z.ZodOptional<z.ZodString>;
    keyFile: z.ZodOptional<z.ZodString>;
    name: z.ZodOptional<z.ZodString>;
    tags: z.ZodDefault<z.ZodOptional<z.ZodArray<z.ZodString, "many">>>;
}, "strip", z.ZodTypeAny, {
    host: string;
    port: number;
    user: string;
    tags: string[];
    password?: string | undefined;
    name?: string | undefined;
    keyFile?: string | undefined;
}, {
    host: string;
    password?: string | undefined;
    port?: number | undefined;
    user?: string | undefined;
    name?: string | undefined;
    tags?: string[] | undefined;
    keyFile?: string | undefined;
}>, "many">;
/**
 * 验证单个 SSH 配置
 */
export declare function validateSSHConfig(config: any): SSHConfig;
/**
 * 验证服务器列表
 */
export declare function validateServersList(data: any): SSHConfig[];
/**
 * 环境变量配置 Schema（可选）
 */
export declare const EnvConfigSchema: z.ZodObject<{
    OPS_CONFIG_PATH: z.ZodOptional<z.ZodString>;
    OPS_CACHE_TTL: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    OPS_SSH_TIMEOUT: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    OPS_MAX_CONCURRENT: z.ZodDefault<z.ZodOptional<z.ZodNumber>>;
    OPS_LOG_LEVEL: z.ZodDefault<z.ZodOptional<z.ZodEnum<["debug", "info", "warn", "error"]>>>;
}, "strip", z.ZodTypeAny, {
    OPS_CACHE_TTL: number;
    OPS_SSH_TIMEOUT: number;
    OPS_MAX_CONCURRENT: number;
    OPS_LOG_LEVEL: "info" | "debug" | "warn" | "error";
    OPS_CONFIG_PATH?: string | undefined;
}, {
    OPS_CONFIG_PATH?: string | undefined;
    OPS_CACHE_TTL?: number | undefined;
    OPS_SSH_TIMEOUT?: number | undefined;
    OPS_MAX_CONCURRENT?: number | undefined;
    OPS_LOG_LEVEL?: "info" | "debug" | "warn" | "error" | undefined;
}>;
export type EnvConfig = z.infer<typeof EnvConfigSchema>;
//# sourceMappingURL=validator.d.ts.map