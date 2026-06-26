#!/usr/bin/env node
/**
 * MCP stdio server — exposes clipper_search_notes and clipper_get_note_context to OpenClaw.
 * Forwards JSON-RPC to Clipper's Unix socket using saved pairing credentials.
 */
import crypto from "node:crypto";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import {
  callClipper,
  loadCredentials,
  saveCredentials,
  defaultSocketPath,
} from "./clipper-socket.mjs";

async function ensureAuthenticated() {
  let creds = loadCredentials();
  if (creds?.token && creds?.clientId) {
    return creds;
  }

  const { publicKey, privateKey } = crypto.generateKeyPairSync("ed25519");
  const jwk = publicKey.export({ format: "jwk" });
  const rawPublic = Buffer.from(jwk.x, "base64url");

  const pairResp = await callClipper("clipper.pairing_request", {
    displayName: "OpenClaw",
    publicKey: rawPublic.toString("base64"),
  });

  const result = pairResp.result ?? {};
  if (result.status !== "approved" && result.error) {
    throw new Error(
      `Clipper pairing failed. Run: node pair.mjs — ${JSON.stringify(result)}`
    );
  }
  const clientID = result.client_id;
  if (!clientID) {
    throw new Error("Pairing not approved. Approve OpenClaw in Clipper Settings → Integrations.");
  }

  const challengeResp = await callClipper("clipper.auth_challenge", { clientId: clientID });
  const challengeId = challengeResp.result?.challenge_id;
  const nonceB64 = challengeResp.result?.nonce;
  if (!challengeId || !nonceB64) {
    throw new Error("Auth challenge failed");
  }

  const nonce = Buffer.from(nonceB64, "base64");
  const signature = crypto.sign(null, nonce, privateKey);
  const verifyResp = await callClipper("clipper.auth_verify", {
    clientId: clientID,
    challengeId,
    signature: signature.toString("base64"),
  });

  const token = verifyResp.result?.token;
  if (!token) {
    throw new Error("Auth verify failed");
  }

  creds = {
    clientId: clientID,
    token,
    privateKeyPem: privateKey.export({ type: "pkcs8", format: "pem" }).toString(),
    publicKeyRaw: rawPublic.toString("base64"),
  };
  saveCredentials(creds);
  return creds;
}

async function clipperRPC(toolMethod, args, token) {
  const resp = await callClipper(toolMethod, {
    token,
    arguments: args,
  });
  if (resp.error) {
    throw new Error(resp.error.message || JSON.stringify(resp.error));
  }
  if (resp.result?.error === "permission_blocked") {
    throw new Error(
      resp.result.message ||
        `Permission blocked — grant ${resp.result.required_scope} in Clipper Settings → Integrations`
    );
  }
  if (resp.result?.error === "tool_disabled") {
    throw new Error(resp.result.message || `Tool disabled in Clipper Settings → Integrations`);
  }
  return resp.result ?? resp;
}

