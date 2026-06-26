## Description: <br>
A local shell utility advertised for Modbus tasks that stores, searches, deletes, and exports entries under a configurable data directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to run bundled shell commands for maintaining a local JSONL log and configuration associated with Modbus-related notes or tasks. It should not be relied on for Modbus device communication or status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Capability mismatch: security evidence says the artifact behaves as a local log and configuration utility, not as a Modbus communication or status-checking tool. <br>
Mitigation: Treat it only as local data management; do not use it to assess, monitor, or control Modbus devices. <br>
Risk: Local data exposure or loss: the script stores entries under ~/.modbus by default, can delete entries, and can export stored data. <br>
Mitigation: Set MODBUS_DIR deliberately, avoid storing sensitive operational details, review exports before sharing, and back up data before removal. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ckchzh/modbus) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Terminal text with local JSONL, JSON, or CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes under MODBUS_DIR or ~/.modbus by default and can export modbus-export.json or modbus-export.csv in the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
