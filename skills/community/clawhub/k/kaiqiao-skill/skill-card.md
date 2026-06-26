## Description: <br>
Kaiqiao calibrates an agent's conversational behavior so it asks when context is missing, proceeds when authorized, challenges risky directions, and gives brief status updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leslietong2046-ship-it](https://clawhub.ai/user/leslietong2046-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to tune assistant behavior around clarification, execution, escalation, and concise progress reporting. It also includes an optional local CLI for checking prompts and producing behavior-diagnostic reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill trains the agent to ask fewer confirmations and act more directly. <br>
Mitigation: Require prior confirmation for deletions, payments, publishing, account changes, external messages, private-data access, commits, and other irreversible or high-impact actions. <br>
Risk: The security guidance flags behavioral profile notes and recurring reminder behavior. <br>
Mitigation: Review or disable USER.md, MEMORY.md, and recurring reminder behavior if preference retention or emotional-cue tracking is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leslietong2046-ship-it/kaiqiao-skill) <br>
- [README](README.md) <br>
- [Behavior checklist](references/checklist.md) <br>
- [Kaiqiao CLI checker](references/kaiqiao.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional text diagnostic reports and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external API is required; the optional CLI uses local rule matching.] <br>

## Skill Version(s): <br>
2.0.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
