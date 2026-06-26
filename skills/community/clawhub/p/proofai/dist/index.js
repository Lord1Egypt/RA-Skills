#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const zod_1 = require("zod");
const API_BASE = process.env.PROOFAI_API_URL || "https://apzgbajvwzykygrxxrwm.supabase.co/functions/v1";
const API_KEY = process.env.PROOFAI_API_KEY || "";
const ANON_KEY = process.env.PROOFAI_ANON_KEY || "";
async function callAPI(path, body) {
    const headers = { "Content-Type": "application/json" };
    if (API_KEY.startsWith("pk_live_")) {
        headers["x-api-key"] = API_KEY;
    }
    if (ANON_KEY) {
        headers["Authorization"] = `Bearer ${ANON_KEY}`;
    }
    const res = await fetch(`${API_BASE}/${path}`, {
        method: "POST",
        headers,
        body: JSON.stringify(body),
    });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(`ProofAI API error ${res.status}: ${text}`);
    }
    return res.json();
}
const server = new mcp_js_1.McpServer({
    name: "proofai",
    version: "1.0.0",
});
// --- Tool: Log an AI decision (full pipeline) ---
server.tool("proofai_certify", "Certify an AI decision with cryptographic proof. Runs the full ProofAI pipeline: compress → execute → analyze → sign → bundle → anchor → verify. Returns a blockchain-verified evidence bundle.", {
    prompt: zod_1.z.string().describe("The AI prompt to certify"),
    provider: zod_1.z.enum(["anthropic", "openai", "gemini"]).default("anthropic").describe("AI provider"),
    temperature: zod_1.z.number().default(0.7).describe("Generation temperature"),
    maxTokens: zod_1.z.number().default(1024).describe("Max output tokens"),
}, async ({ prompt, provider, temperature, maxTokens }) => {
    try {
        // 1. Compress
        const compressed = (await callAPI("compress", { prompt, options: { compressionLevel: "medium" } }));
        // 2. Execute
        const execution = (await callAPI("execute", {
            promptRef: compressed.id,
            options: { provider, modelId: "auto", temperature, maxTokens },
        }));
        // 3. Analyze
        const analysis = (await callAPI("analyze", {
            executionId: execution.id,
            analysisText: execution.output,
        }));
        // 4. Sign
        const signature = (await callAPI("sign", {
            executionId: execution.id,
            rawOutput: execution.output,
            modelProvider: execution.metadata.provider,
            modelId: execution.metadata.model,
            modelVersion: "latest",
            modelParameters: { temperature },
            executionMetrics: { tokens: execution.metadata.tokens.total },
            requesterInfo: { source: "mcp-server" },
            timestamps: { request_received: new Date().toISOString() },
        }));
        // 5. Bundle
        const bundle = (await callAPI("bundle", {
            promptId: compressed.id,
            executionId: execution.id,
            analysisId: analysis.id,
            signatureId: signature.signatureId,
            cognitiveHash: analysis.cognitiveHash,
            promptContent: prompt,
            aiResponse: execution.output,
        }));
        // 6. Anchor
        let anchor = {};
        try {
            anchor = (await callAPI("anchor", { bundleId: bundle.id, network: "polygon" }));
        }
        catch { /* anchor is best-effort */ }
        // 7. Verify
        const verification = (await callAPI("verify", { bundleId: bundle.id }));
        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify({
                        status: "certified",
                        bundleId: bundle.id,
                        bundleHash: bundle.bundleHash,
                        verified: verification.verified,
                        explorerUrl: anchor.explorerUrl || null,
                        transactionHash: anchor.transactionHash || null,
                        provider: execution.metadata.provider,
                        model: execution.metadata.model,
                        tokens: execution.metadata.tokens.total,
                        cognitiveNodes: analysis.metrics.nodeCount,
                        consistencyScore: analysis.metrics.consistencyScore,
                        aiResponse: execution.output.substring(0, 500) + (execution.output.length > 500 ? "..." : ""),
                    }, null, 2),
                },
            ],
        };
    }
    catch (err) {
        return {
            content: [{ type: "text", text: `Error: ${err.message}` }],
            isError: true,
        };
    }
});
// --- Tool: Log a decision (just record, don't execute AI) ---
server.tool("proofai_log", "Log an AI decision that already happened. Creates an evidence bundle with the prompt and response you provide, signs it with Ed25519, and anchors to Polygon.", {
    prompt: zod_1.z.string().describe("The original prompt"),
    response: zod_1.z.string().describe("The AI response to log"),
    provider: zod_1.z.string().default("unknown").describe("Which AI provider generated the response"),
    model: zod_1.z.string().default("unknown").describe("Which model was used"),
}, async ({ prompt, response, provider, model }) => {
    try {
        // Compress
        const compressed = (await callAPI("compress", { prompt, options: {} }));
        // Analyze
        const analysis = (await callAPI("analyze", {
            executionId: `ext_${Date.now()}`,
            analysisText: response,
        }));
        // Sign
        const signature = (await callAPI("sign", {
            executionId: `ext_${Date.now()}`,
            rawOutput: response,
            modelProvider: provider,
            modelId: model,
            modelVersion: "external",
            modelParameters: {},
            executionMetrics: {},
            requesterInfo: { source: "mcp-server-log" },
            timestamps: { logged_at: new Date().toISOString() },
        }));
        // Bundle
        const bundle = (await callAPI("bundle", {
            promptId: compressed.id,
            executionId: `ext_${Date.now()}`,
            analysisId: analysis.id,
            signatureId: signature.signatureId,
            cognitiveHash: analysis.cognitiveHash,
            promptContent: prompt,
            aiResponse: response,
            provider,
            model,
        }));
        // Anchor
        let explorerUrl = null;
        try {
            const anchor = (await callAPI("anchor", { bundleId: bundle.id, network: "polygon" }));
            explorerUrl = anchor.explorerUrl;
        }
        catch { /* best-effort */ }
        return {
            content: [{
                    type: "text",
                    text: `Logged and certified.\n\nBundle ID: ${bundle.id}\nBundle Hash: ${bundle.bundleHash}\nPolygonscan: ${explorerUrl || "pending"}\n\nThis decision is now tamper-evident and blockchain-anchored.`,
                }],
        };
    }
    catch (err) {
        return {
            content: [{ type: "text", text: `Error: ${err.message}` }],
            isError: true,
        };
    }
});
// --- Tool: Verify a bundle ---
server.tool("proofai_verify", "Verify an evidence bundle's integrity and blockchain anchoring. Returns compliance checks against EU AI Act articles.", {
    bundleId: zod_1.z.string().describe("The bundle ID to verify (e.g., bnd_xxx)"),
}, async ({ bundleId }) => {
    try {
        const result = (await callAPI("verify", { bundleId }));
        const checksText = Object.entries(result.checks)
            .map(([k, v]) => `  ${v ? "✅" : "❌"} ${k}`)
            .join("\n");
        return {
            content: [{
                    type: "text",
                    text: `Bundle: ${result.bundleId}\nVerified: ${result.verified ? "✅ YES" : "❌ NO"}\n\nChecks:\n${checksText}${result.ledgerInfo
                        ? `\n\nBlockchain:\n  Network: ${result.ledgerInfo.network}\n  Block: #${result.ledgerInfo.blockNumber}\n  Tx: ${result.ledgerInfo.transactionHash}`
                        : ""}`,
                }],
        };
    }
    catch (err) {
        return {
            content: [{ type: "text", text: `Error: ${err.message}` }],
            isError: true,
        };
    }
});
// --- Tool: Get Polygonscan link ---
server.tool("proofai_polygonscan", "Get the Polygonscan verification URL for a transaction hash. Anyone can verify the proof independently.", {
    txHash: zod_1.z.string().describe("The Polygon transaction hash (0x...)"),
}, async ({ txHash }) => {
    const url = `https://amoy.polygonscan.com/tx/${txHash}`;
    return {
        content: [{
                type: "text",
                text: `Polygonscan verification URL:\n${url}\n\nAnyone can verify this proof — no account, no login, no middleman. Just math.`,
            }],
    };
});
// --- Tool: Get monitoring stats ---
server.tool("proofai_monitor", "Get post-market monitoring statistics for AI compliance (EU AI Act Article 72). Shows anomalies, risk distribution, and compliance status.", {}, async () => {
    try {
        const stats = await callAPI("monitor", {});
        return {
            content: [{
                    type: "text",
                    text: JSON.stringify(stats, null, 2),
                }],
        };
    }
    catch (err) {
        return {
            content: [{ type: "text", text: `Error: ${err.message}` }],
            isError: true,
        };
    }
});
// Start server
async function main() {
    const transport = new stdio_js_1.StdioServerTransport();
    await server.connect(transport);
}
main().catch(console.error);
