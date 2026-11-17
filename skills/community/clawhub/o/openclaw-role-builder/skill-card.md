## Description:

Build and manage OpenClaw roles by creating AI character personas, switching the active role, and generating identity-consistent or freestyle TuQu images for those roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouyi531](https://clawhub.ai/user/zhouyi531)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create and switch character personas, manage role workspaces, and generate character-consistent portraits, selfies, group shots, or freestyle images through TuQu API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed TuQu API access can perform image generation, character management, history operations, balance checks, and recharge/payment flows.

Mitigation: Use a disposable or tightly scoped service key, keep the key out of persisted files, and require explicit user confirmation before deletion, recharge, or payment actions.

Risk: Role switching moves OpenClaw workspaces and can affect the active local character state.

Mitigation: Run the skill under an isolated user account or disposable OpenClaw profile when reviewing it, and inspect ~/.openclaw/ role paths before switching roles.

Risk: The security summary reports that documented host and filesystem boundaries are not fully enforced by the scripts.

Mitigation: Review helper commands before execution and restrict installation to environments where access to ~/.openclaw/ and TuQu credentials is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhouyi531/skills/openclaw-role-builder)
- [TuQu Service Key Dashboard](https://billing.tuqu.ai/dream-weaver/dashboard)
- [TuQu API Notes](artifact/tuqu-photo-api/TUQU_API.md)
- [Endpoint Reference](artifact/tuqu-photo-api/references/endpoints.md)
- [Workflow Recipes](artifact/tuqu-photo-api/references/workflows.md)
- [OpenClaw Character Creator](artifact/openclaw-character-creator/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown persona files, JSON API responses, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and an explicit TuQu service key for authenticated image, character, history, billing, and recharge calls; role data is written under ~/.openclaw/.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
