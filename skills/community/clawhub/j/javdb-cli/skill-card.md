## Description:

Operate the installed JavDB CLI to discover titles and entities, read lists, and perform explicitly authorized account, configuration, marking, or preview-asset actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flanchanxwo](https://clawhub.ai/user/flanchanxwo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate the installed JavDB CLI for scoped discovery, personal lists, and explicitly requested account, configuration, watch/want, or preview-asset actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner assessment is benign with medium confidence, and Skillspector’s review was partial because three local references could not be resolved.

Mitigation: Review the documented update and installation guidance, and use only features that fit the requested task.

Risk: Image search uploads the selected image to AVScan or another configured provider.

Mitigation: Use image search only with an image the user has authorized for upload, and explain the upload when it matters to the task.

Risk: The local JavDB authentication file contains passwords and JWTs.

Mitigation: Never read, display, upload, or include the authentication file or its contents in diagnostics.

## Reference(s):

- [JavDB CLI project homepage](https://github.com/FlanChanXwO/javdb-cli)
- [JavDB CLI skill release](https://clawhub.ai/flanchanxwo/skills/javdb-cli)
- [Authentication and accounts](artifact/references/auth.md)
- [Discovery and navigation](artifact/references/discover.md)
- [Installation and updates](artifact/references/install.md)
- [Preview media assets](artifact/references/media.md)
- [Explicit state changes](artifact/references/state.md)
- [Errors, network, and routing](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, JSON, NDJSON, shell commands, guidance]

**Output Format:** [Human-readable text, JSON, or NDJSON, with shell commands for invoking javdb]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results follow the requested command scope; structured output distinguishes movie, list, entity, and magnet records, and partial failures remain visible.]

## Skill Version(s):

0.8.5 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
