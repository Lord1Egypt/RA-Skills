## Description:

Paper Parser helps agents parse academic papers and research PDFs with MinerU, extracting structured content such as titles, abstracts, sections, figures, tables, formulas, and references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, graduate students, and academic content workflows use this skill to guide agents through extracting structured content from research PDFs and paper URLs with MinerU.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and running the third-party MinerU CLI.

Mitigation: Install MinerU only from the expected publisher or source, avoid elevated privileges, and pin a version where practical.

Risk: MinerU authentication uses MINERU_TOKEN.

Mitigation: Expose MINERU_TOKEN only when needed and keep it out of logs, prompts, and shared configuration.

Risk: PDF files or URLs submitted through MinerU may be processed by MinerU's API service.

Mitigation: Confirm document handling requirements before submitting confidential, regulated, or third-party-restricted papers.

## Reference(s):

- [Paper Parser on ClawHub](https://clawhub.ai/mzlzyca/skills/paper-parser)
- [MinerU](https://mineru.net)
- [OpenDataLab MinerU GitHub Repository](https://github.com/opendatalab/MinerU)
- [MinerU Token Management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include MinerU CLI commands, token setup steps, PDF input notes, model selection, output directory usage, and parsing constraints.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
