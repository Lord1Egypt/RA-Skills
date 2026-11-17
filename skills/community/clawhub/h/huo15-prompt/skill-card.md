## Description:

Guides users of Qingdao Huo15 Information Technology's OpenClaw enterprise assistant by introducing capabilities, access rules, and common workflows when users send greetings or help requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and technical staff use this skill to orient users to the company's enterprise assistant, explain supported workflows, and provide guidance for system access and messaging conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks technical staff to provide Git usernames and tokens in chat for repository operations.

Mitigation: Use a secure repository integration, scoped short-lived credentials, or an approved secret-entry mechanism instead of pasting Git tokens into chat.

Risk: The skill activates on generic greetings and presents a company-specific persona and terminology.

Mitigation: Install it only in workspaces where the Huo15/OpenClaw persona and terminology are intended, and review responses for fit before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-prompt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance in Chinese with tables, examples, and short prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.8.0 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
