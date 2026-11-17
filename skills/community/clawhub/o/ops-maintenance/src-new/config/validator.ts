/**
 * 配置验证器
 * 使用 Zod 进行运行时验证
 */

import { z } from 'zod'
import type { SSHConfig, ConfigValidationError } from './schemas'

/**
 * SSH 配置验证 Schema
 */
const SSHConfigSchema = z.object({
  host: z.string().min(1).max(255),
  port: z.number().int().positive().max(65535).optional().default(22),
  user: z.string().min(1).max(100).optional().default('root'),
  password: z.string().optional(),
  keyFile: z.string().optional(),
  name: z.string().min(1).max(200).optional(),
  tags: z.array(z.string()).optional().default([])
})

/**
 * 服务器列表验证 Schema
 */
export const ServersConfigSchema = z.array(SSHConfigSchema)

/**
 * 验证单个 SSH 配置
 */
export function validateSSHConfig(config: any): SSHConfig {
  try {
    const result = SSHConfigSchema.parse(config)
    // 密码或密钥必须提供一个
    if (!result.password && !result.keyFile) {
      throw new ConfigValidationError(
        '必须提供 password 或 keyFile 中的一个进行认证',
        'auth',
        config
      )
    }
    return result
  } catch (error: any) {
    if (error instanceof z.ZodError) {
      const issue = error.issues[0]
      throw new ConfigValidationError(
        `配置验证失败: ${issue.message}`,
        issue.path.join('.'),
        issue.path[0]
      )
    }
    throw error
  }
}

/**
 * 验证服务器列表
 */
export function validateServersList(data: any): SSHConfig[] {
  if (!Array.isArray(data)) {
    throw new ConfigValidationError('配置必须是数组', 'root', typeof data)
  }

  const results: SSHConfig[] = []
  for (let i = 0; i < data.length; i++) {
    try {
      const validated = validateSSHConfig(data[i])
      results.push(validated)
    } catch (error: any) {
      if (error instanceof ConfigValidationError) {
        throw new ConfigValidationError(
          `服务器列表第 ${i + 1} 项验证失败: ${error.message}`,
          error.field,
          error.value
        )
      }
      throw error
    }
  }

  return results
}

/**
 * 环境变量配置 Schema（可选）
 */
export const EnvConfigSchema = z.object({
  OPS_CONFIG_PATH: z.string().optional(),
  OPS_CACHE_TTL: z.number().int().positive().optional().default(30),
  OPS_SSH_TIMEOUT: z.number().int().positive().optional().default(10000),
  OPS_MAX_CONCURRENT: z.number().int().positive().optional().default(10),
  OPS_LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).optional().default('info')
})

export type EnvConfig = z.infer<typeof EnvConfigSchema>