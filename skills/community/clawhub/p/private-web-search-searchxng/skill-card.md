## Description:

Self-hosted private web search using SearXNG for privacy-sensitive searches when external search APIs are blocked, paid, or undesirable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelpro](https://clawhub.ai/user/adelpro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run a local SearXNG service and retrieve JSON web search results through curl, jq, or the helper script without relying on paid search APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned persistent SearXNG Docker image and exposes the service on port 8080.

Mitigation: Pin the SearXNG image by digest, bind the service to 127.0.0.1, and review container settings before deployment.

Risk: Installation and setup commands include npx and Docker operations that can change the local environment.

Mitigation: Run installation and Docker commands with least privilege and review the artifact before execution.

Risk: The helper script has weak handling for its result-limit argument.

Mitigation: Treat the limit as numeric-only and validate it before use until the helper script is fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adelpro/skills/private-web-search-searchxng)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands and JSON search-result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker, curl, and jq; queries a local SearXNG endpoint.]

## Skill Version(s):

1.3.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
