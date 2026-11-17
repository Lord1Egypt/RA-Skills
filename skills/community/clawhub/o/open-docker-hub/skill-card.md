## Description:

Open Docker Hub in Brave. Use when the user asks to use Docker Hub for this purpose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill when they want an agent to open Docker Hub in Brave, reuse an existing relevant tab or session when available, and verify that Docker Hub has loaded without entering credentials or changing account state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may reuse an already signed-in Brave session.

Mitigation: Stop at login or other authentication prompts and do not enter passwords, API keys, payment details, or make account changes.

Risk: Browser automation could open the wrong page or duplicate tabs if state is unclear.

Mitigation: Navigate directly to https://hub.docker.com/, reuse a relevant existing tab when possible, and verify that the expected Docker Hub page is visible.

## Reference(s):

- [Docker Hub](https://hub.docker.com/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-docker-hub)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with browser navigation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs the agent to open Docker Hub in Brave, reuse relevant browser state when available, verify page load, and stop at authentication prompts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
