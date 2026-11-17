## Description:

Submits code-generation tasks to Huawei Cloud CodeArts through its CLI and provides guidance for configuring access, permissions, and generated-code output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to submit code-generation tasks to Huawei Cloud CodeArts, configure and verify CLI access, and save generated code locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install software automatically and grant file access beyond the workspace the user approves.

Mitigation: Review the installation step, explicitly opt in to file access, and limit the permission scope to the workspace.

Risk: The skill handles Huawei Cloud credentials, and the downloaded installer and CLI have not been audited.

Mitigation: Use minimally privileged credentials, store them safely, attach only authorized files, and remove saved keys afterward. Review the installer and CLI before use.

## Reference(s):

- [Acceptance criteria](artifact/references/acceptance-criteria.md)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)
- [IAM policies](artifact/references/iam-policies.md)
- [JSON output parsing](artifact/references/json-output-parsing.md)
- [Status handling](artifact/references/status-handling.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated code and files, with Markdown guidance and structured JSON status or CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code is returned for the agent to parse and write to disk.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
