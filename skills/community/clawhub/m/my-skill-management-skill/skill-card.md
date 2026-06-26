## Description: <br>
管理和发布用户自定义技能的统一接口。强制执行“my_”前缀、统一存放目录（~/.openclaw/skills）、基于配置文件（skills.json）的智能体绑定规则，并要求本地技能变更后必须立即通过clawhub上传备份。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to standardize publishing, installing, and governing custom OpenClaw skills through ClawHub. It is intended for user-created skills that follow the `my_` naming convention and are stored under `~/.openclaw/skills/`. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish local skill contents to ClawHub, which may expose secrets, private prompts, or unintended files. <br>
Mitigation: Manually review and scan skill files before publishing, and confirm the destination account, slug, version, changelog, and visibility. <br>
Risk: The helper can install remote skills and search arbitrary slugs without strong trust controls. <br>
Mitigation: Install only trusted ClawHub skills and avoid using the helper with untrusted remote skill slugs. <br>
Risk: Using paths outside the intended local skill directory may publish or manage unintended content. <br>
Mitigation: Restrict use to user-created skills under ~/.openclaw/skills and keep the `my_` naming convention for managed skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canonxu/my-skill-management-skill) <br>
- [Publisher profile](https://clawhub.ai/user/canonxu) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose ClawHub publish, search, and install commands for local skill management workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
