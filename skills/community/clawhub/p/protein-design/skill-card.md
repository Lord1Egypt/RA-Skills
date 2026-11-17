## Description:

Protein, peptide, antibody, nanobody, binder, enzyme, and sequence design workflows using Boltzgen, RFdiffusion, RFdiffusion2, RFdiffusion3, ProteinMPNN, LigandMPNN, and BindCraft through SciMiner APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users use this skill to run SciMiner protein-design workflows for backbone generation, binder design, antibody or nanobody design, enzyme scaffolding, sequence redesign, and multi-step design pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable online SciMiner documentation can change authenticated request behavior.

Mitigation: Review the selected SciMiner Markdown document before each invocation and use the skill only when the documentation host is trusted.

Risk: Protein structures, sequences, and design constraints may be sent through SciMiner workflows.

Mitigation: Avoid sensitive or unpublished data unless approved, and verify upload destinations before submitting files.

Risk: The skill requires a SciMiner API key.

Mitigation: Use a dedicated, revocable key stored outside the repository and do not print, persist, or log the key.

## Reference(s):

- [SciMiner Tool API Documentation](https://sciminer.tech/tool_api_files/)
- [SciMiner API Key Utility](https://sciminer.tech/utility)
- [ClawHub Protein Design Skill](https://clawhub.ai/sciminer/skills/protein-design)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown summaries with JSON task results and SciMiner share URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses selected SciMiner Markdown docs as the payload source and returns task share URLs for completed or long-running jobs.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
