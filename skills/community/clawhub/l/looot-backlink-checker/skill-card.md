## Description:

Check a domain's backlinks. Use when the user says things like "check the backlinks of example.com", "who links to this page" or "find broken backlinks pointing at my site". Runs through looot, billed per call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walidboulanouar](https://clawhub.ai/user/walidboulanouar)

### License/Terms of Use:

MIT-0

## Use Case:

Website owners and SEO practitioners use this skill to review backlink totals, referring domains, anchor texts, and broken or spammy sources for a domain, subdomain, or page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A referenced path was not present in the security scan, so that path could not be checked.

Mitigation: Verify the missing path from a trusted source before installation, or proceed only if comfortable with the scan gap.

Risk: Backlink lookup runs are billed per call.

Mitigation: Inspect the endpoint price and input schema, then confirm the price with the user before each billable run.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/walidboulanouar/skills/looot-backlink-checker)
- [looot backlink checker guide](https://looot.ai/agent-skills/backlink-checker)
- [looot skill setup instructions](https://looot.ai/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown backlink summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backlink and referring-domain totals, top anchors, spam score, and broken backlink or page counts when returned by the selected endpoint.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
