## Description: <br>
Provides command guidance for a local pid CLI that records, lists, searches, removes, exports, and configures plaintext entries under a user data directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to invoke a simple local record manager for adding, listing, searching, deleting, exporting, and configuring entries. Security evidence indicates the artifacts do not implement PID controller tuning or simulation despite the package description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release describes a PID tuning and simulation tool, but the security summary says the artifacts implement a local note or log manager instead. <br>
Mitigation: Install only when the desired behavior is local record management, and verify artifact behavior before relying on it for control-system analysis. <br>
Risk: User-provided entries, configuration values, and exports may be stored as plaintext under ~/.pid or PID_DIR. <br>
Mitigation: Do not enter secrets, credentials, or sensitive operational data unless plaintext local storage, search, deletion, and export are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/pid) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output as plaintext, JSONL, or CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local entries and configuration under PID_DIR, defaulting to ~/.pid.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
