## Description:

A Chinese novel-writing agent skill that helps initialize fiction projects, draft and revise chapters, run writing-quality and AI-style checks, manage story state, and adapt generation to multiple publishing platforms and LLM providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xincen0725](https://clawhub.ai/user/xincen0725)

### License/Terms of Use:

MIT-0

## Use Case:

External authors and writing agents use this skill to plan Chinese web novels, generate or continue chapters, review consistency and reader experience, and maintain project state across long-form writing workflows. Developers may also use its local CLI mode for provider discovery, generation, detection, import, comparison, reports, and rollback in a dedicated writing workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly modify project files and persist writing memory, preferences, outlines, chapters, and state.

Mitigation: Install and run it only in a dedicated writing workspace with no unrelated files.

Risk: Local/provider mode can send outlines, chapters, prompts, and project state to automatically discovered LLM providers or custom endpoints.

Mitigation: Enable provider mode and set API keys only after reviewing the selected provider and avoiding untrusted custom endpoints.

Risk: Rollback and import workflows can operate on user-supplied paths.

Mitigation: Use only trusted manuscript and backup paths, and review file targets before running import or rollback commands.

Risk: Anti-detection and AI-style removal features may conflict with authorship disclosure requirements.

Mitigation: Use those features only where permitted and preserve required disclosure or attribution practices.

## Reference(s):

- [One Novel Skill on ClawHub](https://clawhub.ai/xincen0725/skills/one-novel-skill)
- [Publisher Profile](https://clawhub.ai/user/xincen0725)
- [Reference Index](references/index.json)
- [Platform Strategy](references/platform-strategy.md)
- [Writing Techniques Index](references/writing-techniques-allinone/INDEX.md)
- [Content Safety Reference](references/writing-techniques-allinone/content-safety.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, JSON state files, project files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist project memory, chapter drafts, outlines, tracking files, reports, and provider configuration in the working directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
