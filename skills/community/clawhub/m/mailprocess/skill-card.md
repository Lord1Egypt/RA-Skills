## Description:

Automatically opens the Mali low-code app builder in Chrome, fills in a user's app-building request, and starts the build flow for internal tools, dashboards, forms, and rapid prototypes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjada45-maker](https://clawhub.ai/user/chenjada45-maker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and internal platform users can use this skill to launch the Mali App Builder and submit requirements for low-code applications such as management systems, dashboards, forms, and prototypes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit prompts through an authenticated Chrome session without a confirmation step.

Mitigation: Review the submitted requirement before execution and avoid using the skill for secrets, credentials, personal data, or sensitive internal plans.

Risk: Browser automation uses AppleScript and JavaScript injection paths.

Mitigation: Use only in a trusted environment, confirm the target URL and page state before submission, and require stricter URL and button validation before broader deployment.

## Reference(s):

- [Mali App Builder](https://lowcode.baidu-int.com/ai-coding)
- [ClawHub skill page](https://clawhub.ai/chenjada45-maker/skills/mailprocess)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown status messages with inline shell commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open a browser and submit the user's requirement to the Mali platform through an authenticated session.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
