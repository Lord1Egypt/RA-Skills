# Deep Research Guide for Persona Distillation

## Research Depth by Entry Type

### Type 1: Named Person
- Search: `"[name] thinking style"` `"[name] thinking model"` `"[name] decision making"`
- Search: `"[name] quotes"` `"[name] principles"`
- Search: `"[name] biography key lessons"`
- Search: `"[name] mental models"`
- Source depth: Biographies, interviews, letters, speeches, books they wrote
- Target: Extract 3-5 core principles, decision patterns, verbal fingerprints, value hierarchy

### Type 2: Fuzzy Requirement
- First: Diagnose need category using frameworks.md selection guide
- Second: Recommend 2-3 matching frameworks with brief rationale
- Third: Ask user to confirm direction OR select best fit based on context
- Fourth: Once confirmed, research recommended framework deeply
- Output: Framework-as-persona (not a real person, but the thinking model embodied)

### Type 3: Web Link
- Fetch full content with web_fetch
- Extract: Author viewpoint, core arguments, implied values, decision heuristics
- If article about a person: treat as Type 1
- If article about a method: treat as Type 2 + Type 4 hybrid
- Cross-reference author's other works if available
- Target: Extract 3-5 unique insights that define a persona

### Type 4: Existing Skill
- Read the SKILL.md fully
- Identify: What thinking model does this skill embody? What workflow? What values?
- Extract: Core procedure → persona habits; tool choices → persona preferences; constraints → persona boundaries
- Example: A "code-review" skill → "Meticulous Code Artisan" persona (meticulous, standards-driven)

### Type 5: Local Corpus
- Read the corpus files
- Identify: Recurring themes, decisions, worries, aspirations
- This is DISTILLATION of the USER, not an external figure
- Instead of creating a persona, identify what kind of THINKING PARTNER they need
- Then recommend/create that persona

## Information Extraction Template

For each source, fill this grid:

```
Source: [name / link / file]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Worldview: [How do they see the world?]
Values: [What do they care about most?]
Decision Heuristic: [How do they choose?]
Communication Style: [How do they talk/write?]
Signature Concepts: [What ideas are they known for?]
Weaknesses/Blind Spots: [What do they miss?]
Contradictions: [Where do they hold tension?]
Key Quotes: [3-5 most revealing quotes]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Persona Name: [Generated]
One-line Essence: [Generated]
Primary Framework: [From frameworks.md]
```

## Research Quality Standards

- **Minimum sources**: 3 distinct sources before distilling (except Type 4/5)
- **Cross-validate**: Check if key quotes are verified, not misattributed
- **Depth over breadth**: 3 principles deeply understood > 10 superficially mentioned
- **Show work**: Always present the extraction grid before generating persona files
- **User confirmation**: For Type 2, confirm framework selection before generation
- **Language**: Match user's language for persona names and vibe; Chinese for Chinese users

## Web Research Strategy

For Type 1 and Type 3, use these search patterns:

### Chinese sources
- Baidu Baike / Wikipedia ZH for biographies
- Zhihu / Douban for analysis and discussion
- WeChat Read for book excerpts

### English sources
- Wikipedia for baseline bio
- Goodreads for book quotes
- Brainyquote / Wikiquote for verified quotes
- Farnam Street / James Clear for mental model articles
- LessWrong / Effective Altruism for rationalist figures

### Cross-language
- Search in both CN and EN for non-Chinese figures
- Prioritize primary sources (their own words) over secondary analysis