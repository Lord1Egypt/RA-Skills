## Description: <br>
Let agents operate your iCloud Drive, Photos, and Find My safely with local 2FA authentication and explicit confirmation gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to let an agent perform user-directed iCloud Drive, Photos, and Find My workflows against their own iCloud account. It is intended for read-first account operations with local authentication and explicit confirmation before risky actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apple credentials or 2FA codes could be exposed if entered into chat. <br>
Mitigation: Use only local terminal or secure local prompts for authentication, and never paste passwords, codes, tokens, or recovery keys into the conversation. <br>
Risk: Risky iCloud actions could affect the wrong device or path. <br>
Mitigation: Require explicit confirmation of the exact device ID or iCloud Drive path, take a read-only snapshot first, and verify the resulting state with a second read. <br>
Risk: The pyicloud dependency operates against the user's iCloud account. <br>
Mitigation: Review the dependency before installation and use the skill only when comfortable allowing local agent-directed iCloud operations. <br>


## Reference(s): <br>
- [ClawHub iCloud release](https://clawhub.ai/ivangdavila/icloud) <br>
- [iCloud skill homepage](https://clawic.com/skills/icloud) <br>
- [PyPI package index](https://pypi.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local prompts for authentication and confirmation-gated operational steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
