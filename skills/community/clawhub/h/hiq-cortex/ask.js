#!/usr/bin/env node

// Ask the HiQ Cortex LCA assistant a question in natural language.
// Supports: LCA knowledge Q&A, carbon footprint calculations, data analysis,
// BOM matching, web research on sustainability topics.
//
// Uses the MCP endpoint with the run_cortex tool.
//
// Usage:
//   ./ask.js "什么是 GWP？"
//   ./ask.js "calculate carbon footprint for 100kg steel + 50kg aluminum"
//   ./ask.js "compare GWP of PET vs HDPE"

const MCP_URL = "https://x.hiqlcd.com/api/deck/mcp";

const query = process.argv.slice(2).join(" ").trim();

if (!query) {
  console.log(`Usage: ask.js <question>

Ask the HiQ Cortex LCA assistant anything about:
  - LCA concepts (GWP, system boundaries, allocation methods, ISO 14040/44)
  - Carbon footprint calculations (single material or BOM)
  - Material comparisons and analysis
  - Sustainability research and EPD lookup

Examples:
  ask.js "什么是 GWP？"
  ask.js "calculate carbon footprint for 100kg steel + 50kg aluminum"
  ask.js "what is the difference between cut-off and consequential system models?"
  ask.js "compare the environmental impact of PET vs HDPE packaging"`);
  process.exit(1);
}

const apiKey = process.env.HIQ_API_KEY;
if (!apiKey) {
  console.error("Error: HIQ_API_KEY environment variable is required.");
  console.error("Get your API key at https://www.hiqlcd.com");
  process.exit(1);
}

const headers = {
  "Content-Type": "application/json",
  "Accept": "application/json, text/event-stream",
  "X-API-Key": apiKey,
};

try {
  // 1. Initialize MCP session
  const initResp = await fetch(MCP_URL, {
    method: "POST",
    headers,
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: {
        protocolVersion: "2024-11-05",
        capabilities: {},
        clientInfo: { name: "hiq-cortex-skill", version: "1.0.0" },
      },
    }),
  });

  if (!initResp.ok) {
    console.error(`MCP init error: ${initResp.status} ${initResp.statusText}`);
    process.exit(1);
  }

  const sessionId = initResp.headers.get("mcp-session-id");
  if (sessionId) {
    headers["Mcp-Session-Id"] = sessionId;
  }

  // 2. Call run_cortex tool
  const callResp = await fetch(MCP_URL, {
    method: "POST",
    headers,
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 2,
      method: "tools/call",
      params: {
        name: "run_cortex",
        arguments: { message: query },
      },
    }),
  });

  if (!callResp.ok) {
    console.error(`MCP call error: ${callResp.status} ${callResp.statusText}`);
    process.exit(1);
  }

  const contentType = callResp.headers.get("content-type") || "";

  if (contentType.includes("text/event-stream")) {
    // SSE response — collect text content
    const reader = callResp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();

      for (const line of lines) {
        if (!line.startsWith("data:")) continue;
        const raw = line.slice(5).trim();
        if (!raw) continue;

        try {
          const event = JSON.parse(raw);
          // JSON-RPC result with content array
          if (event.result?.content) {
            for (const item of event.result.content) {
              if (item.type === "text" && item.text) {
                process.stdout.write(item.text);
              }
            }
          }
        } catch {
          // skip non-JSON lines
        }
      }
    }
  } else {
    // JSON response
    const data = await callResp.json();
    if (data.result?.content) {
      for (const item of data.result.content) {
        if (item.type === "text" && item.text) {
          process.stdout.write(item.text);
        }
      }
    } else if (data.error) {
      console.error(`MCP error: ${data.error.message}`);
      process.exit(1);
    }
  }

  console.log(); // trailing newline
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
