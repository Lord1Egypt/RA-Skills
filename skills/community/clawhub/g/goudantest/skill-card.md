## Description: <br>
Advanced code review assistant with intelligent analysis, multi-language support, and structured feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gou1995](https://clawhub.ai/user/gou1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review pull requests, code changes, security-sensitive changes, performance work, and maintainability issues across common programming languages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill can use full-access nested review and run local test commands by default, which may inspect sensitive repositories or execute commands in local development workflows. <br>
Mitigation: Install only in trusted development workflows, review generated feedback before acting on it, use restricted execution for untrusted repositories, and disable automatic test execution when command execution is not expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gou1995/goudantest) <br>
- [Code review checklist](CHECKLIST.md) <br>
- [Feedback templates](TEMPLATES.md) <br>
- [Review examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown review feedback, optional JSON reports, checklist reports, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity labels, file and line references, recommendations, and suggested code changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
