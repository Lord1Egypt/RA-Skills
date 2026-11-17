## Description:

Generates Chinese official-document DOCX files from Markdown or JSON with standardized title, heading, font, paragraph, page-number, and punctuation formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujiang817](https://clawhub.ai/user/liujiang817)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user needs a Chinese official-style Word document, report, summary, speech material, or similar formal document generated or reformatted from Markdown or structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the formatter to run for ordinary reports, summaries, or materials that do not need Chinese official-document formatting.

Mitigation: Review ambiguous user requests before invoking the skill and confirm that official-document formatting is desired.

Risk: The install script installs python-docx without a pinned version.

Mitigation: Use a locked dependency workflow or pin python-docx before running the install script in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujiang817/skills/my-docx-formatter)
- [Publisher profile](https://clawhub.ai/user/liujiang817)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [DOCX files generated from Markdown or JSON inputs, with Markdown usage examples and shell commands for invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local .docx files and may install python-docx into a local virtual environment before use.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
