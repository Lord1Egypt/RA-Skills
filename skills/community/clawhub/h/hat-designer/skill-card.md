## Description:

Helps agents create customized hat and cap designs for print or manufacturing on demand using prompts, structured options, and reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, merchants, and developers use this skill to specify personalized hat designs, submit requests to the Craftsman clothing design service, and share available previews or 3D viewer links. The service also supports other clothing categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference-image URLs and design prompts sent to the remote service may expose confidential artwork, unreleased designs, or personal data.

Mitigation: Share only approved assets and data after reviewing the service's data handling; avoid private reference-image URLs.

Risk: The example CLI fetches a package at runtime and remote requests use an API key.

Mitigation: Pin the CLI package version when using the npx example and use a limited-use API key.

Risk: The underlying clothing service supports categories beyond hats and caps.

Mitigation: Confirm the requested clothing category and use the hat template for hat-only requests.

## Reference(s):

- [Hat Designer skill release](https://clawhub.ai/ai-hub-admin/skills/hat-designer)
- [Craftsman Hat Designer](https://craftsman-agent.aiagenta2z.com/app/clothing-designer/hat)
- [OneKey Gateway access keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Design guidance, JSON API requests, Shell commands, Design preview links]

**Output Format:** [Markdown with JSON and shell examples and optional result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote results may include multi-view previews or an interactive 3D viewer, when available.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
