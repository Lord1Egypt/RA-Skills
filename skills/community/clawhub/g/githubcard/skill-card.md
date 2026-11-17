## Description:

Create and manage embeddable GitHub profile and repository cards, customize their layouts, and add them to README files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cactusinhand](https://clawhub.ai/user/cactusinhand)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create and manage live GitHub profile or repository cards, customize their appearance, and embed them in README files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed GitHubCard API key could be misused.

Mitigation: Authenticate directly with the CLI or use GHCARD_API_KEY; never share the key in chat.

Risk: README edits or card deletion can affect repositories and existing embeds.

Mitigation: Review README changes before committing, and confirm before deleting cards.

Risk: The bundled instructions do not assess the external CLI or hosted service implementation.

Mitigation: Use a reviewed, fixed CLI version and assess the service before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Images, Markdown, HTML, Configuration]

**Output Format:** [SVG or PNG card images with Markdown or HTML embeds; optional JSON design and README updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live card links reflect current GitHub data; snapshot links are frozen images.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
