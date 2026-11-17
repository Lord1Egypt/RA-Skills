## Description:

Create and manage Obsidian Clip notes from web, article, or page URLs, with readable summaries saved under Clip/YYYY-MM in an Obsidian vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstract-sum](https://clawhub.ai/user/abstract-sum)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers use this skill to turn URLs into concise bilingual Obsidian clip notes with a theme, takeaways, usage actions, and optional limits. It is suited for personal knowledge management workflows that save Markdown notes into a configured Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled save script can be steered to write Markdown files outside the configured Obsidian vault.

Mitigation: Before using it with untrusted pages or copied metadata, restrict dates to YYYY-MM-DD, reject keywords with path separators or '..', and verify the final destination remains under the vault's Clip directory.

Risk: The skill writes local files into an Obsidian vault.

Mitigation: Install and run it only in environments where local Markdown writes to the configured vault are expected and acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abstract-sum/skills/obsidian-clip)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown notes with shell command usage for saving clips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English note headings; writes or appends Markdown files in an Obsidian vault.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
