## Description: <br>
Tracks skill success rates, discovers better tools, and prompts users to choose when better options are found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyzlove](https://clawhub.ai/user/wyzlove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Path Evolver to record successful execution paths, track skill success rates, and receive suggestions for alternative tools when a task type is new, a tool fails, cached knowledge expires, or the user asks for recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local workflow cache may contain task parameters or other sensitive operational context. <br>
Mitigation: Avoid storing secrets or detailed prompts in task parameters, and review the local cache before using the skill with sensitive work. <br>
Risk: ClawHub or GitHub searches can disclose task categories to external services. <br>
Mitigation: Send only sanitized task types, not user prompts or task parameters, and avoid network search for highly sensitive workflows. <br>
Risk: Tool recommendations may be incorrect, stale, or unsuitable for a specific workflow. <br>
Mitigation: Keep user confirmation in the loop and review or scan recommended skills before deployment. <br>


## Reference(s): <br>
- [Path Evolver ClawHub Page](https://clawhub.ai/wyzlove/path-evolver) <br>
- [Design Decisions](references/design-decisions.md) <br>
- [Workflow Cache Template](assets/workflow-cache-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local cache updates, success-rate summaries, and user-facing tool recommendations.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
