## Description:

Publish a static website (HTML, CSS, JS, images, or a ZIP) or a built framework app (React, Vue, Svelte, Vite, Astro, Next.js static export) to OxyPages and hand the user a live HTTPS link. Works with no account for a 30-minute unclaimed link, or with an OxyPages API key for a permanent site the user owns, including editing a site they already have.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oxypages](https://clawhub.ai/user/oxypages)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to publish static websites or built framework apps to OxyPages, then share a live HTTPS link. With an OxyPages API key, they can deploy to or update a site in the user's account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing makes site content publicly accessible; a no-account link expires after 30 minutes unless claimed.

Mitigation: Publish only after the user explicitly asks to host the content, then share the live URL, expiry, and claim link.

Risk: An OxyPages API key enables permanent deployments and edits to sites in the user's account.

Mitigation: Use the key only for the requested publishing task, and have the user choose an existing site when one fits.

## Reference(s):

- [OxyPages](https://oxypages.com)
- [OxyPages Publish on ClawHub](https://clawhub.ai/oxypages/skills/oxypages-publish)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown with shell commands, JSON examples, and deployment links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides a live HTTPS URL; no-account deployments also include a claim link and expiry details.]

## Skill Version(s):

1.1.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