const server = new Server(
  { name: "offlyn-clipper", version: "0.1.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "clipper_search_notes",
      description:
        "Search existing Offlyn Clipper notes using scoped permissions. Returns summaries, snippets, and citations. Use when the user asks about previous notes, prior thinking, saved context, or project notes.",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "Natural language search query" },
          limit: { type: "number", description: "Max results (default 5)" },
          include_raw: {
            type: "boolean",
            description: "Request raw bodies (requires notes:read:raw in Clipper)",
          },
        },
        required: ["query"],
      },
    },
    {
      name: "clipper_get_note_context",
      description:
        "Retrieve context for a specific Clipper note. Returns summary/snippet by default; full body only if notes:read:raw is granted.",
      inputSchema: {
        type: "object",
        properties: {
          note_id: { type: "string", description: "Clipper note UUID" },
          include_raw_body: { type: "boolean", description: "Include full note body" },
        },
        required: ["note_id"],
      },
    },
    {
      name: "clipper_catch_me_up",
      description:
        "Get live context from the meeting Clipper is recording right now (transcript so far, user notes, decisions). Use when the user asks to catch up, what they missed, or recap the current call. OpenClaw should summarize recap_context for the user.",
      inputSchema: { type: "object", properties: {} },
    },
    {
      name: "clipper_list_chat_presets",
      description:
        "List Clipper chat suggestion presets (same chips as in-app meeting/note chat). Call when starting a Clipper-related conversation so you can offer 2–4 short options to the user, then run the recommended_tool when they pick one.",
      inputSchema: { type: "object", properties: {} },
    },
    {
      name: "clipper_ping",
      description:
        "Health check: Clipper socket, live meeting active, enabled tools. Call first if you see 'bundle-mcp runtime disposed' or before clipper_catch_me_up after gateway restart.",
      inputSchema: { type: "object", properties: {} },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "clipper_ping") {
      const result = await callClipper("clipper.ping", {});
      const body = result.result ?? result;
      return { content: [{ type: "text", text: JSON.stringify(body, null, 2) }] };
    }

    const creds = await ensureAuthenticated();

    if (name === "clipper_search_notes") {
      const result = await clipperRPC(
        "clipper.search_notes",
        {
          query: args?.query ?? "",
          limit: args?.limit ?? 5,
          include_raw: args?.include_raw ?? false,
        },
        creds.token
      );
      const text = formatSearchResult(result);
      return { content: [{ type: "text", text }] };
    }

    if (name === "clipper_get_note_context") {
      const result = await clipperRPC(
        "clipper.get_note_context",
        {
          note_id: args?.note_id,
          include_raw_body: args?.include_raw_body ?? false,
        },
        creds.token
      );
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    }

    if (name === "clipper_catch_me_up") {
      const result = await clipperRPC("clipper.catch_me_up", {}, creds.token);
      if (result?.error === "no_active_meeting") {
        return {
          content: [{ type: "text", text: result.message ?? "No meeting is being recorded in Clipper." }],
          isError: true,
        };
      }
      const text = formatCatchMeUpResult(result);
      return { content: [{ type: "text", text }] };
    }

    if (name === "clipper_list_chat_presets") {
      const result = await clipperRPC("clipper.list_chat_presets", {}, creds.token);
      return { content: [{ type: "text", text: formatChatPresetsResult(result) }] };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (err) {
    return {
      content: [{ type: "text", text: `Clipper error: ${err.message}` }],
      isError: true,
    };
  }
});

function formatSearchResult(result) {
  const answer = result.answer ?? "No answer.";
  const results = result.results ?? [];
  if (results.length === 0) {
    return `${answer}\n\n(No matching notes.)`;
  }
  const sources = results
    .map((r, i) => {
      const title = r.title ?? "Untitled";
      const snippet = r.snippet ?? r.summary ?? "";
      const link = r.deep_link ?? r.deepLink ?? "";
      return `${i + 1}. ${title}\n   "${snippet}"\n   ${link}`;
    })
    .join("\n\n");
  return `${answer}\n\nSources:\n${sources}`;
}

function formatChatPresetsResult(result) {
  const guidance = result.guidance ?? "";
  const ctx = result.session_context ?? result.sessionContext ?? "general";
  const presets = result.presets ?? [];
  const lines = presets.map((p, i) => {
    const tool = p.recommended_tool ?? p.recommendedTool;
    const avail = p.available !== false;
    return `${i + 1}. ${p.suggest_to_user ?? p.suggestToUser ?? p.label}${tool ? ` → ${tool}${avail ? "" : " (unavailable)"}` : ""}`;
  });
  return `Session: ${ctx}\n\n${guidance}\n\nPresets:\n${lines.join("\n")}`;
}

function formatCatchMeUpResult(result) {
  const prompt = result.suggested_agent_prompt ?? result.suggestedAgentPrompt;
  const recap = result.recap_context ?? result.recapContext ?? result.answer ?? "";
  const title = result.title ?? "Current meeting";
  const recording = result.is_recording ?? result.isRecording;
  const header = recording
    ? `Live meeting: ${title} (recording)`
    : `Meeting session: ${title} (paused — transcript so far)`;
  return `${header}\n\n${recap}\n\n---\nSummarize the above for the user (catch me up): decisions, open questions, action items, and current topic.${prompt ? `\nSuggested prompt: ${prompt}` : ""}`;
}

const transport = new StdioServerTransport();
await server.connect(transport);
