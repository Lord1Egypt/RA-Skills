## Description: <br>
Process Viewer is a Bash-based sysops logbook for recording process scans, monitoring notes, alerts, benchmarks, reports, and exports in local plaintext files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and sysops teams use this skill to record process observations, operational alerts, fixes, benchmarks, backups, and health review notes from the command line for later review or export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores entries as plaintext files in the user's home directory. <br>
Mitigation: Avoid entering passwords, tokens, regulated data, confidential incident details, or other sensitive information unless local storage protections and cleanup procedures are in place. <br>
Risk: Export files can copy local log contents into JSON, CSV, or TXT files. <br>
Mitigation: Review exports before sharing them and delete generated exports when they are no longer needed. <br>
Risk: Using the skill requires running a local Bash script. <br>
Mitigation: Review the bundled script and run it only in an environment where local plaintext logging is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/process-viewer) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with Bash command examples; CLI output is plain text and exports may be JSON, CSV, or TXT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local plaintext log and export files under the configured Process Viewer data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
