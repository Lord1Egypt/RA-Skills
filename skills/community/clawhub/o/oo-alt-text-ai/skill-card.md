## Description:

Use AltText.ai to generate image alt text, scrape pages for images, and manage image records through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams and developers can generate alt text for public image URLs, scrape pages for images, and inspect or manage records in an AltText.ai library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Page scraping may include more images than intended and can incur charges; image creation changes the AltText.ai library.

Mitigation: Confirm the page or HTML, discovered-image scope, exact write action, and possible charges before proceeding.

Risk: The recommended CLI installer scripts were not verified by the security review.

Mitigation: Verify the CLI release and installer source before running an installer.

Risk: The hosted connector implementation and automatic skill synchronization across agent hosts were not verified.

Mitigation: Review connector behavior and synchronization scope before granting access across hosts.

## Reference(s):

- [AltText.ai API documentation](https://alttext.ai/apidocs)
- [AltText.ai](https://alttext.ai)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON inputs and JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can include generated alt text and image-record data.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
