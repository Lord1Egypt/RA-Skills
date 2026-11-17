## Description:

HTML Parse helps agents parse local HTML files or remote HTML URLs into structured Markdown with MinerU while preserving document hierarchy and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content managers, and data pipeline builders use this skill to convert HTML files, remote HTML URLs, and crawled pages into structured Markdown for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML content may be sent through MinerU, including local files, authenticated pages, intranet URLs, or regulated data.

Mitigation: Avoid parsing confidential, authenticated, intranet, or regulated content unless use of MinerU is approved for that data.

Risk: The skill depends on installing and running mineru-open-api from an external package source.

Mitigation: Install from trusted sources and prefer a pinned or reviewed version before use.

Risk: MINERU_TOKEN is required for extraction and crawl commands.

Mitigation: Set MINERU_TOKEN only in environments where this tool needs access and avoid exposing it in shared shells, logs, or committed configuration.

## Reference(s):

- [ClawHub HTML Parse skill page](https://clawhub.ai/mzlzyca/skills/html-parse)
- [MinerU homepage](https://mineru.net)
- [MinerU token management](https://mineru.net/apiManage/token)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses mineru-open-api with MINERU_TOKEN; document content is written to stdout by default or saved with -o.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
