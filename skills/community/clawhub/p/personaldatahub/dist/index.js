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
import { HubClient } from './hub-client.js';
import { createPullTool, createProposeTool } from './tools.js';
import { PERSONAL_DATA_SYSTEM_PROMPT } from './prompts.js';
import { discoverHub, checkHub, createApiKey, readCredentials } from './setup.js';
export default {
    id: 'personaldatahub',
    name: 'Personal Data Hub',
    description: 'Unified interface to personal data through PersonalDataHub access control gateway',
    configSchema: {
        safeParse(value) {
            if (!value || typeof value !== 'object' || Array.isArray(value)) {
                return {
                    success: false,
                    error: { issues: [{ path: [], message: 'expected config object' }] },
                };
            }
            const cfg = value;
            if (!cfg.hubUrl || typeof cfg.hubUrl !== 'string') {
                return {
                    success: false,
                    error: { issues: [{ path: ['hubUrl'], message: 'hubUrl is required and must be a string' }] },
                };
            }
            if (!cfg.apiKey || typeof cfg.apiKey !== 'string') {
                return {
                    success: false,
                    error: { issues: [{ path: ['apiKey'], message: 'apiKey is required and must be a string' }] },
                };
            }
            return { success: true, data: value };
        },
        jsonSchema: {
            type: 'object',
            additionalProperties: false,
            properties: {
                hubUrl: { type: 'string' },
                apiKey: { type: 'string' },
            },
            required: ['hubUrl', 'apiKey'],
        },
    },
    async register(api) {
        let config = api.pluginConfig;
        // Step 2: Check environment variables (ClawHub injects from skills.entries.pdh.env)
        if (!config?.hubUrl || !config?.apiKey) {
            const envHubUrl = process.env.PDH_HUB_URL;
            const envApiKey = process.env.PDH_API_KEY;
            if (envHubUrl && envApiKey) {
                config = { hubUrl: envHubUrl, apiKey: envApiKey };
                api.logger.info(`PersonalDataHub: Configured from environment variables (hub: ${envHubUrl})`);
            }
        }
        // Step 3: Check credentials file (~/.pdh/credentials.json)
        if (!config?.hubUrl || !config?.apiKey) {
            const creds = readCredentials();
            if (creds) {
                config = { hubUrl: creds.hubUrl, apiKey: creds.apiKey };
                api.logger.info(`PersonalDataHub: Configured from credentials file (hub: ${creds.hubUrl})`);
            }
        }
        // Step 4: Auto-discovery — probe localhost and create API key
        if (!config?.hubUrl || !config?.apiKey) {
            api.logger.info('PersonalDataHub: Config incomplete, attempting auto-setup...');
            try {
                let hubUrl = config?.hubUrl;
                let apiKey = config?.apiKey;
                if (!hubUrl) {
                    hubUrl = await discoverHub() ?? undefined;
                    if (hubUrl) {
                        api.logger.info(`PersonalDataHub: Discovered hub at ${hubUrl}`);
                    }
                }
                if (hubUrl && !apiKey) {
                    const health = await checkHub(hubUrl);
                    if (health.ok) {
                        const keyResult = await createApiKey(hubUrl, 'OpenClaw Agent');
                        apiKey = keyResult.key;
                        api.logger.info(`PersonalDataHub: Auto-created API key. Save this for your config: ${apiKey}`);
                    }
                }
                if (hubUrl && apiKey) {
                    config = { hubUrl, apiKey };
                }
            }
            catch (err) {
                api.logger.warn(`PersonalDataHub: Auto-setup failed: ${err.message}`);
            }
        }
        if (!config?.hubUrl || !config?.apiKey) {
            api.logger.warn('PersonalDataHub: Missing hubUrl or apiKey. Could not find a running hub.\n' +
                '  To set up PersonalDataHub:\n' +
                '  1. Run: npx pdh init\n' +
                '  2. Run: npx pdh start\n' +
                '  3. Restart the agent — it will auto-connect.\n' +
                '  Or configure manually: { "hubUrl": "http://localhost:3000", "apiKey": "pk_..." }');
            return;
        }
        const client = new HubClient({
            hubUrl: config.hubUrl,
            apiKey: config.apiKey,
        });
        api.logger.info(`PersonalDataHub: Registering tools (hub: ${config.hubUrl})`);
        api.registerTool(createPullTool(client));
        api.registerTool(createProposeTool(client));
        api.on('before_agent_start', async (_event) => {
            return { systemPromptAppend: PERSONAL_DATA_SYSTEM_PROMPT };
        });
    },
};
// Re-export for direct usage
export { HubClient, HubApiError } from './hub-client.js';
export { createPullTool, createProposeTool } from './tools.js';
export { PERSONAL_DATA_SYSTEM_PROMPT } from './prompts.js';
export { checkHub, createApiKey, autoSetup, discoverHub, readCredentials } from './setup.js';
