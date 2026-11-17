## Description:

Use SunoAPI through an OOMOL-connected account to manage music data and submit audio generation and processing tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to read and manage SunoAPI data, generate or process audio, and retrieve task results through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio generation and processing may incur charges, and vocal separation or style boosting may run without a clear confirmation step.

Mitigation: Confirm the requested task and payload before generation or processing, and review style boosting before using it.

Risk: Setup may affect other installed skills, while the remote installers and hosted connector code have not been verified.

Mitigation: Preinstall a reviewed CLI release and decide whether to allow automatic skill synchronization.

Risk: OOMOL mediates account access and submitted content.

Mitigation: Use the connector only when its account and content handling is acceptable for the material being submitted.

## Reference(s):

- [SunoAPI](https://sunoapi.org)
- [SunoAPI documentation](https://docs.sunoapi.org/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, API results, Shell commands]

**Output Format:** [JSON payloads, command examples, task identifiers, and returned result details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio generation and processing run through SunoAPI; the skill returns task identifiers or result details.]

## Skill Version(s):

1.0.6 (source: server-resolved release version and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
