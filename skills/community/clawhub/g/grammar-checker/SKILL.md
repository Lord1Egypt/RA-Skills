---
name: grammar-checker
description: AI-powered English grammar, spelling, and style checker. 
---

# Grammar Checker

## Overview

Check and improve English text for grammar, spelling, punctuation, style, and clarity. For each issue found, explain the error and provide a corrected version.

## Use Cases

Use when the user asks to "check grammar", "fix grammar errors", "check spelling", "improve writing", "grammar checker", "check my text", "proofread", "English grammar check", or when they paste text and ask to find errors. Also use for style suggestions, clarity improvements, and punctuation corrections. Supports emails, essays, blog posts, business documents, and any English writing.

## How to Use

1. Receive the user's text
2. Analyze it using the detailed grammar categories in `references/check_categories.md`
3. For each issue found, report:
   - **Category**: Grammar / Spelling / Punctuation / Style / Clarity
   - **Original**: the problematic text
   - **Explanation**: why it's an error
   - **Correction**: the recommended fix
4. Provide a fully corrected version at the end

## Output Format

```
## 🔍 Grammar Check Report

### Errors Found: N

---

**1. [Category] — [Error Type]**
> "Original text with error"
**Why it's wrong:** Explanation
**Fix:** "Corrected text"

---

### ✏️ Full Corrected Version
[Complete corrected text]

### 📝 Summary
- Grammar issues: N
- Spelling issues: N
- Punctuation issues: N
- Style suggestions: N
- Clarity improvements: N
```

## Response Guidelines

- Be precise: quote the exact original phrase/word in the report
- Explain briefly: one clear sentence per error explaining the rule
- Correct confidently: if unsure, mark as "sounds awkward" rather than wrong
- Keep corrections conservative: don't over-edit — preserve the author's voice and meaning
- Prioritize clarity: prefer shorter, clearer sentences over complex rewrites
- For very long texts (>1000 words), summarize key patterns and provide a partial corrected version + overall feedback
