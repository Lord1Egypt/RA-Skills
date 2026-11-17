## Description:

Remote browser login and session persistence for headless servers through a temporary public browser session that can save cookies and localStorage for future automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaellod](https://clawhub.ai/user/michaellod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill when authenticated browser access is needed on a headless server and a human must complete the login flow visually. It is intended to create reusable Playwright session state for later automated browsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a logged-in browser through a temporary public URL without authentication.

Mitigation: Use it only with intended users, protect the tunnel where possible, and avoid high-value accounts unless access to the tunnel is strongly controlled.

Risk: Saved session files can contain reusable authentication cookies and localStorage.

Mitigation: Restrict access to session files, encrypt or isolate storage where appropriate, and provide a clear deletion process.

Risk: The browser control surface includes an evaluation endpoint that can execute page JavaScript.

Mitigation: Remove or strongly authenticate the endpoint before using the skill with sensitive accounts or untrusted network exposure.

Risk: Typed secrets may pass through browser-control URLs during remote interaction.

Mitigation: Avoid sending secrets in URLs and prefer protected input paths for credentials.

## Reference(s):

- [lock-me-in ClawHub page](https://clawhub.ai/michaellod/skills/lock-me-in)
- [cloudflared Linux AMD64 download](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks, plus saved Playwright JSON session files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates browser session state files containing cookies and localStorage under the configured sessions directory.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
