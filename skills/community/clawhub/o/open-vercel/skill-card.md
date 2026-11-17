## Description:

Open Vercel in the user's Brave browser, reusing an existing Vercel tab or authenticated session when available and verifying that the destination loaded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to open Vercel in Brave, reuse an existing tab or signed-in session when present, and stop safely if authentication is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may reuse an existing logged-in Vercel browser session.

Mitigation: Review the loaded page yourself before taking any account, deployment, or project actions.

Risk: Authentication may be required before Vercel can be used.

Mitigation: The skill stops at the login page and does not enter passwords, authentication codes, API keys, or other credentials.

## Reference(s):

- [Vercel](https://vercel.com/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-vercel)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text status response after browser navigation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open or focus Brave, reuse an existing Vercel tab, and reuse an existing authenticated browser session.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
