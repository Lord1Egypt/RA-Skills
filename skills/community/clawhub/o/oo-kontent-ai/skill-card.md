## Description:

Kontent.ai (kontent.ai). Use this skill for ANY Kontent.ai request — searching and reading data. Whenever a task involves Kontent.ai, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams can use this skill to search and retrieve content items, content types, and languages from a connected Kontent.ai environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, the setup instructions tell the agent to run a remote installer, including piping a downloaded script into a shell.

Mitigation: Install a verified CLI release before using the skill and require review before any remote installer is run.

Risk: Bundled skill synchronization may change other agent configurations, and Kontent.ai access runs through the connected OOMOL account.

Mitigation: Review synchronization effects and connect only the required Kontent.ai environment with the minimum read permissions needed.

## Reference(s):

- [Kontent.ai](https://kontent.ai)
- [Kontent.ai Management API documentation](https://kontent.ai/learn/docs/apis/management-api-v2)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-kontent-ai)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON data returned by Kontent.ai actions, with text responses as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieval covers content items, content types, and languages.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
