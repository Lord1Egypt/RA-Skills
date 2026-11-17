## Description:

Chinese-language contract review skill that checks real estate, construction, procurement, installation, and cooperation contracts against seven review principles and contract-editing habits, then suggests risk levels and revisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seairteng](https://clawhub.ai/user/seairteng)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, procurement, real estate, and operations users can use this skill to perform first-pass Chinese contract review, identify high- and medium-risk clauses, and draft directional revision suggestions. The output is advisory and should be reviewed by a qualified lawyer for significant business decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contracts and generated review reports can contain sensitive business terms or personal data.

Mitigation: Use an isolated local environment, restrict access to uploaded documents and generated Markdown reports, and avoid sharing reports outside the intended review workflow.

Risk: The skill provides directional contract-review suggestions and can miss issues or produce incorrect legal guidance.

Mitigation: Treat findings as first-pass review support and require qualified legal review before relying on the results for major commercial decisions.

Risk: The bundled script depends on python-docx and may render untrusted contract text into Markdown reports.

Mitigation: Pin and review dependencies, scan input files before processing, and render generated Markdown only in trusted viewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seairteng/skills/kt-legal-expert)
- [Publisher profile](https://clawhub.ai/user/seairteng)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown risk reports with clause findings, risk levels, and suggested edits; may include shell commands for running the bundled review script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can analyze docx, txt, and md contract files through the bundled Python script; generated reports may contain contract excerpts and should be handled as sensitive.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact changelog, released 2026-08-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
