## Description:

Generate NIH Biosketch documents compliant with the 2022 OMB-approved format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare NIH biosketch materials from structured researcher, contribution, support, and publication data. The packaged workflow can produce DOCX biosketch files or JSON publication/template outputs and can optionally retrieve publication metadata from PubMed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency setup may install an unintended package or unreviewed dependency versions.

Mitigation: Use an isolated virtual environment, prefer the documented python-docx package over requirements.txt as written, and pin reviewed dependency versions before installation.

Risk: PubMed features send publication identifiers or author queries to NIH services.

Mitigation: Run PubMed import or search only when the user is comfortable sharing those identifiers or queries with NIH.

Risk: Writable output paths can overwrite existing files.

Mitigation: Choose output paths deliberately inside the workspace and check for existing files before running generation commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/neoantigen-predictor)
- [NIH Biosketch Format Instructions](https://grants.nih.gov/grants/forms/biosketch.htm)
- [SciENcv](https://www.ncbi.nlm.nih.gov/sciencv/)
- [PubMed E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)
- [Audit Reference](references/audit-reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts may be DOCX or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires structured JSON input for biosketch generation; optional PubMed features use external NIH APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact body)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
