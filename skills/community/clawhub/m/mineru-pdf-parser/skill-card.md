## Description:

Uses the MinerU API to parse PDFs into Markdown with support for formulas, tables, OCR, local files, and online URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-zxyz](https://clawhub.ai/user/alex-zxyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert academic papers and other PDF documents into Markdown for analysis, document extraction, and knowledge-base building.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents and the MinerU API token are sent to MinerU.

Mitigation: Use only with documents whose confidentiality requirements and MinerU privacy and retention terms are acceptable; keep the token in an environment variable and rotate it if exposure is suspected.

Risk: Downloaded result archives and extracted files are remote outputs that may be unsafe or malformed.

Mitigation: Treat downloaded results as untrusted, inspect outputs before reuse, and prefer a version with safe ZIP validation plus size and time limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alex-zxyz/skills/mineru-pdf-parser)
- [MinerU homepage](https://mineru.net)
- [MinerU project](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files and extracted result files saved locally, with command-line status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINERU_TOKEN; uses the MinerU API and stores results under ~/.openclaw/MinerU_Results/.]

## Skill Version(s):

3.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
