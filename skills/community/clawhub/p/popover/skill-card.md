## Description: <br>
Generate popover UI elements and design assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers may use this skill when they want agent guidance for building interface popovers and related visual components. Security evidence indicates the included script behaves as a local text-entry manager rather than a popover UI generator, so users should review behavior before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a popover UI generator, but security evidence reports that the included script stores, deletes, searches, and exports user-provided text. <br>
Mitigation: Review the script behavior before use and install only if a simple local text-entry manager is intended. <br>
Risk: Local entries may retain sensitive notes in the default data directory or a custom POPOVER_DIR. <br>
Mitigation: Avoid storing secrets or sensitive notes and inspect the configured data directory before and after use. <br>
Risk: Export writes files into the current working directory. <br>
Mitigation: Run export only from a directory where creating popover export files is expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/popover) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May manage local text entries in a user-selected data directory and export data files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
