---
name: kling-ai-mcp
description: Connect an MCP-compatible AI agent to the official Kling AI Global MCP for image and video generation, account credits, task status, and reusable Elements. Use when a user asks to use Kling AI / 可灵 through MCP.
---

# Kling AI Global MCP

Use the official Global remote MCP endpoint:

`https://kling.ai/mcp/plugin`

Connect it through the host application's MCP settings and complete Kling's OAuth sign-in. Do not ask the user to paste passwords, access tokens, or cookies into chat. This skill does not install a local MCP server or CLI.

After connecting, call `tools/list` and `who_am_i` to discover the live tools, model names, accepted inputs, limits, and account region. Do not guess or reuse stale model settings. Use the MCP tools exposed by the connected server for image generation, video generation, uploads, Elements, motion-library lookup, account/credit queries, and task status.

Generation uses credits from the user's Kling account. Before submitting a generation, confirm the requested output and settings when intent is ambiguous; report credit cost only when the server returns it. Do not submit a generation for prompt-writing or planning requests. After submission, retain the returned task ID and query that task for status; never submit a duplicate just because a result is slow or unclear.

Use the connected Global endpoint only; do not mix regional accounts or credentials.
