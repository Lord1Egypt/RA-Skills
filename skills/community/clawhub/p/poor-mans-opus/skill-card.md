## Description:

Poor Mans Opus provides an I-Lang SOUL template and gene-based behavior profile that helps users give an AI agent a consistent personality, communication style, memory posture, and safety controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtmpss](https://clawhub.ai/user/mtmpss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to apply a reusable SOUL behavior profile that shapes an agent's identity, communication style, safety posture, context handling, and I-Lang fluency. It is intended for manual activation by copying the SOUL template into a workspace and reviewing the behavior layer before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change broad workspace-wide agent behavior when its SOUL template is copied into a workspace.

Mitigation: Review SOUL.md before copying it, keep a backup of the existing SOUL.md, and install only when a workspace-wide behavior layer is intended.

Risk: The skill points users toward external advanced configuration and package/download locations that may change over time.

Mitigation: Inspect and pin any GitHub, Hugging Face, or Hermes downloads before activation, and avoid adopting advanced configuration until its authority rules have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mtmpss/skills/poor-mans-opus)
- [Project homepage](https://github.com/mtmpss/poor-mans-opus)
- [I-Lang Protocol](https://ilang.ai)
- [OpenClaw runtime](https://github.com/openclaw/openclaw)
- [Hugging Face project](https://huggingface.co/ilanguage/poor-mans-opus)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with I-Lang configuration blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires manual SOUL.md copy/edit workflow; installation does not automatically overwrite an existing SOUL.md.]

## Skill Version(s):

2.0.8 (source: server release evidence and changelog, released 2026-05-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
