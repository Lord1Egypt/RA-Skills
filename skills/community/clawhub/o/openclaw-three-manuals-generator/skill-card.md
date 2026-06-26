## Description: <br>
Guides users through a dialogue to generate personalized SOUL.md, USER.md, and AGENTS.md setup manuals for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-long-2022](https://clawhub.ai/user/jack-long-2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent builders use this skill to clarify what kind of AI companion they want, then generate personalized local setup manuals for persona, user preferences, and agent working rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated manuals may include personal preferences, workflow details, or sensitive boundaries that the user did not intend to preserve. <br>
Mitigation: Review the generated SOUL.md, USER.md, and AGENTS.md content before saving, and omit secrets, credentials, private account details, or sensitive personal information. <br>
Risk: The skill may create or update local setup manuals and could overwrite existing user configuration. <br>
Mitigation: Confirm target file paths and review any overwrite request before approving writes to SOUL.md, USER.md, or AGENTS.md. <br>
Risk: Incorrect or overly broad agent rules could lead future agents to act outside the user's intended boundaries. <br>
Mitigation: Use the included validation checklist and manually verify identity, user preferences, working rules, and red lines before adopting the generated manuals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jack-long-2022/openclaw-three-manuals-generator) <br>
- [GUIDE.md](artifact/GUIDE.md) <br>
- [SOUL fragments](artifact/TEMPLATES/SOUL-fragments.md) <br>
- [USER fragments](artifact/TEMPLATES/USER-fragments.md) <br>
- [AGENTS fragments](artifact/TEMPLATES/AGENTS-fragments.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown files and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates SOUL.md, USER.md, and AGENTS.md content through guided dialogue, with a validation checklist before delivery.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
