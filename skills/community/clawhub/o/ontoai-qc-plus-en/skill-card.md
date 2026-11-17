## Description:

Inspects submitted artifacts for AI residue, content errors, and compliance risks and returns a graded pre-delivery quality report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ontoai](https://clawhub.ai/user/ontoai)

### License/Terms of Use:

ontoAI QC Plus End User License Agreement

## Use Case:

Creators, editors, and developers use this paid skill to review articles, reports, code, data, and other deliverables before release without automatically editing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or confidential artifacts may be sent to the publisher's remote QC service.

Mitigation: Confirm what will be uploaded and obtain authorization before submitting directories, private repositories, or client files.

Risk: Broad quality-check phrases may initiate a remote paid workflow without clear per-artifact upload consent.

Mitigation: Require explicit confirmation of the artifacts and CNY 1.9 WeChat Pay charge before invoking the service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ontoai/skills/ontoai-qc-plus-en)
- [Inspection dimensions](references/dimensions.md)
- [Artifact types](references/artifact-types.md)
- [Report format](references/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, PDF]

**Output Format:** [Graded Markdown QC report, with optional HTML or PDF visual report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual reports group findings as Must Fix, Should Fix, Unverified, or Passed; full reports require payment per call.]

## Skill Version(s):

2.1.2 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
