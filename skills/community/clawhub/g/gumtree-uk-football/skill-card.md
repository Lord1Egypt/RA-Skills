## Description:

Searches Gumtree UK for football-related goods and ticket-style listings with bb-browser, returning structured listing data and first-image Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salamankakit](https://clawhub.ai/user/salamankakit)

### License/Terms of Use:

MIT-0

## Use Case:

External buyers, sellers, and agent operators use this skill to search Gumtree UK for football shirts, boots, memorabilia, trading cards, football games, and ticket-style listings, then inspect listing details and images before making commerce decisions.

### Deployment Geography for Use:

Global, focused on Gumtree UK listings.

## Known Risks and Mitigations:

Risk: The listing helper can fetch arbitrary HTTP URLs instead of only Gumtree listing URLs.

Mitigation: Only run listing lookups with real Gumtree listing paths or https://www.gumtree.com URLs, and review prompts before execution.

Risk: Ticket-style listings may involve fraud, resale restrictions, or off-platform payment pressure.

Mitigation: Verify seller identity, face-value and resale rules, and avoid encouraging off-platform payments to strangers.

Risk: Copied bb-browser site scripts remain installed after the skill is no longer needed.

Mitigation: Remove the copied ~/.bb-browser/sites/gumtree scripts when retiring the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/salamankakit/skills/gumtree-uk-football)
- [Gumtree UK](https://www.gumtree.com/)
- [bb-browser package](https://www.npmjs.com/package/bb-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-capable bb-browser outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Gumtree search and listing helpers; listing output may include image URLs and first-image Markdown.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
