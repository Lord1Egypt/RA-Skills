# MCP Playbooks — LM Studio

Treat MCP as a separate layer on top of model serving. A bad MCP setup can look like a model problem even when the model is fine.

## 1. When MCP Belongs Here

Use MCP with LM Studio when the user wants:
- Local models plus tools.
- A desktop chat workflow with external capabilities.
- A controlled local-first agent loop where model serving stays separate from tool access.

Do not introduce MCP just because the model is weak. Fix the model path first.

## 2. Basic Connection Flow

Inside LM Studio, MCP servers are configured through `mcp.json`.

High-level process:
1. Add the server definition.
2. Confirm the model still behaves normally without tools.
3. Re-enable the MCP server.
4. Run one focused tool-use test.

That split matters. It tells you whether the failure lives in the model or in the tool layer.

## 3. Manual JSON Pattern

The docs show an `mcpServers` object in `mcp.json`.

Use this mental model:
- Each server entry is explicit.
- Remote URLs and headers are part of the server definition.
- Copy only the server object content that belongs inside `mcpServers`.

Never paste random full JSON blobs into the wrong nesting level.

## 4. Security Boundary

Some MCP servers can:
- Run arbitrary code.
- Access local files.
- Use the network.

Rules:
- Never install MCP servers from untrusted sources.
- Never assume a server is safe because it is popular.
- If the MCP is remote, state clearly that data can leave the machine.

## 5. Token and Context Pressure

Some MCP servers were designed for larger frontier models and can overwhelm smaller local models.

Watch for:
- Context overflows.
- Very slow turns after tool injection.
- Tool descriptions that consume too much prompt budget.

If that happens:
- Reduce tool surface area.
- Use a stronger local model.
- Or keep MCP off for that task.

## 6. Minimal Test Pattern

After enabling MCP:
1. Ask the model to describe which tool it intends to use.
2. Run one small tool request.
3. Confirm the tool output is grounded and complete.
4. Repeat only after the first success.

Avoid multi-tool agent loops until the first small test passes.

## 7. Debugging Split

Use this order:
- Model works without MCP?
- MCP server loads cleanly?
- Tool call works once?
- Multi-step loop works?

Only move to the next layer after the current one passes.
