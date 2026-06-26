## Description: <br>
通讯录查询与维护技能，用于查找联系人信息、记录新联系人、或查询历史沟通偏好。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to maintain local contact cards and look up communication identifiers, channels, and preferences before contacting someone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist and reveal local contact records, including messaging identifiers and communication preferences. <br>
Mitigation: Use it only for explicit contact lookup or update tasks, review contact details before sharing them, and require confirmation before creating or changing contact cards. <br>


## Reference(s): <br>
- [Contacts Skill on ClawHub](https://clawhub.ai/axelhu/openclaw-contacts) <br>
- [Contact Schema](memory/contacts/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes local contact-card files under memory/contacts when an agent follows the skill guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
