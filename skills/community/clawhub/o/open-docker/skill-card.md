## Description:

Open Docker in the user's Brave browser and take the user to the Docker homepage. Reuse an existing Docker tab/session when possible. Use when the user asks to open, visit, or go to Open Docker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to open Docker's homepage in Brave, reuse an existing matching tab when available, and verify the destination before reporting success.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on simple navigation phrases such as "Open Docker" or "Go to Docker."

Mitigation: Use it only when the user intends to visit Docker, and keep behavior limited to opening and verifying Docker's homepage.

Risk: A reused browser session may show an authenticated Docker account or require sign-in.

Mitigation: Reuse existing sessions only for navigation, do not enter credentials, and stop at the login page if authentication is required.

## Reference(s):

- [Docker homepage](https://www.docker.com/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-docker)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Text instructions for browser navigation and verification]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Brave, reuses an existing Docker tab or session when available, verifies the destination, and stops at login without handling credentials.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
