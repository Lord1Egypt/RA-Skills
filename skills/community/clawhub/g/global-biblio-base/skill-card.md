## Description:

Searches and retrieves Chinese and international academic literature through the SmartLib Open Platform, including bibliographic details and available full-text downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and other literature users can search Chinese and international publications, patents, standards, and theses, review bibliographic details, and request available full text. Account registration and quota use may apply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an authentication secret in the package.

Mitigation: Do not expose or reuse a credential shipped with the package; remove it from shared copies and rotate it if it is active.

Risk: The security evidence raises concerns about cross-session persistence and external sharing of research terms.

Mitigation: Review what query and account data the service retains or receives, and avoid sending sensitive research terms until those practices are understood.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/j-levee/skills/global-biblio-base)
- [Publisher profile](https://clawhub.ai/user/j-levee)
- [SmartLib website](https://www.vipslib.com/)
- [Account and quota guide](artifact/references/account.md)
- [Search and retrieval pipeline guide](artifact/PIPELINE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Links]

**Output Format:** [Markdown literature results, bibliographic details, and available PDF download links or files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require email registration; metered API searches and downloads can use account quotas. Full text is available only where supported, including open-access sources.]

## Skill Version(s):

3.10.10 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
