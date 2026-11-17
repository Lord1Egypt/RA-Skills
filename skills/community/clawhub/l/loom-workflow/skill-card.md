## Description:

Analyzes Loom recordings and breaks recorded business processes into structured, automatable workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to analyze authorized Loom walkthroughs, extract steps, tools, decision points, and ambiguities, and generate workflow artifacts for automation review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Loom recordings, extracted frames, and transcripts can contain sensitive business data.

Mitigation: Only process Loom recordings the user is authorized to analyze, and inspect or redact extracted frames and transcripts before any model upload.

Risk: Generated Lobster workflows can include executable steps influenced by untrusted analysis JSON.

Mitigation: Treat analysis JSON as untrusted input, review generated commands and output paths, and dry-run workflows before execution.

Risk: The skill can create automation for destructive or external actions captured in a workflow recording.

Mitigation: Keep approval gates for destructive, external, ambiguous, and decision-point steps, and require human review before running generated workflows.

## Reference(s):

- [Loom Workflow on ClawHub](https://clawhub.ai/g9pedro/skills/loom-workflow)
- [Loom Workflow design notes](artifact/DESIGN.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown summaries, JSON analysis files, Lobster workflow YAML, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Lobster workflows should be manually reviewed before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
