## Description:

Automate Microsoft Forms submission with dual-calendar integration and M365 MFA support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claireaicodes](https://clawhub.ai/user/claireaicodes)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to prepare and submit recurring Microsoft Forms activity logs using calendar-derived training, content development, and learning-hour entries. Developers and automation maintainers can use it to configure Playwright-based submission flows for Microsoft 365 accounts that may require MFA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses Microsoft 365 passwords, browser session state, calendar URLs, and organizational form data locally.

Mitigation: Use restrictive file permissions, add explicit gitignore rules for generated secrets and session artifacts, and prefer OAuth or a secure credential store where possible.

Risk: Passing MFA codes on the command line can expose short-lived authentication material through shell history or process listings.

Mitigation: Enter MFA codes interactively or through a protected secret handoff instead of command-line arguments.

Risk: Debug and audit workflows can save screenshots or HTML that may contain form content or account context.

Mitigation: Disable capture in routine use, store generated captures in protected locations, and delete them after review.

## Reference(s):

- [Authentication Workflow Testing](references/TESTING_AUTH_WORKFLOW.md)
- [Configured Microsoft Forms Endpoint](https://forms.cloud.microsoft/r/LsxLaEv13i)
- [ClawHub Skill Page](https://clawhub.ai/claireaicodes/skills/ms-forms-auto)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local credential, session-state, daily-entry, screenshot, HTML, and audit files during setup, testing, and submission workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
