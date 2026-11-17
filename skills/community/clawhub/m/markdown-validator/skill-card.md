## Description:

Validates Markdown files for broken local links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:


## Use Case:

Developers and documentation maintainers use this skill to scan Markdown files or directories for broken local links before publishing or maintaining documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included test script writes and deletes test.md and broken.md in the current working directory.

Mitigation: Run npm test only in a temporary or disposable directory until the test script isolates its files.

Risk: The skill recursively reads Markdown files under the supplied target path.

Mitigation: Run it only on directories intended for local documentation checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanng-ide/skills/markdown-validator)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON report with file validity, broken link details, and line numbers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Skips external HTTP(S) URLs and same-file anchors.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
