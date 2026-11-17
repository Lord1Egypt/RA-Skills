# Automation

Four programmatic doors, widest to narrowest.

## 1. REST API
Everything the UI does (see api.md). Cookie session + matching Origin + step-up when gated. Right tool for: schema creation (tables/fields, step-up gated), row CRUD and publish cycles, media upload, export/backup pulls, audit reads. Wrong tool for: page-tree edits (never hand-write /site-document payloads).

## 2. In-app AI agent
- Streams over POST /admin/api/ai/chat/site|content (NDJSON); browser-bridged tools relay results via /admin/api/ai/tool-result so edits hit the live workspace state.
- Site scope: 35 tools. Structure moves via semantic-HTML insert/replace through the same import pipeline as paste. Styling via CSS apply (merge/replace/rule-delete/property-removal) plus class assign/remove helpers.
- Content scope: 15 tools over collections and entries.
- Providers: Anthropic, OpenAI, OpenRouter, Ollama, or any OpenAI-compatible endpoint; keys encrypted at rest with INSTATIC_SECRET_KEY. Gates: ai.chat streams, ai.tools.write allows writes.

## 3. MCP server (outside clients driving Instatic)
- Endpoint /_instatic/mcp. Personal access tokens (imcp_pat_ prefix) are created after step-up, shown once, capability-scoped, revocable. Hosted OAuth (authorization code + S256 PKCE; 1h access tokens, rotating refresh, 90-day grant) serves remote MCP clients; hosted clients need an HTTPS canonical origin, they cannot reach localhost or HTTP installs.
- Same tool allow-list gate as the in-app agent; an MCP token grants nothing wider than its capabilities.

## 4. Plugins
- Install by manifest JSON or package zip; inspect-package reads without installing.
- Runtime: each server entrypoint runs in a Bun Worker hosting a QuickJS-WASM sandbox: no Node, no host filesystem, no environment, no network unless granted. SDK surfaces: api.plugin.*, api.cms.*, api.editor.*, api.dashboard.*.
- Plugin capabilities: custom modules/components/pages, dashboard widgets, record resources with CRUD endpoints, schedules (run-now/pause/resume), settings schema with encrypted secrets, frontend asset injection at head/body anchors, publish-time HTML filters.
- Lifecycle: enable/disable, restart, uninstall (?force deletes assets), settings update, SSE event stream.

## Etiquette
Schema through the API (expect step-up). Page trees and styling through the agent or UI. Publishing only via the app's own publish calls, never by writing files into the published directory.
