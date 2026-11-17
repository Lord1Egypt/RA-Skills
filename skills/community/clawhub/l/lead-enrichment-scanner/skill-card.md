## Description:

Enriches B2B company leads from public websites by guessing domains and email patterns, scraping homepage descriptions and social links, and optionally using MiniMax LLM metadata extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzargona](https://clawhub.ai/user/jzargona)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, and developers can use this skill to create CSV lead-enrichment records from company names or domains before manual verification and compliant outreach decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead enrichment may collect scraped email addresses and produce guessed email patterns that are not verified contacts.

Mitigation: Use only public company data, verify addresses before any use, and follow CAN-SPAM, GDPR, and applicable local requirements.

Risk: MiniMax may receive company or lead details when MINIMAX_API_KEY is set and enrichment or draft generation runs.

Mitigation: Unset MINIMAX_API_KEY unless LLM processing is intended, and avoid using sensitive CRM exports or confidential lead data.

Risk: The implemented outreach-drafts command contradicts the documentation that says outreach drafts are not implemented in v1.0.

Mitigation: Review available commands before deployment and restrict use to enrichment workflows unless outreach drafting has been approved.

Risk: Writing to user-specified output paths may replace existing files.

Mitigation: Choose new output paths or back up existing CSV and Markdown files before running the skill.

## Reference(s):

- [Lead Enrichment Scanner ClawHub Listing](https://clawhub.ai/jzargona/skills/lead-enrichment-scanner)
- [jzargona Publisher Profile](https://clawhub.ai/user/jzargona)
- [Lead Enrichment Scanner Reference Docs](references/README.md)
- [Marketplace Listing Copy](references/marketing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [CSV lead-enrichment files, Markdown drafts, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network scraping uses public HTTPS homepages; optional MiniMax LLM calls may process company or lead details when MINIMAX_API_KEY is set.]

## Skill Version(s):

1.0.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
