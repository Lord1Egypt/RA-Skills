## Description:

Mindmap is a terminal note-capture utility for adding, listing, searching, and exporting local plain-text entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and terminal users can capture lightweight notes, search local entries, and export them for downstream analysis. Treat it as local plain-text note storage rather than a mind-map visualization tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is marketed as a mind-map tool, but security evidence says it behaves as a local logging or note-capture utility.

Mitigation: Evaluate and present it as local note storage, and do not rely on it for mind-map visualization unless separately verified.

Risk: Entries and command history may be retained as plain text in the configured data directory.

Mitigation: Avoid storing sensitive information, use a dedicated data directory when needed, and inspect stored logs before sharing or backing them up.

Risk: The remove command logs removal but does not remove stored data.

Mitigation: Do not rely on the remove command for deletion; manually edit or delete retained data and history logs when removal is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/mindmap)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and append plain-text data and history logs under the configured local data directory.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact files report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
