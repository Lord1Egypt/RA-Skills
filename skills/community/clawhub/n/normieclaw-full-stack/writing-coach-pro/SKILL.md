# Writing Coach Pro — Agent Skill

> Your writing gets better every session. Not because you memorized rules, but because your agent learned how you write.

## Description

Writing Coach Pro turns your OpenClaw agent into a persistent writing coach that analyzes, improves, and learns from your writing over time. It checks grammar, enforces style consistency, scores readability, and rewrites text — all while remembering your preferences across sessions.

## Trigger Phrases

Use when the user asks to:
- Review, edit, proofread, or polish writing
- Check grammar, style, or tone
- Rewrite or rephrase text
- Score readability or grade level
- Check document consistency
- Set writing preferences or style guide
- View writing stats or improvement trends
- "Coach me on this" or "explain why this is wrong"

Do NOT use for:
- Generating content from scratch (that's content creation, not coaching)
- Translation
- Plagiarism detection
- Summarization (use summarize skill)

---

## 1. Style Profile System

The style profile is what makes Writing Coach Pro different from every other writing tool. It persists across sessions and evolves as the user writes.

### Profile Location

Store the active profile at: `~/.openclaw/skills/writing-coach-pro/config/settings.json`

### Profile Structure

The profile tracks these dimensions:

**Style Guide**: Which authority governs mechanical choices.
- Options: `ap` (AP Stylebook), `chicago` (Chicago Manual of Style), `apa` (APA 7th Edition), `custom`
- Default: `ap`
- Affects: serial comma usage, title capitalization, number formatting, abbreviation rules, date formatting

**Tone**: The user's preferred voice.
- Scale: `formal` → `professional` → `conversational` → `casual`
- Default: `professional`
- Per-context overrides supported (e.g., emails = conversational, reports = formal)

**Vocabulary Level**: Complexity of word choice.
- Scale: `simple` (6th grade) → `standard` (10th grade) → `advanced` (college) → `technical` (domain-specific)
- Default: `standard`

**Sentence Length Target**: Average words per sentence.
- Range: 10-30 words
- Default: 18
- Agent tracks actual average and nudges toward target

**Active Voice Preference**: How aggressively to flag passive constructions.
- Options: `strict` (flag all), `moderate` (flag when active is clearer), `relaxed` (only flag when passive obscures meaning)
- Default: `moderate`

**Custom Rules**: User-specific preferences the agent has learned.
- Stored as an array of rule objects: `{ "rule": "description", "source": "learned|manual", "confidence": 0.0-1.0 }`
- Example: `{ "rule": "Always use Oxford comma", "source": "learned", "confidence": 0.95 }`
- Example: `{ "rule": "Prefer 'use' over 'utilize'", "source": "manual", "confidence": 1.0 }`

### Profile Discovery

When a new user has no profile, run a discovery flow:

1. Ask: "What kind of writing do you do most? (emails, reports, blog posts, creative, academic, technical)"
2. Ask: "Do you follow a style guide? (AP, Chicago, APA, or none/custom)"
3. Ask: "How would you describe your tone? (formal, professional, conversational, casual)"
4. Set defaults based on answers and save to `settings.json`
5. Tell the user: "Got it. I'll refine these as we work together — the more you write, the better I get."

If the user skips discovery, use defaults and learn from their first few submissions.

### Profile Updates

The profile updates through two mechanisms:

**Explicit**: User says "I prefer Oxford commas" or "Stop flagging my sentence fragments" → update immediately with `confidence: 1.0`.

**Implicit (Learning Loop)**: Track suggestion acceptance/rejection patterns. After 3+ consistent signals on the same suggestion type, update the profile automatically. See Section 6 for the full learning loop.

---

## 2. Analysis Pipeline

Every piece of text runs through a multi-pass pipeline. Each pass is independent and produces its own findings. The agent assembles findings into a unified report.

### Pass 1: Grammar & Mechanics

Check for:
- Spelling errors (context-aware — "their/there/they're" resolved by meaning)
- Punctuation errors (missing commas, incorrect semicolons, misused apostrophes)
- Subject-verb agreement
- Pronoun-antecedent agreement
- Run-on sentences and comma splices
- Sentence fragments (flag only if style profile has `fragments: "flag"`)
- Misplaced or dangling modifiers
- Incorrect word usage (affect/effect, fewer/less, who/whom)

Output format per finding:
```
[GRAMMAR] Line/location → Issue description → Suggested fix
```

### Pass 2: Style & Word Choice

Check for:
- Wordiness: "in order to" → "to", "at this point in time" → "now", "due to the fact that" → "because"
- Redundancies: "absolutely essential" → "essential", "past history" → "history"
- Clichés: "think outside the box", "at the end of the day", "low-hanging fruit"
- Weak verbs: overuse of "is/was/are/were" when stronger verbs exist
- Nominalization: "make a decision" → "decide", "give consideration to" → "consider"
- Adverb overuse: flag adverbs that weaken rather than strengthen ("very", "really", "quite", "actually")
- Jargon level: flag if vocabulary doesn't match the profile's vocabulary level setting
- Sentence variety: flag if 3+ consecutive sentences start the same way or follow the same structure

Apply the user's style guide rules from their profile. For example:
- AP style: numbers under 10 spelled out, no Oxford comma (unless user overrides), "%" not "percent" in most contexts
- Chicago: numbers under 100 spelled out, Oxford comma required
- APA: numbers under 10 spelled out, specific heading formats

Output format per finding:
```
[STYLE] Location → Current text → Suggested revision → Rule/reason
```

### Pass 3: Tone Analysis

Evaluate the overall tone and flag mismatches with the user's profile:
- Detect: confident, tentative, aggressive, friendly, neutral, formal, casual, passive-aggressive
- Flag tone shifts within a document (paragraph 2 is formal, paragraph 5 is suddenly casual)
- Flag tone mismatches with stated context (a professional email that reads as too casual)
- Identify hedging language: "I think maybe we could possibly consider..."
- Identify overly aggressive phrasing: "You need to do this immediately" in a peer email

Output:
```
[TONE] Overall tone: [detected] | Target tone: [from profile] | Mismatches: [list]
```

### Pass 4: Readability Scoring

Calculate all metrics (see Section 4 for formulas and interpretation):
- Flesch-Kincaid Grade Level
- Flesch Reading Ease
- Average sentence length (words)
- Average word length (syllables)
- Passive voice percentage
- Adverb density (adverbs per 100 words)
- Sentence complexity distribution (simple, compound, complex, compound-complex)

Compare against the user's target readability from their profile.

Output:
```
[READABILITY] Grade Level: X | Reading Ease: Y | Avg Sentence: Z words
Passive Voice: N% | Adverb Density: N per 100 words
Target: [user's target] | Status: [on target / above / below]
```

### Pass 5: Document Consistency

Only runs on texts longer than 200 words. Checks for:
- Terminology shifts (see Section 5 for full list)
- Capitalization inconsistencies
- Hyphenation inconsistencies ("e-mail" vs "email" within same doc)
- Number formatting ("10" vs "ten" within same context)
- Tense shifts (past → present without clear reason)
- Voice shifts (active → passive patterns)

Output:
```
[CONSISTENCY] Issue type → First usage → Conflicting usage → Recommendation
```

---

## 3. Feedback Modes

The agent operates in one of four modes based on user request. Default to Quick Review unless the user specifies otherwise.

### Quick Review

**Trigger**: "check this", "proofread this", "quick review", or any short text (<300 words) without mode specification.

**What it does**: Runs Pass 1 (Grammar) only, plus any critical issues from Pass 2 (egregious wordiness, wrong word usage). Skips tone, readability, and consistency.

**Output format**: Concise, inline corrections. No scores, no metrics. Just fixes.

Example output:
```
Found 3 issues:
1. "their" → "there" (paragraph 2) — wrong word
2. "me and John" → "John and I" (paragraph 1) — pronoun case
3. "very unique" → "unique" (paragraph 3) — unique is absolute, no degree modifier needed
```

### Full Review

**Trigger**: "full review", "review this thoroughly", "analyze my writing", or any text >500 words without mode specification.

**What it does**: Runs all 5 passes. Produces a structured report with scores.

**Output format**:

```
## Writing Analysis Report

### Summary
[2-3 sentence overall assessment]

### Readability
- Grade Level: X (target: Y)
- Reading Ease: Z/100
- Avg Sentence Length: N words
- Passive Voice: N%
- Adverb Density: N/100 words

### Grammar & Mechanics (N issues)
[List each issue with fix]

### Style (N suggestions)
[List each suggestion with before/after]

### Tone
[Overall assessment, any mismatches]

### Consistency (N issues)
[List any inconsistencies found]

### Top 3 Priorities
[The three most impactful changes to make]
```

Always end with "Top 3 Priorities" — the user's attention is finite. Surface what matters most.

### Rewrite Mode

**Trigger**: "rewrite this", "polish this", "make this better", "clean this up".

**What it does**: Runs all passes silently, then produces a rewritten version that applies all suggestions while preserving the user's voice (per their style profile).

**Output format**:
1. The full rewritten text
2. A brief summary of what changed and why (collapsed/below the rewrite)
3. If multiple options exist for a section, present 2-3 alternatives

**Rules for rewrites**:
- Never change the meaning or core message
- Preserve the user's vocabulary level and tone preferences from their profile
- Don't make everything sound the same — preserve stylistic choices that are intentional
- When in doubt about whether something is a stylistic choice or an error, ask

### Coach Mode

**Trigger**: "coach me", "explain this", "teach me", "why is this wrong", "writing lesson".

**What it does**: Runs all passes but presents findings as teaching moments, not corrections. Explains the rule behind each suggestion, gives examples, and connects feedback to the user's growth.

**Output format per issue**:
```
### [Issue Title]
**What I found:** [the text in question]
**The principle:** [explain the grammar/style rule and why it matters]
**The fix:** [suggested revision]
**Example in the wild:** [a published example of this principle done well]
**Your pattern:** [if this is a recurring issue, note that — "I've seen this in your last 3 reviews"]
```

Coach Mode is designed to make the user a better writer, not just produce better text. It's the mode that builds loyalty because users learn something every time.

---

## 4. Readability Scoring

### Flesch-Kincaid Grade Level

Formula: `0.39 × (total words / total sentences) + 11.8 × (total syllables / total words) - 15.59`

Ranges: 5-6 (elementary) → 7-8 (middle school) → 9-10 (high school) → 11-12 (college prep) → 13-16 (college) → 17+ (professional)

### Flesch Reading Ease

Formula: `206.835 - 1.015 × (total words / total sentences) - 84.6 × (total syllables / total words)`

Ranges: 90-100 (very easy, 5th grade) → 60-69 (standard, 8th-9th) → 30-49 (difficult, college) → 0-29 (professional)

### Target Recommendations by Context

- **Marketing copy**: Grade 6-8, Reading Ease 70-80
- **Blog posts**: Grade 7-9, Reading Ease 60-70
- **Business emails**: Grade 8-10, Reading Ease 55-65
- **Technical docs**: Grade 10-12, Reading Ease 40-55
- **Academic papers**: Grade 12-16, Reading Ease 30-50
- **Legal writing**: Grade 14+, Reading Ease 20-40

### Additional Metrics

**Passive Voice Percentage**: Count sentences with passive constructions / total sentences × 100. Target: below 15% for most writing. Academic writing may tolerate 20-25%.

**Adverb Density**: Count adverbs / total words × 100. Target: below 5%. Above 8% is excessive for any context.

**Sentence Length Distribution**: Categorize every sentence:
- Short: 1-10 words
- Medium: 11-20 words
- Long: 21-35 words
- Very long: 36+ words

Healthy distribution has variety. Flag if >40% of sentences fall in any single bucket.

---

## 5. Document Consistency Checks

### Terminology

Build a term map as you read the document. Flag when:
- The same concept uses different words: client/customer, app/application, use/utilize
- Proper nouns change capitalization: "internet" vs "Internet"
- Acronyms are used before being defined, or defined multiple times
- Product names are inconsistent: "macOS" vs "MacOS" vs "Mac OS"

### Capitalization

Check for:
- Title case vs. sentence case in headings (should be consistent throughout)
- Inconsistent capitalization of terms: "Agile" vs "agile" (pick one per document)
- Proper noun handling

### Hyphenation

Flag inconsistencies:
- "e-mail" vs "email"
- "on-line" vs "online"
- Compound modifiers: "well-known fact" but "the fact is well known" (hyphenation rules)

### Number Formatting

Per the user's style guide:
- Spell out vs. numerals threshold (AP: under 10, Chicago: under 100)
- Percentages: "50%" vs "50 percent" vs "fifty percent"
- Currency: "$1,000" vs "$1000" vs "one thousand dollars"
- Dates: "March 11, 2026" vs "3/11/2026" vs "11 March 2026"

### Tense Consistency

Track the dominant tense per section. Flag shifts that appear unintentional:
- Past tense narrative suddenly switching to present
- Mixing "will" (future) with "would" (conditional) without clear reason

### Voice Consistency

Track active vs. passive ratio per section. Flag if one section is 90% active and another is 60% passive without clear reason (e.g., a methods section in academic writing legitimately uses more passive).

---

## 6. Learning Loop

The learning loop is what makes Writing Coach Pro improve over time. It tracks patterns in user behavior and adapts the style profile.

### What Gets Tracked

Store in `~/.openclaw/skills/writing-coach-pro/data/learning-log.json`:

```json
{
  "suggestions": [
    {
      "date": "2026-03-11",
      "type": "style",
      "rule": "oxford_comma",
      "suggestion": "Add comma before 'and'",
      "accepted": false,
      "context": "email"
    }
  ],
  "sessions": [
    {
      "date": "2026-03-11",
      "wordCount": 450,
      "issuesFound": 7,
      "issuesAccepted": 5,
      "mode": "full_review",
      "readabilityScore": 62
    }
  ]
}
```

### Acceptance Detection

How to know if a suggestion was accepted or rejected:
- **Accepted**: User says "fix it", "yes", "apply that", "good catch", uses the rewritten version, or doesn't object
- **Rejected**: User says "no", "ignore that", "I meant to write it that way", "skip", or re-submits text without the suggested change
- **Unclear**: If the user doesn't respond to a specific suggestion, don't count it either way

### Profile Update Rules

- After 3 rejections of the same rule type → reduce that rule's priority (add to custom rules with `"action": "suppress"`)
- After 5 acceptances of the same suggestion type → increase confidence, reinforce in profile
- After 10+ sessions → generate a "style fingerprint" summary: "You tend to write at a 9th grade level with a conversational tone. You prefer active voice and short sentences. Your most common issues are comma splices and adverb overuse."
- Never fully remove a grammar rule — only suppress style preferences. "Their/there" is always wrong regardless of preference.

### Feedback to User

Every 10 sessions (or on request), offer a progress report:
```
## Your Writing Progress

Sessions analyzed: 47
Total words reviewed: 23,400

### Trends
- Your average readability has improved from grade 12 to grade 9
- Passive voice usage dropped from 22% to 11%
- You've eliminated most adverb overuse — down from 8.2 to 3.1 per 100 words

### Consistent Strengths
- Strong active voice
- Good sentence variety
- Effective use of transitional phrases

### Areas to Watch
- Comma splices still appear (flagged in 6 of last 10 sessions)
- Tendency toward nominalizations in formal writing

### Your Style Profile
[Display current profile settings]
```

---

## 7. Dashboard Integration

Writing Coach Pro feeds data to the NormieClaw dashboard (if installed). The dashboard kit is in `dashboard-kit/`.

### Data Tables

Three tables (full schemas in `dashboard-kit/manifest.json`):

- **`wc_sessions`**: One row per review session — date, mode, word count, issues found/accepted, readability metrics, context type
- **`wc_issues`**: Individual issues across all sessions — linked to session, categorized by pass (grammar/style/tone/consistency), tracks acceptance
- **`wc_profile_history`**: Style profile change log — what changed, old/new values, whether learned or manual

### Dashboard Route & Sync

Route: `/writing-coach` — displays stat cards (sessions, words, grade level, acceptance rate), readability trend line, issue category breakdown, acceptance rate over time, and a recent sessions table.

After each review session, write a summary row to `wc_sessions` and individual findings to `wc_issues`. Update `wc_profile_history` whenever the style profile changes. See `dashboard-kit/DASHBOARD-SPEC.md` for full layout.

---

## 8. Commands Reference

- `review [text]` — Quick Review (default)
- `full review [text]` — Full 5-pass analysis
- `rewrite [text]` — Produce improved version
- `coach [text]` — Teaching mode with explanations
- `set style [ap|chicago|apa|custom]` — Change style guide
- `set tone [formal|professional|conversational|casual]` — Change tone preference
- `set readability [grade level]` — Set target readability
- `show profile` — Display current style profile
- `edit profile` — Interactively modify profile settings
- `show progress` — Display writing improvement stats
- `export report` — Generate analysis report (runs `export-report.sh`)
- `style check [file]` — Consistency scan on a file (runs `style-check.sh`)

---

## 9. Output Formatting Rules

### For Telegram/Discord/WhatsApp
- No markdown tables — use bullet lists
- Keep responses under 4000 characters when possible
- Use bold for issue types, regular text for details
- Collapse detailed analysis behind a summary

### For Terminal/CLI
- Markdown tables are fine
- Use code blocks for before/after comparisons
- Color coding via terminal formatting if supported

### Universal
- Always lead with a summary count: "Found 7 issues (3 grammar, 2 style, 1 tone, 1 consistency)"
- Always end Full Review with "Top 3 Priorities"
- In Rewrite Mode, present the rewrite first, explanation second
- In Coach Mode, present the teaching point first, the fix second

---

## 10. Edge Cases

### Very Short Text (<20 words)
- Skip readability scoring (not meaningful for short text)
- Skip consistency checks
- Only run grammar pass
- Don't run discovery flow on a one-liner

### Very Long Text (>5000 words)
- Warn the user: "This is a long document — full analysis will take a moment."
- Run consistency checks with higher priority (long docs have more drift)
- Break the report into sections rather than one massive output
- Offer to analyze section by section

### Code Mixed with Prose
- Detect code blocks (```, indented blocks) and skip them for grammar/style analysis
- Still analyze comments within code blocks
- Readability scores should exclude code

### User Disagrees with a Suggestion
- Accept gracefully: "Got it — I'll remember that preference."
- Update the learning log with a rejection
- If the user explains why, capture the reasoning in custom rules
- Never argue or repeat a dismissed suggestion in the same session

### No Style Profile Exists
- Use sensible defaults (AP style, professional tone, standard vocabulary, 18-word sentences)
- Run the discovery flow at the end of the first review, not before — let the user see value first
- Say: "I used default settings for this review. Want to customize your style profile for better results next time?"

---

## 11. Integration with Other Skills

Writing Coach Pro works well alongside:

- **Content Creation skills**: Run content through Writing Coach after drafting
- **Email skills**: Auto-review outgoing emails before sending (if user opts in)
- **Report generation**: Apply style consistency to generated reports

The agent should suggest Writing Coach review when it detects the user is working on writing-heavy tasks, but never force it. A gentle "Want me to run this through Writing Coach before you send it?" is appropriate.

---

## 12. File Locations

| Path | Purpose |
|------|---------|
| `~/.openclaw/skills/writing-coach-pro/config/settings.json` | Style profile |
| `~/.openclaw/skills/writing-coach-pro/data/learning-log.json` | Learning loop data |
| `~/.openclaw/skills/writing-coach-pro/data/session-history/` | Per-session detailed logs |
| `~/.openclaw/skills/writing-coach-pro/reports/` | Exported analysis reports |
