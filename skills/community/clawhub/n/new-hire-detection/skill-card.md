## Description:

Helps revenue teams adapt a Cargo workflow that finds recent decision-maker hires, qualifies their new companies against an ICP, and posts approved matches to Slack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue operations and sales-development teams use this example to build an ICP-qualified new-hire monitoring workflow in their Cargo project. After adaptation and approval, it posts matching hires to a designated Slack channel; CRM routing is an optional, separately approved variation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned external tooling can introduce unreviewed changes.

Mitigation: Review and preferably pin Cargo and cargo-project tooling versions before installation.

Risk: New-hire details could be posted to an unintended Slack audience.

Mitigation: Confirm the destination channel and its audience, then review posts during the ten-record pilot.

Risk: Recurring searches can incur repeated extraction and qualification costs.

Mitigation: Count the search, review estimated cost and pilot results, and add a schedule only after approval.

Risk: Optional CRM routing can create or update records and tasks.

Mitigation: Obtain separate approval for CRM routing and review its effects before enabling it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cargo-ai/skills/new-hire-detection)
- [Publisher-listed project homepage (not verified provenance)](https://github.com/getcargohq/gtm-skills)
- [Search setup](references/search.md)
- [Run and pilot guidance](references/run.md)
- [Optional CRM adaptation](references/crm-adaptation.md)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [TypeScript project resources and Markdown instructions; qualified hires appear as Slack posts after deployment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires project-specific ICP, search filters and a designated Slack channel; the example is not deploy-verified and does not deploy or post on its own.]

## Skill Version(s):

0.1.3 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
