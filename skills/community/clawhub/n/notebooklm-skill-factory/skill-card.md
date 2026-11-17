## Description:

Orchestrates NotebookLM research into SKILL.md generation and Claude Code validation in a single automated pipeline for creating, testing, and iterating Claude Code skills from source materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kidcvs](https://clawhub.ai/user/kidcvs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to turn curated PDFs, articles, YouTube links, URLs, and other source materials into reusable Claude Code skills. It guides source collection, NotebookLM extraction, SKILL.md parsing, validation, security review, testing, and iterative fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill builds and installs AI-generated agent instructions from external source material, which may persist incorrect or unsafe behavior.

Mitigation: Use trusted sources, review the complete generated SKILL.md, and run validation and security checks before installation, overwrite, or test execution.

Risk: Private or sensitive documents used as sources may be sent through NotebookLM during skill creation.

Mitigation: Avoid private documents unless the user is comfortable using them with NotebookLM, and require a fresh review for each generated or updated skill.

## Reference(s):

- [NotebookLM CLI](https://github.com/UseClawPro/notebooklm)
- [Skill Extraction Prompt Template](references/skill-extraction-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated SKILL.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent skill files and validation/test guidance; generated skills require human review before installation or overwrite.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
