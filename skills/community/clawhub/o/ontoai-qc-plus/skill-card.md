## Description:

Inspects AI-assisted deliverables for residual AI text, content errors, and compliance concerns, then produces a graded quality-check report before release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ontoai](https://clawhub.ai/user/ontoai)

### License/Terms of Use:

End User License

## Use Case:

Creators and teams review articles, code, data, documents, and multimedia before delivery. The skill identifies findings requiring correction, items needing verification, and checks that passed without editing the submitted work by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inspected documents, code, PDFs, or directories may be sent to a third-party paid service.

Mitigation: Obtain explicit consent before upload, limit the material to what is needed, and avoid broad directory scans.

Risk: Broad quality-check triggers may initiate a paid request or lead to follow-on edits.

Mitigation: Confirm user intent before invoking the service and require separate confirmation for payment or edits.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ontoai/skills/ontoai-qc-plus)
- [Publisher profile](https://clawhub.ai/user/ontoai)
- [Report template and output contract](artifact/references/report-template.md)
- [Quality-check dimensions](artifact/references/dimensions.md)
- [Publisher's paid service](https://www.ontoagent.net/qc402/)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, PDF]

**Output Format:** [Graded quality-check report in Markdown, with optional bilingual HTML or PDF presentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups findings as Must Fix, Should Fix, Unverified, and Passed; no follow-on edits without confirmation.]

## Skill Version(s):

2.1.2 (source: frontmatter, changelog, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
