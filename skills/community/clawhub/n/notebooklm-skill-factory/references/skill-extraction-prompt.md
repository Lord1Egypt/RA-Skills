# Skill Extraction Prompt Template

Use this template with `notebooklm ask` to extract a SKILL.md from sources. Replace `{USER_INTENT}` with the user's description.

## Primary Prompt

```
Based on ALL the provided sources, generate a complete, production-ready SKILL.md file for a Claude Code skill that: {USER_INTENT}

## Output Format

Output the ENTIRE SKILL.md content wrapped in a single ```markdown code block. The content must:

1. Start with YAML frontmatter (--- ... ---) containing:
   - name: kebab-case skill name
   - description: Comprehensive description covering WHAT the skill does AND WHEN to trigger (specific scenarios, file types, tasks). This is the primary trigger mechanism.

2. Body written in imperative/infinitive form. Keep it concise - Claude is already smart. Only include information Claude doesn't already have. Do NOT include:
   - "Overview" or "Introduction" sections
   - "When to Use This Skill" sections in body (belongs in description)
   - Tutorial-style explanations of common knowledge
   - Multi-paragraph docstrings or comment blocks

3. Include only essential procedural knowledge, domain-specific details, and non-obvious instructions.

## Quality Standards

- Output MUST be a complete, working SKILL.md ready to save to a .claude/skills/<name>/ directory
- No placeholder text, no TODO items, no "[add content here]"
- Every instruction must be actionable
- Description field must clearly state both capabilities AND trigger conditions
- If the sources contain specific workflows, code patterns, or APIs, include them precisely
- DO NOT add any explanation before or after the code block - just the code block
```

## Alternative: Fast Iteration Prompt

For refining an existing SKILL.md based on test failure feedback:

```
The SKILL.md at [path] has the following issue when tested: {ISSUE_DESCRIPTION}

Based on the sources, rewrite the SKILL.md to fix this issue. Output the complete corrected file in a ```markdown code block. Keep everything that works, only fix what's broken.
```
