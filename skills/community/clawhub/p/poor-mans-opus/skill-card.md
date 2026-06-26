## Description: <br>
Gives an AI agent a personality profile through I-Lang ::GENE{} behavior blocks for identity, security, communication, capability, memory, and I-Lang fluency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtmpss](https://clawhub.ai/user/mtmpss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to configure an OpenClaw or Hermes agent with a reusable personality and behavioral policy profile by copying and editing the included SOUL.md template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual SOUL.md replacement can overwrite or unintentionally change an agent's existing behavior policy. <br>
Mitigation: Back up the existing SOUL.md and diff or merge changes before copying the template. <br>
Risk: The skill changes agent control, continuity, and external-action behavior. <br>
Mitigation: Review SOUL.md and the optional full configuration before installing, and avoid putting secrets in continuity files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mtmpss/poor-mans-opus) <br>
- [Project homepage](https://github.com/mtmpss/poor-mans-opus) <br>
- [I-Lang Protocol](https://ilang.ai) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Hugging Face distribution](https://huggingface.co/ilanguage/poor-mans-opus) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and I-Lang configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; includes a SOUL.md template that users manually copy into a workspace.] <br>

## Skill Version(s): <br>
2.0.8 (source: server release metadata and CHANGELOG; SKILL.md frontmatter says 2.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
