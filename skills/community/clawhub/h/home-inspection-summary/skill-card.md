## Description:

Creates a clear, factual home inspection summary for US buyers with prioritized findings and no repair estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US home inspectors use this skill to turn inspection notes into buyer-friendly summaries organized by priority, with observable findings, limitations, and referrals to qualified professionals rather than repair estimates.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The supplied YAML format may omit findings, and supported Markdown notes may retain prices in the digest.

Mitigation: Compare every digest against the original inspection and remove any prices before sharing.

Risk: Each run overwrites digest.md in the selected output folder.

Mitigation: Use a dedicated output folder for each inspection.

## Reference(s):

- [US home inspection summary practices](references/home-inspection-summary.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/home-inspection-summary)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown digest organized into Safety, Major Issues, Minor Issues, Maintenance, Limitations, and guardrails sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes inspection notes with prioritized findings and locations; does not provide repair estimates. The digest file is overwritten on each run.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
