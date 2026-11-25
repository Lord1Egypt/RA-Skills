## Description:

Put a local dev server on the user's stable public HTTPS domain with localhost.run, for previews, sharing work in progress, testing on phones, or receiving webhooks. Use when the user wants a public URL for something running locally, asks to share or preview their local app, needs a webhook endpoint, wants their app on a particular domain, or mentions localhost.run. Also sets up a new user's localhost.run domain and SSH key, or gives them a temporary address if they'd rather skip setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhr](https://clawhub.ai/user/lhr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to share a locally running app through a public HTTPS URL, including for previews, phone testing, teammate access, and webhooks. It can configure a stable localhost.run domain or create a temporary tunnel when the user chooses one.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: While a tunnel is active, anyone with its public URL can reach the local app.

Mitigation: Only start a tunnel when the user intends to share that app, and stop it when sharing is done.

Risk: The security scan was partial (75% coverage), and tool-misuse analysis was degraded; the scan calls out SSH behavior, an external URL check, and a detached supervisor for review.

Mitigation: Review those reported behaviors before use and confirm they fit the intended tunnel task.

## Reference(s):

- [localhost.run documentation](https://localhost.run/docs/)
- [Custom domains](https://localhost.run/docs/custom-domains)
- [Setup guide](references/setup.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with public URLs, status text, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A public tunnel URL and connection status; tunnels stop after a configured duration.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
