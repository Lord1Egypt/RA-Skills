## Description:

Inspects container health and suggests fixes for common errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liverock](https://clawhub.ai/user/liverock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Docker-style container health signals, identify common failure patterns, and receive suggested remediation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostics may reflect bundled mock container data rather than live Docker state.

Mitigation: Verify findings against actual container status and logs before making operational changes.

Risk: Suggested fixes such as restarts, memory changes, or dependency checks may be incomplete for a specific deployment.

Mitigation: Review the recommendation in context and apply changes through normal operational controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liverock/skills/openclaw-skill-local-docker-health-check)
- [Publisher profile](https://clawhub.ai/user/liverock)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Plain text summary, Markdown status table, and JSON prescriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional name parameter narrows diagnostics to a specific container when supported by the caller.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
