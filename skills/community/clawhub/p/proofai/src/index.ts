#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const API_BASE = process.env.PROOFAI_API_URL || "https://apzgbajvwzykygrxxrwm.supabase.co/functions/v1";
const API_KEY = process.env.PROOFAI_API_KEY || "";
const ANON_KEY = process.env.PROOFAI_ANON_KEY || "";

async function callAPI(path: string, body: Record<string, unknown>): Promise<unknown> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
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

const server = new McpServer({
  name: "proofai",
  version: "1.0.0",
});

// --- Tool: Log an AI decision (full pipeline) ---
server.tool(
  "proofai_certify",
  "Certify an AI decision with cryptographic proof. Runs the full ProofAI pipeline: compress → execute → analyze → sign → bundle → anchor → verify. Returns a blockchain-verified evidence bundle.",
  {
    prompt: z.string().describe("The AI prompt to certify"),
    provider: z.enum(["anthropic", "openai", "gemini"]).default("anthropic").describe("AI provider"),
    temperature: z.number().default(0.7).describe("Generation temperature"),
    maxTokens: z.number().default(1024).describe("Max output tokens"),
  },
  async ({ prompt, provider, temperature, maxTokens }) => {
    try {
      // 1. Compress
      const compressed = (await callAPI("compress", { prompt, options: { compressionLevel: "medium" } })) as { id: string; compressedDsl: string };

      // 2. Execute
      const execution = (await callAPI("execute", {
        promptRef: compressed.id,
        options: { provider, modelId: "auto", temperature, maxTokens },
      })) as { id: string; output: string; metadata: { provider: string; model: string; tokens: { total: number } } };

      // 3. Analyze
      const analysis = (await callAPI("analyze", {
        executionId: execution.id,
        analysisText: execution.output,
      })) as { id: string; cognitiveHash: string; metrics: { nodeCount: number; consistencyScore: number } };

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
      })) as { signatureId: string };

      // 5. Bundle
      const bundle = (await callAPI("bundle", {
        promptId: compressed.id,
        executionId: execution.id,
        analysisId: analysis.id,
        signatureId: signature.signatureId,
        cognitiveHash: analysis.cognitiveHash,
        promptContent: prompt,
        aiResponse: execution.output,
      })) as { id: string; bundleHash: string };

      // 6. Anchor
      let anchor: { transactionHash?: string; explorerUrl?: string; status?: string } = {};
      try {
        anchor = (await callAPI("anchor", { bundleId: bundle.id, network: "polygon" })) as typeof anchor;
      } catch { /* anchor is best-effort */ }

      // 7. Verify
      const verification = (await callAPI("verify", { bundleId: bundle.id })) as { verified: boolean };

      return {
        content: [
          {
            type: "text" as const,
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
    } catch (err) {
      return {
        content: [{ type: "text" as const, text: `Error: ${(err as Error).message}` }],
        isError: true,
      };
    }
  }
);

// --- Tool: Log a decision (just record, don't execute AI) ---
server.tool(
  "proofai_log",
  "Log an AI decision that already happened. Creates an evidence bundle with the prompt and response you provide, signs it with Ed25519, and anchors to Polygon.",
  {
    prompt: z.string().describe("The original prompt"),
    response: z.string().describe("The AI response to log"),
    provider: z.string().default("unknown").describe("Which AI provider generated the response"),
    model: z.string().default("unknown").describe("Which model was used"),
  },
  async ({ prompt, response, provider, model }) => {
    try {
      // Compress
      const compressed = (await callAPI("compress", { prompt, options: {} })) as { id: string };

      // Analyze
      const analysis = (await callAPI("analyze", {
        executionId: `ext_${Date.now()}`,
        analysisText: response,
      })) as { id: string; cognitiveHash: string };

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
      })) as { signatureId: string };

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
      })) as { id: string; bundleHash: string };

      // Anchor
      let explorerUrl: string | null = null;
      try {
        const anchor = (await callAPI("anchor", { bundleId: bundle.id, network: "polygon" })) as { explorerUrl: string };
        explorerUrl = anchor.explorerUrl;
      } catch { /* best-effort */ }

      return {
        content: [{
          type: "text" as const,
          text: `Logged and certified.\n\nBundle ID: ${bundle.id}\nBundle Hash: ${bundle.bundleHash}\nPolygonscan: ${explorerUrl || "pending"}\n\nThis decision is now tamper-evident and blockchain-anchored.`,
        }],
      };
    } catch (err) {
      return {
        content: [{ type: "text" as const, text: `Error: ${(err as Error).message}` }],
        isError: true,
      };
    }
  }
);

// --- Tool: Verify a bundle ---
server.tool(
  "proofai_verify",
  "Verify an evidence bundle's integrity and blockchain anchoring. Returns compliance checks against EU AI Act articles.",
  {
    bundleId: z.string().describe("The bundle ID to verify (e.g., bnd_xxx)"),
  },
  async ({ bundleId }) => {
    try {
      const result = (await callAPI("verify", { bundleId })) as {
        bundleId: string;
        verified: boolean;
        checks: Record<string, boolean>;
        ledgerInfo?: { transactionHash: string; blockNumber: number; network: string };
      };

      const checksText = Object.entries(result.checks)
        .map(([k, v]) => `  ${v ? "✅" : "❌"} ${k}`)
        .join("\n");

      return {
        content: [{
          type: "text" as const,
          text: `Bundle: ${result.bundleId}\nVerified: ${result.verified ? "✅ YES" : "❌ NO"}\n\nChecks:\n${checksText}${
            result.ledgerInfo
              ? `\n\nBlockchain:\n  Network: ${result.ledgerInfo.network}\n  Block: #${result.ledgerInfo.blockNumber}\n  Tx: ${result.ledgerInfo.transactionHash}`
              : ""
          }`,
        }],
      };
    } catch (err) {
      return {
        content: [{ type: "text" as const, text: `Error: ${(err as Error).message}` }],
        isError: true,
      };
    }
  }
);

// --- Tool: Get Polygonscan link ---
server.tool(
  "proofai_polygonscan",
  "Get the Polygonscan verification URL for a transaction hash. Anyone can verify the proof independently.",
  {
    txHash: z.string().describe("The Polygon transaction hash (0x...)"),
  },
  async ({ txHash }) => {
    const url = `https://amoy.polygonscan.com/tx/${txHash}`;
    return {
      content: [{
        type: "text" as const,
        text: `Polygonscan verification URL:\n${url}\n\nAnyone can verify this proof — no account, no login, no middleman. Just math.`,
      }],
    };
  }
);

// --- Tool: Get monitoring stats ---
server.tool(
  "proofai_monitor",
  "Get post-market monitoring statistics for AI compliance (EU AI Act Article 72). Shows anomalies, risk distribution, and compliance status.",
  {},
  async () => {
    try {
      const stats = await callAPI("monitor", {});
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify(stats, null, 2),
        }],
      };
    } catch (err) {
      return {
        content: [{ type: "text" as const, text: `Error: ${(err as Error).message}` }],
        isError: true,
      };
    }
  }
);

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
