## Description: <br>
Lockout tagout safety procedure manager. Use when json lockout tasks, csv lockout tasks, checking lockout status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, safety coordinators, and operations teams can use this skill to run a local command-line lockout/tagout record manager for adding, listing, searching, exporting, and checking lockout entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps local lockout/tagout records and configuration on disk. <br>
Mitigation: Confirm the approved data location before use, set LOCKOUT_DIR if needed, and apply organizational retention and audit controls. <br>
Risk: Remove and export behavior may not meet operational safety record requirements without review. <br>
Mitigation: Validate remove/export behavior against internal procedures before relying on the records for operational safety workflows. <br>


## Reference(s): <br>
- [Lockout on ClawHub](https://clawhub.ai/xueyetianya/lockout) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell command examples; the CLI emits terminal text and can export JSON or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local records under LOCKOUT_DIR or ~/.lockout by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
