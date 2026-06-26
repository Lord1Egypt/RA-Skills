# humanizer-cn

> Remove AI writing traces from Chinese text, making it sound natural and human-written.

**Language:** [English](README.md) · [中文](README_zh.md)

---

## English

### Overview

**humanizer-cn** is a Claude Code skill that identifies and removes AI-generated writing patterns from Chinese text, making it sound natural and human-written.

Based on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide maintained by WikiProject AI Cleanup.

### What It Detects

24 types of AI writing patterns across 4 categories:

**Content Patterns (6)**
- Exaggerated significance and legacy
- Overemphasis on media coverage
- Shallow -ing analyses
- Promotional/advertising language
- Vague attribution
- Formulaic "challenges and outlook" sections

**Language Patterns (6)**
- Overused AI vocabulary
- Verb avoidance (using complex structures instead of "是")
- Negative parallelism
- Rule of three overuse
- Synonym cycling
- False scope statements

**Style Patterns (6)**
- Dash overuse
- Bold overuse
- Inline title lists
- Title case in titles
- Emoji decoration
- Curly quotes

**Communication Patterns (6)**
- Collaboration traces ("Hope this helps!")
- Knowledge cutoff disclaimers
- Sycophantic tone
- Filler phrases
- Over-qualification
- Generic positive conclusions

### Installation

```bash
# Via ClawHub (recommended)
clawhub install humanizer-cn

# Manual
git clone https://github.com/0xcjl/cjl-humanizer-cn.git ~/.claude/skills/humanizer-cn
```

### Usage

Invoke with `/humanizer-cn` followed by text to humanize:

```
/humanizer-cn
[paste your AI-generated Chinese text here]
```

Or paste text and state your intent directly.

### Processing Flow

0. **Evaluate** — Skip if text is < 20 characters or already human-written
1. Read the input text carefully
2. Identify all AI pattern instances
3. Rewrite each problematic section
4. Ensure the revised text:
   - Sounds natural when read aloud
   - Varies sentence structure naturally
   - Uses concrete details over vague claims
   - Maintains appropriate tone
   - Uses simple structures where appropriate
5. Present the humanized version

### Quality Scoring

Rate the humanized text on a 1-50 scale:

| Dimension | What to Check | Score |
|-----------|---------------|-------|
| **Directness** | Straight facts vs. circular framing | /10 |
| **Rhythm** | Sentence length variation | /10 |
| **Trust** | Respects reader intelligence | /10 |
| **Authenticity** | Sounds like a real person | /10 |
| **Refinement** | Any unnecessary content left | /10 |

**Scale:** 45-50 = excellent, 35-44 = good, below 35 = needs revision

### Core Principles

1. **Remove filler phrases** — eliminate opening filler and hedging crutch words
2. **Break formulaic structures** — avoid binary contrasts, dramatic paragraphs, rhetorical setups
3. **Vary rhythm** — mix sentence lengths. Two items beat three. Vary paragraph endings.
4. **Trust the reader** — state facts directly, skip softening and hand-holding
5. **Delete quotable quotes** — if it sounds like a quotable statement, rewrite it

### Example

**Before (AI-sounding):**
> 新的软件更新作为公司致力于创新的证明。此外，它提供了无缝、直观和强大的用户体验——确保用户能够高效地完成目标。这不仅仅是一次更新，而是我们思考生产力方式的革命。

**After (Humanized):**
> 软件更新添加了批处理、键盘快捷键和离线模式。来自测试用户的早期反馈是积极的，大多数报告任务完成速度更快。

### Tags

`humanizer` `chinese` `text-editing` `ai-detection` `writing-improvement` `openclaw-skill` `claude-code`

### Credits

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) — WikiProject AI Cleanup
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) — reference
- [Karpathy/autoresearch](https://github.com/karpathy/autoresearch) — optimization methodology

### License

MIT
