## Description: <br>
Motor specification and selection tool <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to run a local shell tool for recording, listing, searching, exporting, and managing motor-related entries. It should not be relied on as a validated motor selection system without review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill behaves like a persistent local entry store rather than a real motor specification or selection tool. <br>
Mitigation: Review the tool before installation and do not treat saved entries as validated motor selection guidance. <br>
Risk: The security guidance warns that entries are stored as plaintext under ~/.motor by default. <br>
Mitigation: Avoid storing secrets or sensitive project data and set MOTOR_DIR to an approved local directory when needed. <br>
Risk: The security guidance notes that export and remove behavior copies or mutates saved entries. <br>
Mitigation: Review generated exports and deletion targets before running export or remove. <br>


## Reference(s): <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain1) <br>
- [Skill page](https://clawhub.ai/bytesagain1/motor) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Plain text stdout with JSONL storage and optional JSON or CSV export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries under MOTOR_DIR or ~/.motor by default and can export motor-export.json or motor-export.csv.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
