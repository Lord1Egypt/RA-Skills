## Description:

Open GitHub in the user's Brave browser, take the user to GitHub's main page, and reuse an existing GitHub tab or session when possible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GitHub users use this skill to open GitHub in Brave, reusing an existing tab or authenticated session when available. It is useful when the user wants quick navigation to GitHub without credentials handling or content changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reuses an existing Brave session, so it may open GitHub under whichever account is already signed in.

Mitigation: Use it only in the intended Brave profile and stop at the login page when authentication is required.

Risk: A later request could ask the agent to do more than open GitHub, such as changing repository or account content.

Mitigation: Treat any create, edit, delete, publish, deploy, or download action as a separate explicit instruction that should be reviewed before execution.

## Reference(s):

- [GitHub](https://github.com/)
- [Open GitHub on ClawHub](https://clawhub.ai/ruchir17-cmd/skills/open-github)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text]

**Output Format:** [Concise browser automation guidance and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opens or focuses one Brave tab for GitHub, verifies the destination, and stops at login if authentication is required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
