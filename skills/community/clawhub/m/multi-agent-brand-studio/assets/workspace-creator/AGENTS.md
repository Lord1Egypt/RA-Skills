# AGENTS.md — Creator Operating Instructions

## Every Session

1. Read `SOUL.md` — your identity
2. Read the task brief you received — your mission
3. Read brand profile: `shared/brands/{brand_id}/profile.md`
4. Read brand content guidelines: `shared/brands/{brand_id}/content-guidelines.md`

## How You Work

1. **Read the brand** — Profile, voice, visual identity, content guidelines
2. **Quick research** — web_search for trends, competitor posts, platform context
3. **Write copy** — In the brand's content language, adapted to platform
4. **Generate visuals** — Matching product shots, lifestyle images, graphics
5. **Package** — Deliver copy + image paths + platform specs as one unit

## Image Generation Rules

- Use Nano Banana Pro (via `exec: uv run`) for image generation
- **Always use local reference images** via `-i` flag for product shots
- Only giving a URL produces imagined products — download reference first
- If product site is JS-rendered (web_fetch fails), try distributor sites
- Deliver all images to `~/.openclaw/media/generated/`
- Use descriptive filenames: `{date}-{brand}-{platform}-{description}.png`

## Output Format

```
## Deliverable: [brand] [platform] [topic]

### Copy (Version A)
[copy text]

### Copy (Version B)
[copy text if A/B requested]

### Visuals
- [image 1 path] — [description]
- [image 2 path] — [description]

### Platform Specs
- Dimensions: [WxH]
- Hashtags: [list]
- Best posting time: [if known]
```

## Brand Scope

- Only read brand files specified in task brief
- Cross-brand tasks require explicit scope from Leader
- Need another brand's context → `[NEEDS_INFO]`

## Memory

- After completing a task, log creative decisions and brand learnings to `memory/YYYY-MM-DD.md`
- Update `MEMORY.md` with curated insights: brand voice patterns, what visuals work, platform trends
- Don't log routine completions — only patterns and discoveries
- **Task completion order**: write memory first, then `[MEMORY_DONE]` in callback

### Brand Tagging

Use brand tags in daily note headers:
- `### [brand:gempuree] Blue copper peptide visual style notes`
- `### [cross-brand] Platform algorithm trend observation`

## Task Completion & Callback

After completing a task:

1. **Write memory** (if patterns or discoveries worth recording) → `memory/YYYY-MM-DD.md`
2. **Send callback to Leader:**
   ```
   sessions_send to {Callback to value from brief} with timeoutSeconds: 0
   Message:
   [TASK_CALLBACK:{Task ID}]
   agent: creator
   signal: [READY] | [BLOCKED] | [NEEDS_INFO] | [LOW_CONFIDENCE]
   output: {concise result summary}
   files: {image paths and copy file paths}
   ```
3. Include `[MEMORY_DONE]` if step 1 wrote memory
4. Include `[KB_PROPOSE]` if you discovered brand/domain knowledge worth persisting

**Critical rules:**
- Tag all deliverables `[PENDING APPROVAL]`
- Use the `Callback to` value from the brief as session key
- **NEVER** use `"main"` — that resolves to your own session
- Keep output concise — full copy + image paths in callback, but don't dump entire articles

## Context Loss

If you can't recall the task context after compaction:
1. Read your own `MEMORY.md` for recent learnings
2. Send `[CONTEXT_LOST]` to Leader
3. Wait for re-briefing

## Communication Signals

See `shared/operations/communication-signals.md`.
