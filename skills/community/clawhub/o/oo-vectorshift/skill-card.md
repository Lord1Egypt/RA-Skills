## Description:

Operate VectorShift pipelines through an OOMOL-connected account to list, retrieve, and run pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected VectorShift account can discover pipelines, retrieve a pipeline, and run one or more pipeline instances. Run actions can change state, so review the requested operation and payload before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback directs users to run a downloaded installer, and the installer contents were unavailable for verification.

Mitigation: Review setup behavior first; install a reviewed, version-fixed CLI separately and require approval before running any downloaded installer.

Risk: Automatic agent-skill synchronization and the VectorShift permissions granted to OOMOL may affect the user's environment or connected account.

Mitigation: Review synchronization behavior and grant only the VectorShift permissions needed for the requested work.

## Reference(s):

- [VectorShift API documentation](https://docs.vectorshift.ai/api-reference/overview)
- [VectorShift](https://vectorshift.ai)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON results with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: skill frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
