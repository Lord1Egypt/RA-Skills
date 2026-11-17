## Description:

Plan and run intelligent workflows through a user-configured 算力超市 tenant for model, app, media, digital-human, music, smart-clip, asset, and social-media operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likeadmin-hub](https://clawhub.ai/user/likeadmin-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan, validate, and execute workflows against a configured 算力超市 tenant for generation, media processing, application API, asset, and task operations. It is intended for requests where the user explicitly invokes 算力超市 or provides tenant context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tenant API keys could be exposed if configured with an unencrypted HTTP tenant URL.

Mitigation: Configure only an HTTPS tenant URL, use a least-privilege API key with quotas, and rotate the key if HTTP was ever used.

Risk: Uploads, destructive asset deletion, social-media lookup/list/search, and watermark-removal operations can affect user data or third-party content.

Mitigation: Require explicit user approval before those operations and proceed only when the user confirms authorization for the content.

Risk: Paid or state-changing generation workflows can spend tenant credits or create persistent assets such as cloned voices.

Mitigation: Check availability and pricing before cost-sensitive work, ask the user to choose materially different options, and do not automatically retry voice cloning.

## Reference(s):

- [Capability Catalog](references/capability-catalog.json)
- [Contracts Bundle](references/contracts.bundle.json)
- [Intelligent Orchestration](references/orchestration.md)
- [Workflow Inputs](references/workflow-inputs.md)
- [ClawHub Skill Page](https://clawhub.ai/likeadmin-hub/skills/likeadmin-market-skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with JSON and shell command snippets; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist non-secret workflow state when requested.]

## Skill Version(s):

1.1.0 (source: server release evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
