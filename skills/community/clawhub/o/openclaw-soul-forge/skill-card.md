## Description: <br>
OpenClaw Lobster Soul Forge helps OpenClaw agent builders create a complete lobster persona, including identity positioning, SOUL.md content, boundary rules, a name, and an avatar prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eamanc-lab](https://clawhub.ai/user/eamanc-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and agent builders use this skill to design character-driven OpenClaw souls with a coherent identity, behavioral boundaries, name, and avatar prompt. It supports guided design, random gacha-style persona generation, and packaging generated content into SOUL.md and IDENTITY.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SOUL.md or IDENTITY.md content can change an agent's active personality and operating boundaries. <br>
Mitigation: Review the generated persona, boundaries, and sample replies before installing them as active agent configuration. <br>
Risk: Writing generated files to the wrong directory or over existing files could replace an existing OpenClaw soul configuration. <br>
Mitigation: Confirm the target directory and check whether SOUL.md or IDENTITY.md already exist before allowing file writes. <br>
Risk: Avatar image generation is optional and depends on a separate image-generation skill when available. <br>
Mitigation: Use the text avatar prompt as the fallback path, and review any optional image-generation dependency before invoking it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eamanc-lab/openclaw-soul-forge) <br>
- [Project homepage](https://github.com/eamanc-lab/openclaw-persona-forge) <br>
- [Avatar style](references/avatar-style.md) <br>
- [Boundary rules](references/boundary-rules.md) <br>
- [Error handling](references/error-handling.md) <br>
- [Identity tension](references/identity-tension.md) <br>
- [Naming system](references/naming-system.md) <br>
- [Output template](references/output-template.md) <br>
- [Optional baoyu-image-gen dependency](https://github.com/JimLiu/baoyu-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated SOUL.md and IDENTITY.md content, gacha command output, and avatar prompt text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally write SOUL.md and IDENTITY.md after user confirmation; avatar image generation depends on an optional external skill.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
