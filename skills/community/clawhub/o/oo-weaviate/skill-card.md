## Description:

Weaviate (weaviate.io). Use this skill for ANY Weaviate request — searching and reading data. Whenever a task involves Weaviate, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use the skill to inspect Weaviate collections, instance metadata, and objects, and to list or retrieve stored objects through a connected Weaviate account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote installers and a CLI binary that the available evidence does not verify.

Mitigation: Review and install a specific CLI release before enabling the skill.

Risk: The required CLI can have broader effects on installed agent skills, and the connected account exposes Weaviate data to the integration.

Mitigation: Consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1 and connect only the Weaviate account intended for this use.

## Reference(s):

- [Weaviate API documentation](https://docs.weaviate.io/weaviate/api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Weaviate homepage](https://weaviate.io)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read and retrieval actions; requires an installed, signed-in oo CLI and a connected Weaviate account.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
