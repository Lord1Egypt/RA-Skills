## Description: <br>
Automatically generate and save a reusable skill after an AI agent successfully completes a complex task involving five or more tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture a successful multi-step workflow, desensitize the session text, draft a focused SKILL.md, and save it for reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Completed conversations can contain sensitive or private session details that may be preserved in a generated skill. <br>
Mitigation: Run the provided desensitization step, avoid using highly sensitive sessions, and review the cleaned session and generated SKILL.md before relying on it. <br>
Risk: A generated skill may have an overly broad trigger description or misleading workflow guidance. <br>
Mitigation: Review and narrow trigger descriptions, verify workflow steps against the successful path, and scan the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/oh-my-skill) <br>
- [Publisher profile](https://clawhub.ai/user/goog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown skill draft with inline shell commands and optional Python masking output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a reusable SKILL.md and may save supporting scripts, references, or assets when the captured workflow requires them.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
