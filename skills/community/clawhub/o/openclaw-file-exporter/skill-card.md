## Description:

Exports OpenClaw configuration files, skills, or other files by compressing them, uploading them to tmpfile.link, and returning formatted download details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eraycc](https://clawhub.ai/user/eraycc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to package OpenClaw skills, configuration files, or related files for temporary external sharing and backup through tmpfile.link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files or directories to a temporary hosting service, including sensitive files if an unsafe path is selected.

Mitigation: Use only with files approved for temporary external sharing; avoid configuration directories, credential stores, and other secret-bearing paths.

Risk: Returned tmpfile.link download links should be treated as public while they are active.

Mitigation: Share generated links only with intended recipients and avoid uploading data that requires private access control.

Risk: The script accepts a custom archive name, which could cause confusing or unsafe output names if supplied from untrusted input.

Mitigation: Choose simple archive names manually and review the source path and output name before running the upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eraycc/skills/openclaw-file-exporter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and formatted upload results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs a tmpfile.link download URL, encoded URL, file metadata, and the upload service response.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
