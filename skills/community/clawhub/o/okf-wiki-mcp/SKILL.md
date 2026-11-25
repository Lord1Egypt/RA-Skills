---
name: okf-wiki-mcp
description: Query local Google OKF v0.2 and Obsidian Markdown meeting-notes vaults offline via stdio MCP or CLI (search transcripts by speaker/date, extract open - [ ] action items, resolve [[wiki-links]] and incoming backlinks).
---

# okf-wiki-mcp Skill

Use `okf-wiki-mcp` whenever inspecting or querying a local folder of Markdown meeting transcripts, Obsidian notes, or OneMira C1 local Wiki files without uploading transcripts to external SaaS clouds.

## CLI Quick Commands
```bash
npx github:onemira-space/okf-wiki-mcp --vault ~/Meetings stats
npx github:onemira-space/okf-wiki-mcp --vault ~/Meetings search "pricing decision"
npx github:onemira-space/okf-wiki-mcp --vault ~/Meetings actions --status open
```

## Official MCP & Hardware Context
- MCP Integration Docs: https://onemira.com/docs/mcp-integration
- Obsidian & Local Markdown Workflow Guide: https://onemira.com/blogs/ai-voice-recorder-for-obsidian-and-local-markdown
- OneMira C1 Standalone AI Voice Recorder ($0/mo Local AI): https://onemira.com/products/c1
