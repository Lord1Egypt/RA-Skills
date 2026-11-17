## Description:

Search Gumtree UK Pets listings with bb-browser for dogs, cats, small furries, reptiles, horses, and pet equipment, returning structured JSON and first-image Markdown for comparing ads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salamankakit](https://clawhub.ai/user/salamankakit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and compare UK Gumtree pet and pet-equipment listings through bb-browser adapters. It supports read-only listing research and comparison, not posting ads or contacting sellers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The search adapter is described as pets-only, but it can accept broader Gumtree categories.

Mitigation: Use or revise the adapter so it enforces the expected pet categories before installation.

Risk: The listing adapter can fetch URLs beyond the intended Gumtree pet-listing scope.

Mitigation: Require HTTPS listing URLs on www.gumtree.com and reject redirects or other hosts.

Risk: The installation instructions use the latest global bb-browser package.

Mitigation: Pin and review the bb-browser dependency version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/salamankakit/skills/gumtree-uk-pets)
- [Gumtree UK](https://www.gumtree.com/)
- [bb-browser package](https://www.npmjs.com/package/bb-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON-producing bb-browser adapters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Gumtree search and listing outputs can include listing URLs, titles, prices, locations, snippets, descriptions, image URLs, and first-image Markdown.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
