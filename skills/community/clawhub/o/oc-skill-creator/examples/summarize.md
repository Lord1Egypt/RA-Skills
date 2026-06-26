# Example: summarize (Sub-Agent Pipeline)

The summarize skill was the first skill validated using skill-creator's 5-step process.

## Why This Skill Was Created

Existing summarization skills were locked into project-specific depth terminology (1x/5x) and didn't match real user requests ("make it short", "200 chars", "by chapter", "use emojis"). A universal summarization skill was needed.

## skill-creator Process Applied

### Step 1: Analyze "Good Results"
- Extracted patterns: Style Guide, Phase 0, sub-agent context injection
- Collected 30+ natural language request patterns from actual usage

### Step 2: Analyze "Failed Results"
- Existing limitations: depth=1x/5x only, no per-language length control, no style variants
- These limitations became the new skill's requirements

### Step 3: Write Style Guide
- Defined essence: "information restructuring", not "text compression"
- Specified preservation/compression criteria
- Defined 7 style-specific writing rules

### Step 4: Structure Workflow
- Natural language parser (Phase 0) → parameter mapping → chunk → sub-agent → merge → output

### Step 5: Split References
- `parameter-mapping.md` — 30+ natural language request → parameter mapping table
- `subagent-templates.md` — Per-style sub-agent instructions
- `output-format.md` — Per-style output specifications

## Validation Results

5 test cases:

| TC | Request | length | style | Result |
|----|---------|--------|-------|--------|
| 1 | "summarize briefly" | short | brief | ✅ 8 bullets |
| 2 | "summarize by chapter" | auto | chapter | ✅ 8 section headings |
| 3 | "use lots of emojis" | auto | emoji-rich | ✅ 25+ emojis |
| 4 | "Korean, under 200 chars" | 200 | brief | ✅ 186 chars |
| 5 | "don't miss anything" | full | comprehensive | ⚠️→fixed |

### Issue Found & Fixed
- **chapter vs comprehensive ambiguity** → chapter = 2-3 sentences per section; comprehensive = restructured prose (not copy), all important content preserved

## Final Structure

```
summarize/
├── SKILL.md                              # Minimal — delegates to references
└── references/
    ├── parameter-mapping.md              # Natural language → parameter mapping
    ├── subagent-templates.md             # Sub-agent prompt templates per style
    └── output-format.md                  # Output specs per style
```
