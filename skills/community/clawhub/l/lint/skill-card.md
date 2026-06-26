## Description: <br>
Lint provides shell commands for recording and searching local lint-related activity logs rather than performing syntax or style checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers can use this skill to record lint-related checks, formatting notes, fixes, and reports in local timestamped logs, then search or export those records. It should not be relied on to perform linting, style enforcement, syntax checking, or CI gating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is presented as a linting and auto-fix tool, but the security review identifies it as a local logbook that does not actually lint, enforce style, fix code, or gate CI. <br>
Mitigation: Use it only for recording lint-related notes; run trusted linters, formatters, and CI checks separately before relying on results. <br>
Risk: Users may enter secrets, proprietary code, credentials, or sensitive review details into local logs that can be searched or exported. <br>
Mitigation: Avoid recording secrets or sensitive code, and review local log and export files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/lint) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance and CLI-style text output; exports can be JSON, CSV, or TXT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries locally under ~/.local/share/lint and can export collected logs.] <br>

## Skill Version(s): <br>
2.0.1 (source: release evidence; artifact metadata reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
