## Description:

Extracts readable text from PowerPoint (.pptx) files with MinerU, producing Markdown or JSON outputs from local files or URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert PowerPoint slide decks into readable text for search indexing, content review, NLP preprocessing, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentations may contain confidential data and the skill depends on MinerU document handling.

Mitigation: Send slide decks to MinerU only when its service terms, data handling, and token handling are acceptable for the intended use case.

Risk: The documented install commands use mutable global package installation paths.

Mitigation: Prefer pinned package versions, avoid elevated privileges during installation, and review the package source before deployment.

Risk: The quick extraction path has documented size and page limits and returns Markdown rather than true plain text.

Mitigation: Use JSON extraction when structured text fields are required and validate extracted content before downstream processing.

## Reference(s):

- [MinerU homepage](https://mineru.net)
- [MinerU repository](https://github.com/opendatalab/MinerU)
- [MinerU token management](https://mineru.net/apiManage/token)
- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/pptx-to-text)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; extracted presentation content is Markdown by default or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [flash-extract can write to stdout or an output directory; full JSON extraction requires MINERU_TOKEN.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
