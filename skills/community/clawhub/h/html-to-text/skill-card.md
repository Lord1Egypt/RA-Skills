## Description:

Convert HTML files and web pages into readable text using MinerU, with Markdown output as the closest plain-text format and JSON output available for text fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to strip markup from local HTML files or web page URLs and extract readable content for indexing, NLP pipelines, text analysis, or other workflows that need clean HTML-derived text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local HTML files or URLs may be processed through MinerU using an access token.

Mitigation: Use non-sensitive HTML and public URLs unless MinerU handling is acceptable for the data.

Risk: Install instructions reference mutable third-party packages.

Mitigation: Install in an isolated environment, pin and verify package versions, and avoid elevated shells.

Risk: The workflow depends on MINERU_TOKEN authentication.

Mitigation: Use a narrowly scoped, revocable token and rotate it if exposed.

## Reference(s):

- [HTML to Text on ClawHub](https://clawhub.ai/mzlzyca/skills/html-to-text)
- [MinerU homepage](https://mineru.net)
- [MinerU repository](https://github.com/opendatalab/MinerU)
- [MinerU token management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and optional JSON text fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses mineru-open-api with MINERU_TOKEN; HTML extraction returns Markdown or JSON text fields rather than a native text format.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
