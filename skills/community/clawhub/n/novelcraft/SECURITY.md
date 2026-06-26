# Security Considerations

## Before You Run NovelCraft

### ⚠️ Data Privacy

**NovelCraft writes your book content to disk and may send it to external services:**

- All drafts, reviews, and final chapters are stored in `~/.openclaw/workspace/novelcraft/`
- If you enable **image generation**, content may be sent to external APIs
- Treat any configured image provider as a potential sink for book contents

**Recommendations:**
- Do not include real names, addresses, or sensitive personal information
- Review `module-images.md` before enabling image generation
- Use `manual` or `local` image providers for sensitive content

### ⚠️ Network Access

**Image generation requires network calls:**

- Default configuration uses **no provider** (images disabled)
- If you enable images, the skill will make HTTP requests to your configured endpoint
- Review network activity or run in a restricted environment until you trust the providers

### ⚠️ Disk Space

**NovelCraft generates many large files:**

- Drafts, reviews, revisions per chapter
- Final PDFs and EPUBs
- Estimated: 5-15 MB per novel project

**Ensure you have sufficient disk space and backups.**

### ⚠️ Required Binaries

**PDF/EPUB generation requires:**

- `pandoc` — Document conversion
- `xelatex` (optional) — Enhanced PDF output

**Check before running:**
```bash
which pandoc
which xelatex
```

If missing, publication will fail.

### ⚠️ Autonomy Levels

| Mode | Behavior | Recommendation |
|------|----------|----------------|
| `step-by-step` | Confirms after each module | ✅ **Use for first runs** |
| `autonomous` | No questions, runs through | Only after you trust the config |

**Always use step-by-step mode when testing a new project.**

### ⚠️ Configuration Files

**Do not paste secrets into:**

- `project-manifest.md`
- Any `module-*.md` files

**Keep API keys in:**
- Environment variables
- Separate secret management tools
- MCP server configs (outside NovelCraft)

### ⚠️ Image Provider Defaults

**Default configuration:**
```yaml
# module-images.md
enabled: false  # Images are DISABLED by default
provider: none
```

**Before enabling images:**
1. Choose your provider: `mcp`, `api`, `local`, or `manual`
2. Configure the endpoint (if using external API)
3. Review what data will be sent

## Reporting Issues

If you discover security issues with NovelCraft:
1. Check your configuration files first
2. Review what data was sent to external services
3. Report to the skill maintainer with details

---

*Last updated: 2026-04-06*
