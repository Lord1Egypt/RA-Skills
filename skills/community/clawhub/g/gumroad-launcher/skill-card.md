## Description:

Research a digital product niche, generate the product (ebook, template, script, checklist, or skill), write high-converting Gumroad sales copy, and publish the product listing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michelle447](https://clawhub.ai/user/michelle447)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and operators use this skill to research a digital product niche, create deliverables such as guides, templates, scripts, checklists, or skills, prepare Gumroad sales copy, and publish a listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish live Gumroad products using named accounts without enough confirmation or account verification.

Mitigation: Remove embedded account identifiers, require the user to choose and verify an authorized Gumroad store, and add an explicit preview-and-confirm step before any live API call.

Risk: Gumroad credentials could be exposed or misused if tokens or account details are placed directly in skill text or generated commands.

Mitigation: Keep Gumroad tokens out of the skill text and use only credentials for accounts the user is authorized to manage.

## Reference(s):

- [Gumroad Sales Copy Examples](references/copy-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/michelle447/skills/gumroad-launcher)
- [Gumroad API v2 Endpoint](https://api.gumroad.com/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with file paths, sales copy, pricing guidance, and API or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce product files and a live Gumroad listing URL when publishing is confirmed and authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
