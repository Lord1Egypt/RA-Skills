## Description:

Operate Matrix Client-Server API through UXC with a curated OpenAPI schema, bearer-token auth, and homeserver-aware messaging guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure UXC for Matrix Client-Server API calls, inspect account, room, profile, and presence state, run sync polling, and perform guarded message sends against a chosen homeserver.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Matrix access token may allow the agent to read or act through the user's Matrix account.

Mitigation: Use the least-privileged token practical, store it through UXC bearer-token credentials, and verify the homeserver binding before use.

Risk: Room message sends can post visible content or create duplicate sends if retried carelessly.

Mitigation: Require explicit approval for sends, default to plain text room messages, and use a unique transaction ID for each send attempt.

Risk: Sync polling subscriptions may continue polling and store room events in local UXC subscription files.

Mitigation: Stop or remove subscriptions when no longer needed and protect local subscription outputs that may contain room event data.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/matrix-client-server.openapi.json)
- [Matrix Client-Server API](https://spec.matrix.org/latest/client-server-api/)
- [Matrix spec source](https://github.com/matrix-org/matrix-spec/tree/main/data/api/client-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is homeserver-aware and uses read-first checks before higher-risk message sends.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
