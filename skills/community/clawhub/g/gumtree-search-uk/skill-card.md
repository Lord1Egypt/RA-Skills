## Description:

Search Gumtree UK from the terminal with bb-browser for property, rentals, flatshares, second-hand goods, pets, used cars, and other local classifieds, returning structured JSON plus first-image Markdown for assistant workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salamankakit](https://clawhub.ai/user/salamankakit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and inspect Gumtree UK classifieds through bb-browser commands, comparing listings with prices, locations, descriptions, URLs, and image references.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: The listing adapter can fetch arbitrary full URLs when a non-Gumtree URL is supplied.

Mitigation: Pass only trusted Gumtree listing paths or https://www.gumtree.com URLs to gumtree/listing and review the adapter before installation.

Risk: Installing the adapter as a private bb-browser site override keeps the local Gumtree behavior active after setup.

Mitigation: Pin the bb-browser version used with the adapter and remove ~/.bb-browser/sites/gumtree when the override is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/salamankakit/skills/gumtree-search-uk)
- [Gumtree UK](https://www.gumtree.com/)
- [bb-browser package](https://www.npmjs.com/package/bb-browser)
- [bb-sites adapter pattern](https://github.com/epiral/bb-sites)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Structured JSON search and listing results with Markdown image snippets and inline shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bb-browser and local Gumtree adapter files; search reads public Gumtree HTML and listing detail accepts a Gumtree path or URL.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
