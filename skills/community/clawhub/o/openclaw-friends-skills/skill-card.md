## Description:

Claw Friends helps an agent create OpenClaw characters for well-known or fictional personas and use TuQu Dream Weaver APIs for selfies, photo generation, prompt enhancement, character management, billing checks, and related image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouyi531](https://clawhub.ai/user/zhouyi531)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to build OpenClaw character workspaces, switch active personas, and route image-generation or photo-management requests through documented TuQu helper commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TuQu service keys can authorize photo, character, history, billing, and recharge operations.

Mitigation: Use least-privileged disposable service keys, pass them only at runtime, and do not store keys in character workspaces.

Risk: Recharge and billing flows can initiate payment-related actions.

Mitigation: Run recharge or payment commands only after an explicit user request and confirm the selected plan and payment path before execution.

Risk: Workspace switching and delete operations can move active OpenClaw workspaces or remove remote TuQu resources.

Mitigation: Require explicit confirmation and trusted workspace paths or resource IDs before running /shift, delete, or destructive maintenance operations.

Risk: The security scan reports sensitive API, billing, credential, and workspace-moving powers with insufficient safeguards.

Mitigation: Review the skill before installation, restrict use to trusted workspaces, and require confirmation for actions that affect credentials, spending, or persisted state.

## Reference(s):

- [Claw Friends ClawHub Listing](https://clawhub.ai/zhouyi531/skills/openclaw-friends-skills)
- [OpenClaw Project](https://github.com/nicepkg/openclaw)
- [TuQu Service Key Dashboard](https://billing.tuqu.ai/dream-weaver/dashboard)
- [TuQu API Notes](artifact/tuqu-photo-api/TUQU_API.md)
- [TuQu Endpoint Reference](artifact/tuqu-photo-api/references/endpoints.md)
- [TuQu Workflow Recipes](artifact/tuqu-photo-api/references/workflows.md)
- [Well-Known Character System Instruction](artifact/openclaw-character-creator/references/wellknown_system_instruction.md)
- [Fictional Character System Instruction](artifact/openclaw-character-creator/references/nonwellknown_system_instruction.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON payload examples, generated persona files, and formatted API JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write OpenClaw role registries and character workspaces; authenticated TuQu calls require an explicit service key at runtime.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
