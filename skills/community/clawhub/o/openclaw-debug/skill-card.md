## Description:

When users encounter OpenClaw-related issues or errors, this skill searches official docs and GitHub issues first, then provides solutions for feature malfunctions, error troubleshooting, version upgrade advice, configuration questions, and known issue verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyan](https://clawhub.ai/user/skyan)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to diagnose OpenClaw issues by gathering version and platform context, checking official documentation, searching GitHub issues, and summarizing fix status or configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting details may contain tokens, private URLs, tenant names, proprietary configuration, or long stack traces that should not be exposed during public documentation or GitHub searches.

Mitigation: Redact sensitive details before using the skill or sharing search terms, while retaining only the minimum error keywords and environment context needed for diagnosis.

Risk: Issue search results or changelog matches may be outdated, incomplete, or not applicable to the user's deployed OpenClaw version and channel.

Mitigation: Confirm the user's current version and platform, compare results against official documentation and changelog entries, and present fix status with any uncertainty clearly labeled.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub Issues](https://github.com/openclaw/openclaw/issues?q=is%3Aissue)
- [OpenClaw CHANGELOG](https://raw.githubusercontent.com/openclaw/openclaw/main/CHANGELOG.md)
- [OpenClaw Debug Skill Page](https://clawhub.ai/skyan/skills/openclaw-debug)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with diagnostic summaries, issue references, upgrade recommendations, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links to official documentation, GitHub issues, and changelog entries when relevant.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
