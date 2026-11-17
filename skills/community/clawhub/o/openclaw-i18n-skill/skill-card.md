## Description:

Internationalization and localization layer for OpenClaw that auto-detects language, enforces correct diacritics, formats dates and currency per locale, and pipes output through a post-processing cleaner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloom500](https://clawhub.ai/user/bloom500)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to localize agent responses for Romanian and German, including language detection, diacritics correction, locale-aware formatting, and response post-processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist language preferences and rewrite all agent output before the user sees it.

Mitigation: Use it in a constrained or opt-in workflow, and avoid relying on rewritten output for code, commands, legal, medical, financial, exact quotations, or mixed-language content.

Risk: The manual install path includes unnecessary unpinned Python dependencies.

Mitigation: Prefer the ClawHub install path or pin and review dependencies before manual installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bloom500/skills/openclaw-i18n-skill)
- [Publisher profile](https://clawhub.ai/user/bloom500)
- [Project homepage](https://github.com/bloommediacorporation-lab/openclaw-i18n-skill)
- [Public documentation site](https://bloommediacorporation-lab.github.io/openclaw-i18n-skill/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist language preferences and rewrite agent output before the user sees it.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
