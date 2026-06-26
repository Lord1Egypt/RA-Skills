"use strict";
// Memory Garden MCP - Unified ClawHub Skill
// Combines search, extraction, and validation in a single skill
// with automatic daemon lifecycle management.
Object.defineProperty(exports, "__esModule", { value: true });
exports.tools = void 0;
exports.beforeQuery = beforeQuery;
exports.afterResponse = afterResponse;
exports.callTool = callTool;
exports.shutdown = shutdown;
const daemon_manager_1 = require("./daemon-manager");
const config_1 = require("./config");
// Initialize configuration
const config = (0, config_1.loadConfig)();
const warnings = (0, config_1.validateConfig)(config);
warnings.forEach(w => console.warn(`[memory-garden] ${w}`));
// Daemon manager (lazy initialized)
let daemonManager = null;
let daemonUrl = config.daemonUrl;
// Ensure daemon is running before making requests
async function ensureDaemon() {
    if (!daemonManager) {
        daemonManager = new daemon_manager_1.DaemonManager();
    }
    daemonUrl = await daemonManager.ensureRunning();
    return daemonUrl;
}
// Generic MCP tool call
async function callMcpTool(toolName, args, timeoutMs = 5000) {
    const url = await ensureDaemon();
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
    try {
        const response = await fetch(`${url}/mcp/tools/call`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: toolName,
                arguments: args
            }),
            signal: controller.signal,
        });
        if (!response.ok) {
            let message = `HTTP ${response.status}`;
            try {
                const body = await response.json();
                if (body.error?.message) {
                    message = body.error.message;
                }
            }
            catch {
                // Ignore JSON parse errors, use HTTP status
            }
            throw new Error(`${toolName} failed: ${message}`);
        }
        const result = await response.json();
        if (!result.content?.[0]?.text) {
            throw new Error('Invalid response format: missing content');
        }
        return JSON.parse(result.content[0].text);
    }
    catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
            throw new Error(`${toolName} timeout after ${timeoutMs}ms. ` +
                `Check if daemon is running: curl ${url}/health`);
        }
        throw error;
    }
    finally {
        clearTimeout(timeoutId);
    }
}
// === Search functionality ===
async function searchPatterns(query, limit, domain) {
    // CR-6: Updated error message to reflect default-enabled behavior
    if (!config.search.enabled) {
        throw new Error('Search is disabled. Remove MG_SEARCH_ENABLED=false to enable (search is enabled by default).');
    }
    const results = await callMcpTool('search_patterns', {
        query,
        limit: limit ?? config.search.limit,
        ...(domain && { domain })
    });
    return results.results || [];
}
// Called by OpenClaw before sending query to LLM
async function beforeQuery(query) {
    if (!config.search.enabled) {
        return query; // Search disabled, no augmentation
    }
    try {
        const results = await searchPatterns(query);
        if (results.length === 0) {
            return query; // No augmentation
        }
        // Build context from patterns
        const context = results
            .map(r => `[${r.pattern.slug}] ${r.pattern.claim}`)
            .join('\n');
        return `Relevant knowledge from community commons:\n${context}\n\nQuery: ${query}`;
    }
    catch (error) {
        console.error('[memory-garden] Search failed:', error);
        return query; // Fail open - don't block query
    }
}
async function extractPatterns(query, response, domain) {
    if (!config.extraction.enabled) {
        throw new Error('Extraction is disabled. Set MG_EXTRACTION_ENABLED=true to enable.');
    }
    return await callMcpTool('harvest_patterns', {
        query,
        response,
        ...(domain && { domain })
    });
}
// Called by OpenClaw after receiving response from LLM
async function afterResponse(query, response) {
    if (!config.extraction.enabled) {
        return; // Extraction disabled
    }
    try {
        const result = await extractPatterns(query, response);
        if (result.patterns.length > 0) {
            console.log(`[memory-garden] Extracted ${result.patterns.length} patterns (confidence: ${result.confidence})`);
            if (config.extraction.confirmRequired) {
                // In confirmation mode, patterns are queued for review
                // The user will see them in the Memory Garden UI
                console.log('[memory-garden] Patterns queued for confirmation');
            }
        }
    }
    catch (error) {
        console.error('[memory-garden] Extraction failed:', error);
        // Fail silently - don't interrupt user flow
    }
}
async function validatePattern(patternCid, context, stance = 'affirming') {
    return await callMcpTool('validate_pattern', {
        pattern_cid: patternCid,
        context,
        stance,
        artifact_source: 'self'
    });
}
// === Tool exports ===
exports.tools = [
    {
        name: 'memory_garden_search',
        description: 'Search the community knowledge commons for relevant patterns',
        inputSchema: {
            type: 'object',
            properties: {
                query: { type: 'string', description: 'Search query' },
                limit: { type: 'number', description: 'Max results (default 8)' },
                domain: { type: 'string', description: 'Filter by domain' },
            },
            required: ['query'],
        },
    },
    ...(config.extraction.enabled ? [{
            name: 'memory_garden_extract',
            description: 'Extract knowledge patterns from a conversation',
            inputSchema: {
                type: 'object',
                properties: {
                    query: { type: 'string', description: 'Original query' },
                    response: { type: 'string', description: 'AI response to extract from' },
                    domain: { type: 'string', description: 'Knowledge domain' },
                },
                required: ['query', 'response'],
            },
        }] : []),
    {
        name: 'memory_garden_validate',
        description: 'Record your experience with a pattern (helps improve ranking)',
        inputSchema: {
            type: 'object',
            properties: {
                pattern_cid: { type: 'string', description: 'Pattern CID to validate' },
                context: { type: 'string', description: 'How/where you validated it' },
                stance: {
                    type: 'string',
                    enum: ['affirming', 'tensioning', 'questioning'],
                    description: 'Your stance on the pattern'
                },
            },
            required: ['pattern_cid', 'context'],
        },
    },
];
async function callTool(name, args) {
    switch (name) {
        case 'memory_garden_search': {
            const results = await searchPatterns(args.query, args.limit, args.domain);
            return {
                content: [{ type: 'text', text: JSON.stringify(results, null, 2) }],
            };
        }
        case 'memory_garden_extract': {
            const result = await extractPatterns(args.query, args.response, args.domain);
            return {
                content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
            };
        }
        case 'memory_garden_validate': {
            const result = await validatePattern(args.pattern_cid, args.context, args.stance);
            return {
                content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
            };
        }
        default:
            throw new Error(`Unknown tool: ${name}`);
    }
}
// Graceful shutdown
async function shutdown() {
    if (daemonManager) {
        await daemonManager.shutdown();
        daemonManager = null;
    }
}
//# sourceMappingURL=index.js.map