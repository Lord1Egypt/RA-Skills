## Description: <br>
Advertised as an inverter and VFD parameter calculator, but security evidence identifies this release as a local note/data utility with add, list, search, remove, export, stats, and config commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill as a shell-driven local data-store utility for recording, listing, searching, removing, exporting, and configuring entries. Security evidence says not to rely on it for electrical, inverter, VFD, equipment status, or operational decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as an inverter or VFD calculator, but the security evidence identifies it as a local data-store utility. <br>
Mitigation: Use it only for local note/data tasks and do not rely on it for electrical calculations, equipment status, or operational decisions. <br>
Risk: Entries and configuration can persist under ~/.inverter or another INVERTER_DIR path and may be exported or deleted by command. <br>
Mitigation: Avoid storing secrets or sensitive operational details, review the data directory before export, and back up needed data before remove or delete workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/inverter) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may persist JSONL data and configuration under the INVERTER_DIR path, defaulting to ~/.inverter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
