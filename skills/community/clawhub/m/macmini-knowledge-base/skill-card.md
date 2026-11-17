## Description:

Sets up a local knowledge base and retrieval system on Mac mini, with document extraction and OCR, scheduled analysis, and optional Feishu summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seairteng](https://clawhub.ai/user/seairteng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Mac mini administrators use this skill to install and configure a local document knowledge base, extract and repair text from office files and PDFs, and optionally schedule analysis and Feishu summary delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic document processing may include folders intended to be excluded, allowing unintended contents to reach scheduled delivery.

Mitigation: Keep automatic delivery disabled until approved-folder boundaries are verified; review the scanned folders and Feishu recipient before enabling delivery.

Risk: Bulk OCR repair can overwrite archived summaries, and scheduled jobs continue running until removed.

Mitigation: Back up summaries before bulk repair, review the affected files, and inspect or remove persistent jobs with the OpenClaw cron commands.

Risk: Cron wrappers use hard-coded /Users/home paths that may not match the intended machine or workspace.

Mitigation: Verify and correct wrapper paths before enabling scheduled jobs.

## Reference(s):

- [ClawHub release](https://clawhub.ai/seairteng/skills/macmini-knowledge-base)
- [Ollama download](https://ollama.com/download)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and configuration examples; generated summaries are plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update summaries and catalogs, configure persistent scheduled jobs, and send summaries to a Feishu recipient when enabled.]

## Skill Version(s):

1.4.17 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
