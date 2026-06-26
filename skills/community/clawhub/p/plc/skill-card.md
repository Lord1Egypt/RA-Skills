## Description: <br>
Programmable logic controller programming helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and industrial automation practitioners can use Plc as a local CLI helper for recording, listing, searching, exporting, and configuring PLC-related entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security verdict is suspicious because the skill presents as a PLC helper while managing generic local user data. <br>
Mitigation: Review SKILL.md and scripts/script.sh before installation, and confirm the local data model and commands match the intended PLC workflow. <br>
Risk: Entries and configuration are stored locally under ~/.plc by default and may contain sensitive operational notes if users add them. <br>
Mitigation: Avoid storing credentials, secrets, customer data, or sensitive operational details unless local storage behavior and access controls are acceptable. <br>
Risk: Remove, export, and config commands can alter or copy locally stored data. <br>
Mitigation: Check command arguments and output paths before running mutating or export commands, and back up important local data before removal. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/plc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; the helper emits structured stdout and JSONL or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local PLC_DIR data directory, defaulting to ~/.plc, and stores entries in JSONL format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
