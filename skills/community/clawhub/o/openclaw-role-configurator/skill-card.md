## Description: <br>
OpenClaw role configuration assistant that guides users through creating or replacing an assistant persona, applying preset role templates, writing SOUL.md, and recommending related skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill during initial setup or later reconfiguration to define an assistant name, role, tasks, capabilities, and communication style. It can apply one of the bundled role templates, generate the resulting SOUL.md configuration, and suggest complementary skills for the selected role. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently replace the assistant's active SOUL.md role configuration. <br>
Mitigation: Preview the selected template and keep a backup of SOUL.md before applying a new configuration. <br>
Risk: Bundled medical, pregnancy, infant-care, and mental-health personas may be under-scoped for sensitive advice. <br>
Mitigation: Use these personas only with strong safety limits and do not treat their output as professional medical or mental-health advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhuqingsonga/openclaw-role-configurator) <br>
- [Publisher profile](https://clawhub.ai/user/zhuqingsonga) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and SOUL.md configuration text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or replace the active SOUL.md role configuration when the bundled writer is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
