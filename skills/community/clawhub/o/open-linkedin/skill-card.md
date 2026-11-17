## Description:

Open LinkedIn in the user's Brave browser and take the user to the LinkedIn homepage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they want an agent to open LinkedIn in Brave, reuse an existing LinkedIn tab or session when available, and confirm the homepage has loaded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening LinkedIn may use the user's existing authenticated Brave session.

Mitigation: Reuse only the browser session already available to the user and stop if LinkedIn asks for sign-in.

Risk: A browser-opening skill could be mistaken for permission to act on the user's LinkedIn account.

Mitigation: Limit behavior to opening and verifying the LinkedIn homepage; do not post, message, follow, change settings, or handle credentials.

## Reference(s):

- [open-linkedin ClawHub page](https://clawhub.ai/ruchir17-cmd/skills/open-linkedin)
- [LinkedIn homepage](https://www.linkedin.com/)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [Plain text status with browser-action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open or focus Brave, reuse an existing LinkedIn tab, and stop at sign-in without handling credentials.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
