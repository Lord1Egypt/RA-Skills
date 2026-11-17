## Description:

Use the OOMOL-connected TypeSafe AI service to evaluate text or structured data and list available models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to evaluate text or structured JSON with TypeSafe Choice, Score, and Noul questions, or to list models available to their connected TypeSafe AI account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute software whose remote installer and installed release were not verified.

Mitigation: Review and verify the oo CLI before installing it.

Risk: The current upstream CLI behavior can persistently install other agent skills during startup.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization if those changes are unwanted.

Risk: Text or structured data submitted through the connected service is processed by OOMOL and TypeSafe AI.

Mitigation: Submit only content intended for OOMOL and TypeSafe AI to process.

## Reference(s):

- [TypeSafe AI](https://typesafe.ai)
- [TypeSafe AI API documentation](https://docs.typesafe.ai/api)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector responses and text results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected TypeSafe AI account and selected action.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
