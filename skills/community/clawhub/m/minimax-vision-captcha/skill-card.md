## Description:

Uses the MiniMax vision model to analyze images and screenshots for CAPTCHA text, slider positions, visible text, and webpage element content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-nurmamat](https://clawhub.ai/user/ai-nurmamat)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation users use this skill for reviewed image OCR, screenshot analysis, and MiniMax vision prompts. CAPTCHA or slider analysis should only be used when allowed by the applicable site, account, and workflow rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable CAPTCHA or slider-challenge bypass.

Mitigation: Use it only for sites, accounts, and workflows where this analysis is explicitly allowed.

Risk: The helper script can upload unintended screenshots when no image path is provided.

Mitigation: Provide explicit, reviewed image paths and redact sensitive image content before analysis.

Risk: The helper script is reported by security evidence as having a command-injection issue.

Mitigation: Review and fix the helper before running it; prefer reviewed direct MCP calls until the issue is resolved.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and text vision results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on configured MiniMax MCP access and explicit, readable image paths.]

## Skill Version(s):

1.0.0 (source: release evidence and marketplace metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
