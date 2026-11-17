## Description:

短剧爆款预演器 analyzes short-drama scripts using the configured OpenClaw AI model or a local fallback, producing hook-strength scores, suspense analysis, hit-potential predictions, simulated audience comments, emotion heatmaps, and platform adaptation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makclaw](https://clawhub.ai/user/makclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, producers, and developers use this skill to evaluate short-drama scripts for likely audience retention, suspense, shareability, and fit for platforms such as Douyin, Bilibili, Kuaishou, and Xiaohongshu. It helps generate script-improvement guidance, simulated audience reactions, and platform-specific publishing suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send submitted scripts to the user's configured external AI provider.

Mitigation: Use it only with script content that is acceptable to share with that provider, and review provider configuration before execution.

Risk: Diagnostics may expose part of an API key in shared logs.

Mitigation: Avoid running diagnostic commands in shared logs until the API-key-prefix output is fixed.

Risk: Generated results can include an embedded promotional link that was flagged as unaudited external content.

Mitigation: Review generated reports before sharing and treat the promotional link as untrusted external content.

Risk: AI-generated hit predictions and simulated comments may be inaccurate or misleading.

Mitigation: Use the output as planning guidance, then validate with human editorial review and real platform testing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/makclaw/skills/hit-preview)
- [Publisher Profile](https://clawhub.ai/user/makclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts script text or a script file plus platform options; requires Node.js and may call the user's configured AI provider.]

## Skill Version(s):

1.0.2 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
