## Description:

Use Wit.ai through OOMOL to analyze text and manage apps, intents, entities, traits, and utterances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to access Wit.ai through their OOMOL-connected account. It supports language analysis and management of apps, intents, entities, traits, and utterances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback setup executes unverified remote code without a clear approval step.

Mitigation: Review setup before installing, use a reviewed version-pinned CLI, check automatic skill synchronization, and keep explicit approval for write and deletion actions.

## Reference(s):

- [Wit.ai](https://wit.ai)
- [Wit.ai HTTP API documentation](https://wit.ai/docs/http/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration guidance]

**Output Format:** [Shell commands with JSON payloads and structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some training and deletion actions run asynchronously; write and deletion actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
