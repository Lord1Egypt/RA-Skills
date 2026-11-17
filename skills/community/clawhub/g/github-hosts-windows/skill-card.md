## Description:

Optimize GitHub access speed on Windows by finding low-latency IP addresses for GitHub domains and preparing hosts-file updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vay-qz](https://clawhub.ai/user/vay-qz)

### License/Terms of Use:

MIT-0

## Use Case:

Windows users and support engineers use this skill when GitHub access is slow and they want agent-generated PowerShell guidance to resolve candidate GitHub IPs, update hosts entries, and flush DNS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose persistent administrator-level changes to the Windows hosts file.

Mitigation: Use it only for an explicit GitHub hosts-file repair request, inspect the exact entries, and back up the hosts file before applying changes.

Risk: Incorrect or stale GitHub IP mappings can break GitHub access or cause certificate warnings.

Mitigation: Be prepared to remove the added entries or restore the hosts-file backup if GitHub access breaks or certificate warnings appear.

Risk: The PowerShell workflow has weak safeguards around privileged writes.

Mitigation: Review the generated commands before any administrator run and prefer manual entry when direct edits fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vay-qz/skills/github-hosts-windows)
- [Publisher profile](https://clawhub.ai/user/vay-qz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; may include administrator-level hosts-file edits and DNS cache flush commands.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
