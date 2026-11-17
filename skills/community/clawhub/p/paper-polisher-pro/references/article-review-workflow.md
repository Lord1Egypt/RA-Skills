<!-- 何时读我：想把本工具的检测/建议嵌入一篇论文的完整审阅流程时。
     最短路径：SKILL.md § Quick start → 本文的四步流程。
     回 INDEX：SKILL.md § 30-second task routing -->

# Article Review Workflow (Terminology + AI Detection + Metaphor Audit)

> Three-task parallel review for medical/scientific articles before publication.

## Workflow Sequence

### Phase 1: Parallel Tool Runs (do these simultaneously)

```bash
# Task A: Terminology check
python3 scripts/term_check.py <article.md>

# Task B: AI detection with JSON output
python3 scripts/ai_detector.py <article.md> --lang auto --format json --output /tmp/ai_report.json
```

### Phase 2: Metaphor/Analogy Audit (manual, by agent)

Extract ALL metaphors, analogies, and figurative language from the article. For each:

| Field | What to assess |
|-------|---------------|
| Location | Chapter/section + line number |
| Quoted text | The exact metaphor |
| Scientific accuracy | Does the analogy correctly represent the underlying biology/medicine? |
| Appropriateness | Is it suitable for the target audience? (e.g., peer physicians vs. lay public) |
| Verdict | ✅ Keep / ⚠️ Modify / ❌ Remove |

#### Metaphor Quality Criteria

1. **Accuracy first**: The analogy must not distort the science. Example: "alarmin = smoke alarm" is accurate because alarmins signal danger without being the danger itself.
2. **Consistency**: Maintain one imagery system per concept thread. Mixing metaphors (e.g., "car engine" → "fire" → "gasoline") breaks coherence. Fix by picking one system and sticking with it.
3. **No over-explanation**: State the metaphor once. Don't add "you can't just pretend..." follow-up sentences that explain the metaphor to death.
4. **Audience match**: For peer physicians, metaphors should illuminate mechanism, not dumb it down. Avoid overly literary/poetic phrasing in clinical sections.

### Phase 3: Present Findings (concise!)

Present a single consolidated table to the user. Do NOT write a long essay.
- **Keep it actionable**: table format with verdict + specific fix
- **Get confirmation before patching**: list all proposed changes, ask once, execute all
- **Don't make the user ask "进度?"** — if the report is ready, say so immediately

### Phase 4: Execute Patches

Apply all confirmed changes, then re-run tools to verify improvement.

## AI Detection: What's Worth Fixing

Not every 50+ paragraph needs rewriting. Prioritize:

1. **Model fingerprints** (DeepSeek/GLM/Qwen specific patterns) — highest priority, always fix
2. **Classic AI openers** ("值得注意的是", "综上所述", "在此基础上") — easy wins
3. **RLHF alignment patterns** — fix if concentrated in one section
4. **Markdown bold patterns** — ignore, these are formatting not AI tells

## Metaphor Audit: Common Pitfalls

| Pitfall | Example | Fix |
|---------|---------|-----|
| Mixed imagery systems | "油门卡死" then "火上浇油" | Pick one system (engine → "第二台发动机") |
| Over-explained metaphor | "like X. You can't just pretend Y isn't happening." | Delete the explanation sentence |
| Literary excess in clinical text | "面纱" + "狰狞的脸" | Simplify to direct language ("伪装") |
| Chains too long | A→B→C→D extended metaphor | Cut to A→B, max |
| Scientifically inaccurate | Any analogy that misrepresents pathophysiology | Rewrite or remove |