---
name: Intelligence Ingestion
description: "Auto-analyze URLs/info for OpenClaw strategic value, classify, create Obsidian notes, update memory. Use when user shares a URL, article, tweet, or any external info source."
---

# Intelligence Ingestion Skill

When the user shares a URL, article, tweet, thread, or any piece of external information, execute this pipeline automatically. Do NOT ask for permission — just process it.

## Trigger Conditions

**USE this skill when:**
- User sends a URL (x.com, github.com, any domain)
- User pastes article text or tweet content
- User says "analyze this", "evaluate this", "what do you think about this"
- User forwards content from Telegram or any messaging surface
- User shares something and asks about strategic value

**DO NOT USE when:**
- User is asking a general question unrelated to external content
- User is asking about internal workspace files
- User explicitly says they don't want analysis

## Pipeline Steps

### Step 1: READ — Extract Content
1. If a URL is provided, read the full content (use `read_url_content` or browser)
2. If text is pasted, use it directly
3. If X/Twitter link fails to parse (common), search web for the tweet content

### Step 2: CLASSIFY — What Is This?
Assign **one primary category** and up to 2 secondary tags:

| Category | Description | Examples |
|----------|------------|---------|
| `infra` | Infrastructure / protocols / networking | Pilot Protocol, MCP, networking stacks |
| `strategy` | Routing / cost / architecture decisions | Model routing, multi-account, fallback chains |
| `skill` | Agent skills / tools / capabilities | OpenAI Skills, Skill design patterns |
| `theory` | Conceptual frameworks / mental models | Bayes, decision theory, learning loops |
| `tutorial` | How-to guides / learning material | Claude Code, OpenClaw tutorials |
| `product` | Tools / apps / services | LM Studio, new AI models, apps |
| `community` | OpenClaw ecosystem / discussions | Community posts, feature requests |
| `threat` | Risks / security / deprecation | API changes, breaking updates, security alerts |

### Step 3: ANALYZE — Strategic Value Assessment

For each piece of information, evaluate:

```markdown
## Strategic Assessment
- **What is it?** [One sentence]
- **What can it do for us?** [Specific capability/benefit]
- **What can we build with it?** [Concrete output/project]
- **Strategic value:** [🔴 Critical / 🟡 High / 🟢 Medium / ⚪ Low]
- **Competitive edge:** [What advantage over people who don't have this?]
- **Relation to active bottleneck:** [Does it relate to context overflow/token saving?]
```

Reference the current engineering bottleneck from `MEMORY.md` → "Active Engineering Bottleneck" section.

### Step 4: MAP — Relate to Existing Architecture

Check against the OpenClaw stack:
```
SOUL.md → PRINCIPLES.md → AGENTS.md (Identity Stack)
MEMORY.md (System State + Bottleneck)
TOOLS.md (Coprocessors: Codex, Antigravity, LM Studio)
Pilot Protocol (Context Separation Layer - P0)
```

Determine which layer this information impacts and note dependencies/synergies with existing components.

### Step 5: STORE — Write Obsidian Note

Create a note at:
```
/Volumes/T7 Shield/Obsidian_Vault/20_Intelligence/YYYYMMDD_AuthorOrSource_ShortTitle.md
```

Follow this template exactly:
```markdown
# [Title]

**Source:** [Link](URL)
**Date:** YYYY-MM-DD
**Category:** [Primary Category] / [Secondary Tags]
**Strategic Value:** [🔴/🟡/🟢/⚪] + one-line reason
**Relation to Active Bottleneck:** [Yes/No + how]

---

## Summary
[2-3 paragraphs of core content]

## Key Takeaways
[Numbered list of actionable insights]

## Impact on OpenClaw Architecture
[How this relates to our stack]

## Action Items
[What to do next, if anything]

---

**Keke's Note:** [Opinionated analysis in Keke's voice — direct, no-BS, relate to 阳哥's goals]
```

### Step 6: REMEMBER — Update Memory

1. **Always** append to today's daily log: `~/.openclaw/workspace/memory/YYYY-MM-DD.md`
2. **If strategic value is 🔴 Critical**: Also update `MEMORY.md` (Pending Work or Active Bottleneck)
3. **If it suggests a new principle**: Flag for potential `PRINCIPLES.md` update
4. **If it's a new tool/service**: Flag for potential `TOOLS.md` update

### Step 7: RESPOND — Summarize to User

Reply with a concise summary:
```
📥 已摄取: [Title]
📂 类别: [Category]
🎯 战略价值: [🔴/🟡/🟢/⚪] [One-line reason]
💾 已存档: Obsidian → 20_Intelligence/[filename]
📝 已记录: memory/YYYY-MM-DD.md
🔗 关联: [Which existing component it relates to]
⚡ 建议行动: [Next step, if any]
```

## Edge Cases

- **Multiple URLs in one message**: Process each separately, create separate Obsidian notes
- **Duplicate/similar content**: Check if similar note exists, merge or reference instead of duplicating
- **Non-English content**: Analyze in original language, write notes in Chinese (matching existing vault style)
- **Paywalled/inaccessible content**: Note as "content unavailable" and work with whatever user provided
- **User provides their own analysis**: Incorporate their judgment, don't overwrite — they know their system best

## Quality Checklist

Before completing, verify:
- [ ] Obsidian note created with correct filename format
- [ ] Daily memory log updated
- [ ] Source URL preserved in note
- [ ] Strategic value assessed against current bottleneck
- [ ] Keke's Note written with genuine analysis (not generic)
- [ ] User received confirmation summary
