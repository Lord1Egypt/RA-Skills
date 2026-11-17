## Description:

Read meeting minutes or notes from a local file path or URL, or inspect a local meeting-notes directory and report the file count plus file list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaocaijic](https://clawhub.ai/user/xiaocaijic)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to read meeting notes from trusted local files or URLs and answer questions about decisions, action items, conclusions, and discussion content. It can also list supported meeting-note files in a local directory when the user asks for counts or file names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted URL fetching can retrieve untrusted or permission-gated meeting documents.

Mitigation: Use trusted meeting-document URLs only and run the skill with network egress controls when URL fetching is allowed.

Risk: Windows directory listing has a command-injection risk.

Mitigation: Avoid Windows use until the PowerShell directory listing is replaced with Python-only enumeration or properly parameterized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaocaijic/skills/meeting-minutes-retriever)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses, with JSON strings returned by the directory listing helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads raw meeting text from a local path or URL; directory listings include directory, recursion flag, supported extensions, total file count, and file paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
