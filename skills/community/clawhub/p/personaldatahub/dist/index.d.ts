/**
 * PersonalDataHub — OpenClaw skill for interacting with PersonalDataHub.
 *
 * Registers tools that let the agent pull personal data and propose
 * outbound actions through the PersonalDataHub access control gateway.
 *
 * Config resolution order:
 *   1. Plugin config (hubUrl + apiKey passed directly)
 *   2. Environment variables (PDH_HUB_URL + PDH_API_KEY)
 *   3. Credentials file (~/.pdh/credentials.json, written by npx pdh init)
 *   4. Auto-discovery (probe localhost, create API key)
 */
export interface PersonalDataHubPluginConfig {
    hubUrl: string;
    apiKey: string;
}
declare const _default: {
    id: string;
    name: string;
    description: string;
    configSchema: {
        safeParse(value: unknown): {
            success: false;
            error: {
                issues: {
                    path: string[];
                    message: string;
                }[];
            };
            data?: undefined;
        } | {
            success: true;
            data: object;
            error?: undefined;
        };
        jsonSchema: {
            type: string;
            additionalProperties: boolean;
            properties: {
                hubUrl: {
                    type: string;
                };
                apiKey: {
                    type: string;
                };
            };
            required: string[];
        };
    };
    register(api: {
        pluginConfig?: Record<string, unknown>;
        logger: {
            info: (msg: string) => void;
            warn: (msg: string) => void;
            error: (msg: string) => void;
        };
        registerTool: (tool: unknown) => void;
        on: (hook: string, handler: (event: unknown) => Promise<unknown>) => void;
    }): Promise<void>;
};
export default _default;
export { HubClient, HubApiError } from './hub-client.js';
export type { HubClientConfig, PullParams, ProposeParams, PullResult, ProposeResult } from './hub-client.js';
export { createPullTool, createProposeTool } from './tools.js';
export { PERSONAL_DATA_SYSTEM_PROMPT } from './prompts.js';
export { checkHub, createApiKey, autoSetup, discoverHub, readCredentials } from './setup.js';
