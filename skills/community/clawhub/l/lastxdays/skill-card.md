## Description:

Research and summarize what happened in the last N days (or a date range) about a topic, optionally using Reddit API and X ingestion via x-cli/API/archive with graceful fallback to web.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levineam](https://clawhub.ai/user/levineam)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to summarize recent activity for a topic across web results and, when configured, Reddit and X sources. It is useful for quickly identifying top themes, notable links, and follow-up searches for a recent date window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because ordinary use may access local credentials, local X archive data, and unreviewed helper or CLI code.

Mitigation: Review the skill before installing, prefer web-only source requests unless local or credentialed sources are intended, and verify x-cli packages and helper scripts before use.

Risk: Reddit and X ingestion can rely on API credentials or local configuration files.

Mitigation: Use minimally scoped API credentials, avoid storing unnecessary secrets, and confirm which credential sources are configured before running non-web ingestion.

Risk: X archive mode may read local archive data from the user's environment.

Mitigation: Use X archive mode only when that local data source is expected and appropriate for the requested research.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/levineam/skills/lastxdays)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with links, bullets, and follow-up search suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source labels for web, Reddit, and X; snippet-only items are identified when fetches are unavailable.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
