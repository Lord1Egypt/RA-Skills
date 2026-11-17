## Description:

Obtain temporary Lix API tokens via CLI with human email approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aakarim](https://clawhub.ai/user/aakarim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need authenticated access to Lix APIs for enrichment or other Lix service requests and do not already have a valid token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install or invoke an authentication CLI from an unpinned distribution path.

Mitigation: Use a pinned and verified lix-agents CLI release before installation or execution.

Risk: The token request prints a temporary bearer token to stdout, which can be captured in logs or transcripts.

Mitigation: Keep tokens out of logs and transcripts where possible, limit handling to the current task, and revoke or let temporary tokens expire after use.

Risk: Login creates local session state for the Lix CLI.

Mitigation: Review local session behavior before installing and use the skill only when the publisher and CLI distribution path are trusted.

## Reference(s):

- [Lix API Docs](https://lix-it.com/docs)
- [lix-agents GitHub Releases](https://github.com/lix-it/lix-agents/releases)
- [ClawHub Skill Page](https://clawhub.ai/aakarim/skills/lix-agents)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and authorization header guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or expose a temporary bearer token after user email approval.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
