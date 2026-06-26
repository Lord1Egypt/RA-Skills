## Description: <br>
Think proactively during idle time with sandboxed reflections, adaptive rhythms, and feedback-driven focus areas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agent users use Meditate to receive lightweight reflection prompts during idle time, based on conversation patterns and local feedback memory. It is intended for observations and questions only, not actions, command execution, or external data access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived reflection memory may include sensitive personal or work patterns if the user allows the skill to retain them locally. <br>
Mitigation: Keep memory in ~/meditate/, review or delete stored files when needed, and avoid placing personal data in the pending insight queue. <br>
Risk: Proactive reflections may become distracting or focus on topics the user does not want considered. <br>
Mitigation: Use feedback controls to exclude topics, reduce frequency after silence or negative feedback, and pause meditations when engagement remains low. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/meditate) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [memory-template.md](artifact/memory-template.md) <br>
- [sandbox.md](artifact/sandbox.md) <br>
- [feedback.md](artifact/feedback.md) <br>
- [topics.md](artifact/topics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reflection prompts and local memory templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be framed as observations or questions, with no executable code, commands, API calls, notifications, or actions on the user's behalf.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
