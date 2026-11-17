## Description:

Human-machine interface design tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to run a local shell-based entry manager that records, lists, searches, removes, exports, and configures data under a user-controlled HMI directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifacts behave like a local entry/log manager rather than the advertised HMI design tool.

Mitigation: Review the script behavior before installing and confirm it matches the intended operational use.

Risk: Entries and configuration are persisted, deleted, exported, and configured under ~/.hmi or a custom HMI_DIR.

Mitigation: Run the skill only as a normal user in directories you control, and avoid storing sensitive data unless storage, deletion, and export handling are improved.

Risk: JSONL and CSV handling may not safely escape arbitrary user-provided values.

Mitigation: Add robust JSON and CSV escaping or validation before using the skill with untrusted or sensitive input.

Risk: Removal, export, and configuration writes may overwrite or alter local files without stronger protections.

Mitigation: Add removal confirmation, configuration input validation, and overwrite or symlink protections before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/hmi)
- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub publisher profile](https://clawhub.ai/user/bytesagain1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with JSONL data files and optional JSON or CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 on success and 1 on error.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
