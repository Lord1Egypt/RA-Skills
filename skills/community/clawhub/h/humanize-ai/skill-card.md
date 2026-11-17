## Description:

Humanize AI helps agents analyze local text for common AI-writing patterns and apply Python-based replacements for filler phrases, chatbot artifacts, curly quotes, and optional dash cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artur-zhdan](https://clawhub.ai/user/artur-zhdan)

### License/Terms of Use:


## Use Case:

External users, developers, and content editors use this skill to audit local text for AI-writing patterns, rewrite common filler and chatbot artifacts, and review flagged vocabulary before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch rewriting can accidentally overwrite matching text files in place.

Mitigation: Run report-only analysis first, write rewritten output to a separate file, keep backups, and review changes before replacing originals.

Risk: Automated phrase replacements can change meaning, tone, or context.

Mitigation: Review rewritten output manually, especially vocabulary and puffery findings that require human judgment.

## Reference(s):

- [Humanize AI skill page](https://clawhub.ai/artur-zhdan/skills/humanize-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and optional text or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read from stdin or local files and may write rewritten text to an output file when requested.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
