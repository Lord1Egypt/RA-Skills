---
name: no-ai-tone
description: Checks and rewrites copy to eliminate AI-generated tone. Supports Chinese (中文), English, and Japanese (日本語). Triggers when writing or editing any user-facing copy — homepage text, product descriptions, marketing content, emails, social media posts, brand messaging. Activate when user says "去AI味", "去掉AI感", "听起来太AI了", "no AI tone", "humanize this", "write with human voice", "make it sound natural", "remove AI feel", "AI臭をなくして", "人間らしく書いて", or when producing any copy that will be read by real users.
---

# Avoid AI-Generated Tone

This skill loads the appropriate language guide based on the language of the content being written or edited.

## Language Routing

Detect the target language from:
1. The language of the copy being edited or generated
2. The language the user is writing in
3. An explicit instruction ("write in English / 中文で / 日本語で")

Then load the corresponding instruction file:

| Target Language | Instruction File |
|---|---|
| Chinese / 中文 | `$SKILL_DIR/instructions/zh.md` |
| English | `$SKILL_DIR/instructions/en.md` |
| Japanese / 日本語 | `$SKILL_DIR/instructions/ja.md` |

If the copy mixes languages (e.g., English product name in Chinese copy), apply the primary-language guide and spot-check vocabulary from the secondary language guide.

## How to Apply This Skill

1. **Read** the instruction file for the detected language
2. **Scan** the copy against that language's vocabulary blacklist and structural patterns
3. **Rewrite** flagged sections — produce the actual rewritten copy, not just annotations
4. **Apply** the rewrite checklist from the instruction file
5. **Self-test** using the three questions at the end of the instruction file

**Output format**: Always produce the rewritten version. Show the original and rewrite side-by-side only when explaining specific moves. Never return a list of annotations without the fixed copy.

## What Each Guide Covers

All three language guides share the same structure:
- Vocabulary blacklist (words/phrases that signal AI generation)
- Sentence structure problems (rhythm, parallelism, list addiction)
- Tone problems (hedging, no stance, emotional flatness)
- Formatting problems (bold-first bullets, em-dash overuse, fractal summaries)
- Content problems (vague without specifics, one-point dilution, fake attribution)
- Rewrite checklist (step-by-step scan)
- Before/after rewrite examples
- Three self-test questions

## Core Principle (All Languages)

The problem isn't a list of bad words. It's a **posture**: AI writing covers everything, commits to nothing, varies nothing. Good writing makes cuts, takes sides, and sounds like a specific person said it.

> Chinese: AI文章像预制菜——成分齐全、摆盘漂亮、没有锅气。
> English: AI writing is the verbal equivalent of stock photography.
> Japanese: どこを読んでも同じ温度で、感情の起伏がない。
