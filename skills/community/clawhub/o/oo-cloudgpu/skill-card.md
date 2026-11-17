## Description:

CloudGPU (cloudgpu.app). Use this skill for ANY CloudGPU request — searching and reading data. Whenever a task involves CloudGPU, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using CloudGPU through an OOMOL-connected account can list available models and request chat completions with the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat completion requests are billed and may incur costs without explicit spending approval.

Mitigation: Require user approval for the request or set an explicit spending limit before running a paid completion.

Risk: Request data is sent through OOMOL to CloudGPU.

Mitigation: Review each payload for sensitive information and send only data approved for those services.

Risk: The CLI installer and any additional skills it installs were not available for inspection in the release evidence.

Mitigation: Review the installer source and any added skills before installation or use.

## Reference(s):

- [CloudGPU API documentation](https://cloudgpu.app/api/docs)
- [CloudGPU](https://cloudgpu.app)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls]

**Output Format:** [Chat completion text or model metadata returned as JSON through the oo CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat completion requests are billed and non-streaming.]

## Skill Version(s):

1.0.0 (source: skill frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
