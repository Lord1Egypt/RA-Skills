# TOOLS.md — Tool & Skill Configuration

## Local Environment

- **OS:** Linux 6.17.0-1008-nvidia (arm64), Ubuntu-based
- **GPU:** NVIDIA GB10 (Grace Blackwell), 128GB unified memory
- **Node:** v22.22.1
- **LLM Backend:** Ollama (port 11434)
- **Current Model:** qwen3.5:27B
- **Dashboard:** http://127.0.0.1:18789/

## Workspace Conventions

- All workspace files are in `~/.openclaw/workspace/`
- Memory files: `memory/YYYY-MM-DD.md` for daily, `memory/people/`, `memory/projects/`, `memory/topics/`, `memory/decisions/` for structured
- Treat this workspace as a private git repo — commit changes regularly
- File encoding: UTF-8 always
- Line endings: LF (Unix)

## Installed Skills

_Skills to be vetted and installed. Start conservative:_

### Phase 1 (Approved)
- Web search (built-in)
- File read/write (workspace only)
- Memory tools (built-in)

### Phase 2 (Pending Security Review)
- Email integration (dedicated agent account needed first)
- Calendar integration (dedicated agent account needed first)
- Apollo.io CRM (API key configuration pending)

### Phase 3 (Future)
- Notion integration
- Google Drive access
- Terminal/shell execution (requires sandbox mode)
- Browser control

## Skill Vetting Rules

Before installing any ClawHub skill:
1. Read the skill's source code entirely
2. Check for network calls to unexpected endpoints
3. Check for filesystem access outside workspace
4. Look for obfuscated code or encoded strings
5. Prefer skills with community reviews and stars
6. When in doubt, skip it — write a custom skill instead

## Model-Specific Notes

### Qwen3.5 (Current)
- Role translation needed: `developer` → `system`, `toolResult` → `tool`
- Use the proxy from github.com/ZengboJamesWang/Qwen3.5-35B-A3B-openclaw-dgx-spark
- `[think]` keyword toggles extended reasoning per-request
- Chunked transfer encoding requires proxy handling

### Ollama Quirks
- Stateless API — does NOT maintain conversation history between calls
- OpenClaw must manage full conversation context
- Check that the gateway is passing history correctly if agent seems forgetful
