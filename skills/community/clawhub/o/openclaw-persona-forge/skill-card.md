## Description: <br>
OpenClaw 龙虾灵魂锻造炉 helps agents design OpenClaw persona packages by guiding or randomly drawing a lobster persona, then producing identity text, SOUL.md content, character boundary rules, names, avatar prompts, and optionally avatar images through an installed image-generation skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eamanc-lab](https://clawhub.ai/user/eamanc-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to create or customize characterful OpenClaw agent personas with a guided workflow or random draw. The skill is intended for new OpenClaw persona design, not for editing an existing SOUL.md or building personality-free tool agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated persona context may contain tone, boundaries, or behavioral rules that do not match the user's intended agent behavior. <br>
Mitigation: Review the generated SOUL.md and IDENTITY.md before using them as agent context. <br>
Risk: The skill can create local output files after user approval, so an unsuitable target directory could overwrite or mix persona files with unrelated project files. <br>
Mitigation: Choose the output directory deliberately and inspect generated files before committing or deploying them. <br>
Risk: Automatic avatar generation depends on a separately installed image-generation skill and its provider. <br>
Mitigation: Use automatic avatar generation only when that dependency and provider are trusted, or use the generated prompt manually instead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eamanc-lab/openclaw-persona-forge) <br>
- [Source homepage](https://github.com/eamanc-lab/openclaw-persona-forge) <br>
- [Avatar style reference](references/avatar-style.md) <br>
- [Boundary rules reference](references/boundary-rules.md) <br>
- [Error handling reference](references/error-handling.md) <br>
- [Identity tension reference](references/identity-tension.md) <br>
- [Naming system reference](references/naming-system.md) <br>
- [Output template reference](references/output-template.md) <br>
- [Optional baoyu-image-gen dependency](https://github.com/JimLiu/baoyu-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with generated SOUL.md and IDENTITY.md content, avatar prompts, optional file creation, and optional shell command execution for random draws.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Random-draw mode uses a local Python script with a maximum of five draws per invocation; avatar image generation is optional and depends on a separately installed image-generation skill.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
