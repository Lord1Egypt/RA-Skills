# Example: screenshot-capture (Tool Integration)

Combines OpenClaw tools (browser, nodes, image) to produce a result.

## Characteristics
- Phase 0: source detection (URL vs Node vs current browser)
- No sub-agents (direct tool calls)
- Style Guide: N/A
- Core: tool combination patterns, error fallback chains

## skill-audit Score: 78.0 (B)
N/A: C+E → A(30%), B(20%), D(20%), F(30%)

## Skill Structure
```
screenshot-capture/
├── SKILL.md                              # 108 lines — capture methods + error handling
└── references/
    └── browser-automation-notes.md       # stale refs, SPA, Cloudflare workarounds
```

## Lessons Learned
- Tool-integration skills hinge on "which tool, when" — decision logic is the core
- Error fallback chains matter (Cloudflare → web_fetch → firecrawl)
- Moving tool-specific caveats to references/ keeps SKILL.md clean
