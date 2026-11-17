## Description:

Scans and cleans Autodesk Maya scene malware on Windows using the portable maya_umbrella.exe CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and technical artists use this skill to scan Autodesk Maya .ma and .mb scene files for Maya Umbrella malware and, after explicit approval, clean infected scenes with auditable reports and backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup force-saves approved infected Maya scenes in place.

Mitigation: Scan first, disclose the exact affected files and report hash, require explicit cleanup approval, create adjacent _virus backups, and verify with a separate post-clean scan.

Risk: Installing or switching the portable CLI without review could run an unintended executable.

Mitigation: Review the exact repository, version, release asset, checksum asset, and LOCALAPPDATA destination before install; validate the CLI version and required scan/clean arguments before use.

Risk: Broad or ambiguous filesystem scope could scan or clean more Maya scenes than intended.

Mitigation: Resolve every requested path to an absolute existing directory, repeat --path for each target, and require explicit confirmation for broad roots such as drive roots, user profiles, or shared production roots.

Risk: Maya 2019-2021 cannot safely save non-ASCII scene paths through this scanner.

Mitigation: Stop on the scanner rejection and obtain a fresh scan and approval before using a different Maya version; do not move, rename, or copy scenes after approval.

## Reference(s):

- [Operation contract](references/operation-contract.md)
- [ClawHub skill page](https://clawhub.ai/loonghao/skills/maya-umbrella-batch-antivirus)
- [Publisher profile](https://clawhub.ai/user/loonghao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell command examples and JSON report references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only workflow for Autodesk Maya scene files; cleanup requires explicit user approval after scan evidence is reviewed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
