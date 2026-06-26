# Changelog

## 2.0.0 (2026-03-05)

### New Commands
- **`!rollback <time>`** — Rewind memory to any point in time (e.g., "1h", "2 days ago")
- **`!search <query>`** — Explicit semantic search with relevance scores
- **`!forget <topic>`** — Find and delete memories matching a topic
- **`!remember <text>`** — Explicitly save a fact (vs. auto-save)

### Improvements
- Smart message filtering — skips trivial messages (< 15 chars) to conserve API calls
- Response truncation — caps auto-saved responses at 500 characters
- 10-second timeout on all API calls (prevents agent hangs)
- Better first-run error with signup URL
- Centralized API call helper (DRYer, consistent error handling)
- Enhanced `!status` — shows rollback count and quota percentages

### ClawHub
- Rewrote SKILL.md with proper ClawHub frontmatter and LLM instructions
- Rewrote README as product pitch with feature comparison table
- Added CHANGELOG.md, .clawhubignore, examples/

### Cleanup
- Removed unused `edges()` and `stats()` methods
- Removed dead `fs`/`path` imports

## 1.0.0

### Features
- Auto-save conversation turns to Novyx
- Auto-recall relevant memories before each response
- `!undo [N]` — delete last N saved memories
- `!audit [N]` — show API operations with integrity hashes
- `!status` — memory usage and tier info
- `!help` — command menu
- Graceful 429/403 handling (never crashes the agent)
