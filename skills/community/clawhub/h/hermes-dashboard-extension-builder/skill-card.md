## Description:

Generate and validate Hermes-style dashboard extension scaffolds: themes, plugins, custom tabs, slots, and backend API route manifests for OpenClaw/Hermes agent teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Hermes/OpenClaw dashboard integrators use this skill to generate and validate packaged dashboard extension scaffolds, including manifests, frontend stubs, backend route stubs, and readiness reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated dashboard files can embed untrusted spec values as executable Python or browser-rendered HTML.

Mitigation: Use trusted specs or review generated files before use; safely encode or strictly validate api_route and HTML-escape tab and slot values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevojarvisai-star/skills/hermes-dashboard-extension-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated scaffold files include JSON, HTML, and Python.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate extension.json, frontend HTML, backend Python route stubs, and VALIDATION.json in the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
