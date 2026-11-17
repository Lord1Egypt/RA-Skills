## Description:

Guides agents through a HappyCoding AI Coding workflow for requirement discussion, code editing, preview validation, project saving, publishing, and evidence capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongkuang](https://clawhub.ai/user/dongkuang)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to implement or iterate application features in the HappyCoding AI Coding platform while preserving a requirements-to-publish workflow. It is especially oriented toward platform tasks that need preview checks, saved project state, publication links, and evidence records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow directs agents to use an existing logged-in platform account and to save or publish projects.

Mitigation: Require explicit user confirmation before saving or publishing and record the resulting link and evidence only after confirmation.

Risk: The skill describes use of an external image API with an API key and uploaded or prompt-derived content.

Mitigation: Keep API keys in a secret manager or server-side environment and avoid sending sensitive prompts or images unless that sharing is intended.

Risk: Scanner guidance classifies the release as suspicious because account operation, publication, and external API handling are insufficiently scoped.

Mitigation: Review the skill before deployment and constrain agent access to the minimum platform permissions needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongkuang/skills/happycoding-aicoding)
- [HappyCoding AI Coding platform](https://aicoding.aigcuniversity.com/)
- [Image generation API endpoint](https://ainet.aigcuniversity.com/api/v1/tank/custom_gpt/10/execute)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown guidance with JavaScript snippets and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to operate a logged-in platform account, save and publish projects, and use an external image API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
