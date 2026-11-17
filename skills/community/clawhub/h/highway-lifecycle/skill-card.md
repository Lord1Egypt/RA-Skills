## Description:

Provides Chinese-language highway lifecycle assistance for design review, construction tunnel analysis, traffic event detection, road damage inspection, multimodal model evaluation, and engineering document consistency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxy799](https://clawhub.ai/user/sxy799)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, transportation engineers, and highway operations teams use this skill to structure Chinese-language reviews of highway design documents, tunnel geology images, traffic video events, road damage images, and multimodal model evaluations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Engineering compliance, tunnel support, traffic safety, and maintenance-priority outputs may be incomplete or incorrect if treated as final decisions.

Mitigation: Treat results as advisory and have qualified engineers verify standards, field measurements, and safety-critical recommendations before action.

Risk: Project documents, images, or video may contain sensitive operational or engineering data when sent to a model endpoint.

Mitigation: Review and minimize project data before model submission, and use approved endpoints and data-handling controls.

## Reference(s):

- [Norm Compliance](references/norm-compliance.md)
- [Multimodal Evaluation](references/multimodal-eval.md)
- [Tunnel Analysis](references/tunnel-analysis.md)
- [Event Detection](references/event-detection.md)
- [Model Selection Guide](assets/model_selection_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON review and evaluation templates, Python helper code, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language advisory outputs; safety-critical findings require qualified human review.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
