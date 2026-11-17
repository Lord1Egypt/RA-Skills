## Description:

Datalust Seq (datalust.co). Use this skill for ANY Datalust Seq request — reading, creating, updating, and deleting data. Whenever a task involves Datalust Seq, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query Seq events and create, update, or delete events, saved queries, and signals through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run downloaded code that has not been verified.

Mitigation: Use a verified oo CLI release and explicitly approve installation; avoid the automatic downloaded-script fallback.

Risk: The documented skill synchronization may change agent skills, and its broader effects are unexplained.

Mitigation: Review what the synchronization changes or disable it before launch.

Risk: Seq logs may pass through OOMOL.

Mitigation: Connect a narrowly scoped Seq account and consider whether the logs are appropriate to route through OOMOL.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Datalust Seq](https://datalust.co/seq)
- [Seq HTTP API documentation](https://docs.datalust.co/docs/using-the-http-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Shell commands with JSON request payloads and structured Seq results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read, create, update, or delete Seq data; write and destructive actions are identified in the skill instructions.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
