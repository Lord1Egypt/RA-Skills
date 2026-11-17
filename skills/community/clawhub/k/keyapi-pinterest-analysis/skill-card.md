## Description:

Discover and analyze Pinterest users, pins, boards, followers, and following by searching users, retrieving profile information, exploring pin libraries and board collections, and traversing follower and following networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, analysts, and operators use this skill to collect Pinterest profile, content, board, follower, and following data through KeyAPI and synthesize it into Pinterest intelligence reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner is broader than the Pinterest-focused description and can use a configurable KeyAPI server URL.

Mitigation: Review the requested platform and leave KEYAPI_SERVER_URL unset unless the alternate destination is trusted.

Risk: KEYAPI_TOKEN and Pinterest profile or social graph data may be exposed through local environment, .env, output, or cache files.

Mitigation: Prefer setting KEYAPI_TOKEN only for the process, avoid interactive token entry, restrict output locations, and periodically delete .keyapi-cache when retained data is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-pinterest-analysis)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI Pinterest MCP endpoint](https://mcp.keyapi.ai/pinterest/mcp)
- [Artifact-declared repository](https://github.com/EchoSell/keyapi-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or higher and a KEYAPI_TOKEN; the runner can cache API responses locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
