## Description:

Investigates a username across 1000+ social media platforms and websites using social-analyzer, with supplemental checks for Bilibili, Zhihu, and Weibo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guleguleguru](https://clawhub.ai/user/guleguleguru)

### License/Terms of Use:


## Use Case:

External users, security researchers, journalists, and developers use this skill to check whether a public username appears across social platforms and to summarize likely matches for legitimate OSINT or self-audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Username lookups are sent to many external services and may be sensitive when the target or purpose is ambiguous.

Mitigation: Use the skill only for legitimate public-profile checks, avoid ambiguous third-party lookups, and include a reminder that results are public information and must be used lawfully.

Risk: The setup guidance installs an unpinned package into the system Python environment with --break-system-packages.

Mitigation: Prefer installing social-analyzer in a pinned virtual environment before running investigations.

Risk: Broad cross-platform profile searches can produce uncertain matches.

Mitigation: Treat confidence scores as triage signals and require manual confirmation for medium or approximate matches.

## Reference(s):

- [Platform Coverage Reference](references/platforms.md)
- [social-analyzer](https://github.com/qeeqbox/social-analyzer)
- [OSINT Social Analyzer on ClawHub](https://clawhub.ai/guleguleguru/skills/osint-social)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style conversational summaries with profile links, confidence scores, and setup or command guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence tiers, public profile metadata, and privacy or legality reminders.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
