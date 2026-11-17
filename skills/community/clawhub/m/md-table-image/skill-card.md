## Description:

Render markdown tables as PNG images. Use whenever you need to send a table in chat -- render it as an image instead of raw markdown text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kirorab](https://clawhub.ai/user/kirorab)

### License/Terms of Use:

ISC

## Use Case:

External users, developers, and agents use this skill to convert markdown tables or short markdown snippets into styled PNG images for chat or documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled markdown is rendered as active HTML in an unsandboxed browser.

Mitigation: Use only trusted markdown unless the renderer is changed to escape or sanitize input, disable JavaScript and network requests, and restore browser sandboxing.

Risk: The release ships risky dependency versions.

Mitigation: Review, update, or pin safer dependencies before installing in a production or shared environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kirorab/skills/md-table-image)
- [ClawHub publisher profile](https://clawhub.ai/user/kirorab)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image file path with shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a local Chrome executable compatible with puppeteer-core.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
