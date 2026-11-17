## Description:

Persona Forge helps agents record, review, search, and export local persona and character-creation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to keep local records of persona ideas, character profiles, trait analysis, comparisons, batch generation notes, and exports. The implementation is best understood as a local text logging and retrieval utility for character material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw prompts, character notes, and other entered text can be stored persistently on the local machine and later searched or exported.

Mitigation: Avoid entering sensitive personal, proprietary, or private story material unless the local files are managed and deleted appropriately.

Risk: The release is presented as a character creator, but the security evidence characterizes the bundled behavior as broad local text logging.

Mitigation: Review the artifact behavior before installation and use it only when local logging, search, and export are desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/persona-forge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local text file outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI use may create local log and export files under ~/.local/share/persona-forge.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
