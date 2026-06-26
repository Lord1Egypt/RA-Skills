const fs = require('fs');

const port = process.env.PORT || '18789';
const llmUrl = process.env.LLM || 'http://localhost:11434/v1';
const model = process.env.MODEL || 'ServiceNow-AI/Apriel-1.6-15b-Thinker:Q4_K_M';
const token = process.env.TOKEN || Math.random().toString(36).substring(2);
const dataDir = process.env.DATA || (process.env.USERPROFILE || process.env.HOME) + '/.openclaw';

const modelKey = 'locallm/' + model;

const config = {
    meta: { lastTouchedVersion: '2026.2.17' },
    models: {
        providers: {
            locallm: {
                baseUrl: llmUrl,
                apiKey: '',
                api: 'openai-completions',
                authHeader: false,
                models: [{
                    id: model,
                    name: model,
                    api: 'openai-completions',
                    reasoning: false,
                    input: ['text'],
                    cost: { input: 0, output: 0 },
                    contextWindow: 200000,
                    maxTokens: 20000
                }]
            }
        }
    },
    agents: {
        defaults: {
            model: { primary: modelKey },
            models: { [modelKey]: {} },
            workspace: dataDir + '/workspace',
            compaction: { mode: 'safeguard' },
            maxConcurrent: 4
        }
    },
    gateway: {
        port: parseInt(port),
        mode: 'local',
        bind: '127.0.0.1',  // Localhost-only for security (no external access)
        auth: { mode: 'token', token: token },
        tailscale: { mode: 'off' },  // Disabled by default (no account required)
        nodes: { denyCommands: ['camera.snap', 'camera.clip', 'screen.record', 'exec'] }
    },
    channels: {
        "webchat": {
            "account": "default",
            "config": {}
        }
    },
    hooks: { internal: { enabled: true, entries: {} } },
    commands: { native: 'auto', nativeSkills: 'auto' },
    messages: { ackReactionScope: 'group-mentions' }
};

fs.mkdirSync(dataDir, { recursive: true });
fs.mkdirSync(dataDir + '/workspace', { recursive: true });
fs.writeFileSync(dataDir + '/openclaw.json', JSON.stringify(config, null, 2));

console.log('Config created at ' + dataDir + '/openclaw.json');
console.log('Token: ' + token);