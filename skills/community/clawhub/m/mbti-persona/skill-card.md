## Description: <br>
Configures an OpenClaw agent with a selected MBTI personality type to adjust communication, decision-making, workflow, and interaction style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JarviYin](https://clawhub.ai/user/JarviYin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to save an MBTI-style interaction preference for an OpenClaw agent and adapt the agent's responses to a chosen personality profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist an MBTI-style interaction preference locally and may activate for broad personality or preference requests. <br>
Mitigation: Review the selected persona before relying on adapted behavior, and remove ~/.openclaw/mbti-config.json if the local preference should no longer persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JarviYin/mbti-persona) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or reads a local MBTI preference file at ~/.openclaw/mbti-config.json when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
