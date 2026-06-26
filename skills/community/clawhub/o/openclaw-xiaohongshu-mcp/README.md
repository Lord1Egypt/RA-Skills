# OpenClaw Xiaohongshu MCP

A local OpenClaw skill for operating Xiaohongshu / RED through a local MCP server and `mcporter`.

## What it includes

- Search Xiaohongshu notes
- Load note details and comments
- Post comments and replies
- Publish image posts
- Use local-image publishing through Docker-mounted `/images`
- Reusable helper scripts for common workflows

## Included files

- `SKILL.md` — skill instructions and trigger description
- `scripts/` — helper scripts for search, detail, comment, pick-detail, and publish
- `assets/config/mcporter.json` — minimal local mcporter config
- `assets/templates/` — publish JSON templates
- `assets/docker-compose.xiaohongshu-mcp.yml` — example local deployment
- `references/setup.md` — setup and persistence notes

## Quick start

### Search

```bash
./scripts/xhs-search.sh OpenClaw
```

### Pick from search results and load detail

```bash
./scripts/xhs-pick-detail.sh OpenClaw
./scripts/xhs-pick-detail.sh --comments OpenClaw
```

### Publish

```bash
./scripts/xhs-publish.sh assets/templates/publish-template-private.json
```

## Notes

- The default config expects a local MCP endpoint at `http://localhost:18060/mcp`
- For local images, publish container-visible paths such as `/images/demo.png`
- Keep runtime data out of the repository; see `.gitignore`
