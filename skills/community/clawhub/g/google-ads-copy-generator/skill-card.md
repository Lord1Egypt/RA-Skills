## Description:

Writes Google Search and Performance Max ad copy from a product brief, with every field checked against the real character limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

Media buyers, agencies, and US direct-to-consumer brands use this skill to prepare Google Search and Performance Max ad copy, check draft RSA field lengths, and identify claims that need supporting evidence before ads are used.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The security evidence reports a suspicious, medium-confidence mismatch between the advertised ad-copy generation and the checking behavior; it does not establish malicious intent.

Mitigation: Review the generated result against the requested ad-copy task and the supplied brief before using or sharing it.

Risk: The security evidence says file-writing scope is undeclared and the scan was partial because some referenced paths were missing.

Mitigation: Review the script and chosen output directory before running it, use a dedicated output folder, and inspect the generated files.

## Reference(s):

- [Google Ads limits and US claim rules](artifact/references/google-ads-limits.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with grouped headlines, descriptions, and claim checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responsive Search Ad headlines are limited to 30 characters and descriptions to 90 characters; claims should be paired with evidence supplied by the user.]

## Skill Version(s):

1.0.7 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
