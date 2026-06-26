## Description: <br>
Claw Friends creates OpenClaw character personas and connects them to Tuqu photo generation for selfies, portraits, and other image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouyi531](https://clawhub.ai/user/zhouyi531) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill collection to create and switch character workspaces, generate persona files, and run Tuqu photo API workflows for character selfies, portraits, presets, prompt enhancement, history, balance, and recharge tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Tuqu service keys for authenticated photo, character, billing, and recharge API calls. <br>
Mitigation: Use a limited or disposable Tuqu key, avoid placing keys in query strings or saved workspace files, and pass credentials only at runtime. <br>
Risk: The skill includes payment, recharge, delete, and persistent character-management actions. <br>
Mitigation: Personally confirm every recharge, payment, delete, and character-management operation before allowing the agent to run it. <br>
Risk: The skill can persist OpenClaw role and workspace state under ~/.openclaw. <br>
Mitigation: Review ~/.openclaw/ROLES.json and the target workspace paths before using /shift or modifying character workspaces. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhouyi531/openclaw-friends-skills) <br>
- [OpenClaw](https://github.com/nicepkg/openclaw) <br>
- [Package README](artifact/README.md) <br>
- [OpenClaw Friends skill instructions](artifact/SKILL.md) <br>
- [OpenClaw Character Creator instructions](artifact/openclaw-character-creator/SKILL.md) <br>
- [Tuqu Photo API instructions](artifact/tuqu-photo-api/SKILL.md) <br>
- [Tuqu API notes](artifact/tuqu-photo-api/TUQU_API.md) <br>
- [Tuqu endpoint reference](artifact/tuqu-photo-api/references/endpoints.md) <br>
- [Tuqu workflow recipes](artifact/tuqu-photo-api/references/workflows.md) <br>
- [Tuqu photo API host](https://photo.tuqu.ai) <br>
- [Tuqu billing host](https://billing.tuqu.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON payload examples, generated persona files, and API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes OpenClaw role and workspace files under ~/.openclaw and uses Tuqu service keys only when supplied for authenticated API calls.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
