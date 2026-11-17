## Description:

Isolate and coordinate sub-agent memory in OpenClaw with Hippocampus using scoped IDs, bounded merge-back, and explicit cross-agent imports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cezexpl](https://clawhub.ai/user/cezexpl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to isolate sub-agent memory in OpenClaw, prevent accidental leakage across parent and sibling contexts, and coordinate explicit bounded merge-back from child agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect sub-agent memory scoping could leak child-agent context into parent or sibling namespaces.

Mitigation: Use scoped sub-agent IDs, keep child memory isolated by default, and import only explicitly approved summaries, artifacts, or references.

Risk: Related Hippocampus automation, packages, or portal configuration may perform memory storage and lifecycle behavior outside this documentation-only skill.

Mitigation: Review and scan related packages and portal configuration before deployment.

## Reference(s):

- [Hippocampus Subagent Memory on ClawHub](https://clawhub.ai/cezexpl/skills/hippocampus-subagent-memory)

## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable code or hidden installation behavior is included.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
