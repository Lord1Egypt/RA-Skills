## Description:

Writes LinkedIn sponsored content for a specified job title and company size, then checks drafts against character limits and configured hype-word rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External US B2B demand-generation teams and agency media buyers use the skill to draft LinkedIn sponsored-content copy for a specified job title, company size, industry, and trigger event, then check it against documented field limits and copy guardrails.

### Deployment Geography for Use:

United States (US-focused guidance)

## Known Risks and Mitigations:

Risk: A clean lint report does not guarantee policy-compliant copy, and the checks are incomplete.

Mitigation: Manually verify completed sections, field limits, factual claims, and applicable platform rules before use.

Risk: An optional Windows app is not required for this workflow and has not been established as safe by its checksum alone.

Mitigation: Avoid the optional app unless it receives a separate security review; do not treat the supplied checksum as proof of safety.

Risk: Running the linter can replace an existing lint-report.md in the selected output folder.

Mitigation: Choose an output folder where replacing lint-report.md is acceptable.

## Reference(s):

- [LinkedIn ad specifications and checklist](artifact/references/linkedin-ad-specs.md)
- [ClawHub release page](https://clawhub.ai/rapidworker1/skills/linkedin-ads-copy-generator)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown ad-copy draft and lint report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft fields follow documented format-specific character limits; the lint report lists detected overlong fields and configured banned phrases.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
