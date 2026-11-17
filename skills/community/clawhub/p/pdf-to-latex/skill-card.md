## Description:

PDF to LaTeX helps agents convert PDF documents into LaTeX source with MinerU, including text, formulas, and document structure for academic and technical material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, graduate students, and academics use this skill to configure and run MinerU conversions from local PDF files or PDF URLs into editable LaTeX for revision, reference, or reproduction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party MinerU CLI/API, so PDF content may be handled under MinerU/OpenDataLab terms.

Mitigation: Review MinerU/OpenDataLab privacy, retention, and security terms before processing confidential PDFs.

Risk: Installing an unpinned CLI package or Go module can expose users to unexpected dependency changes.

Mitigation: Verify that mineru-open-api is the intended package or Go module and pin a known version where operational controls require reproducibility.

Risk: The VLM model path may produce rare hallucinations on complex layouts.

Mitigation: Use the pipeline mode when fidelity is more important than enhanced recognition, and review converted LaTeX before relying on it.

## Reference(s):

- [MinerU website](https://mineru.net)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [MinerU API token management](https://mineru.net/apiManage/token)
- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/pdf-to-latex)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and LaTeX file output from MinerU.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mineru-open-api CLI and MINERU_TOKEN; accepts local PDF files or PDF URLs and can write output to stdout or a directory.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
