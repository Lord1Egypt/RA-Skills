## Description:

Generate and update table-of-contents (TOC) sections for Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation maintainers use this skill to generate or refresh navigable Markdown tables of contents for long documents, READMEs, and technical guides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the local Python script reads the Markdown file path supplied by the user.

Mitigation: Run it only on Markdown files you intend the agent to inspect.

Risk: Using the in-place option modifies the target Markdown file.

Mitigation: Preview the generated TOC without the in-place option first, then use in-place mode only on files you intend to update.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/md-toc-generator)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown table of contents text, with optional in-place Markdown file updates when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads the target Markdown file and writes changes only when the in-place option is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
