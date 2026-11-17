## Description:

Paraphraser helps agents rewrite text for reduced repetition, academic tone, simpler wording, formal style, expansion, and before-and-after comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and agents can use this skill to prepare Markdown paraphrasing prompts for rewriting, academic restyling, simplification, formalization, expansion, and comparison of text drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags an unrelated local data-management script that silently stores user input.

Mitigation: Review the package before installing, avoid sensitive drafts or personal data, and prefer use only after the publisher removes or clearly documents the storage behavior.

Risk: Stored local text may persist under the user's data directory and can be listed, searched, or exported.

Mitigation: Set an isolated PARAPHRASER_DIR when testing, inspect retained files, and delete local data outside the tool if retention controls are not documented.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/skills/paraphraser)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prompts and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The paraphrasing commands emit prompt text; the package also includes a local data-management command that can store and export text.]

## Skill Version(s):

2.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
