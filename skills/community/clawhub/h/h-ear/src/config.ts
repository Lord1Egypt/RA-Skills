/**
 * Config resolution for H-ear OpenClaw skill.
 * Reads from environment variables (OpenClaw passes these from SKILL.md requires).
 */

import { ENVIRONMENTS, type ServerConfig, type HearEnvironment } from '@h-ear/core';

export function resolveConfig(): ServerConfig {
    const apiKey = process.env.HEAR_API_KEY;
    const bearerToken = process.env.HEAR_BEARER_TOKEN || undefined;
    if (!apiKey && !bearerToken) throw new Error('HEAR_API_KEY or HEAR_BEARER_TOKEN environment variable is required');
    const envStr = process.env.HEAR_ENV || 'prod';

    const environment = (Object.keys(ENVIRONMENTS).includes(envStr) ? envStr : 'prod') as HearEnvironment;
    const envConfig = ENVIRONMENTS[environment];
    const baseUrl = process.env.HEAR_BASE_URL || envConfig.baseUrl;
    const apiPath = envConfig.apiPath;

    return { apiKey: apiKey || '', bearerToken, environment, baseUrl, apiPath };
}
