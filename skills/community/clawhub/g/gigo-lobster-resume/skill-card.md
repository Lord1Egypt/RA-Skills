## Description: <br>
Resume entrypoint for GIGO Lobster benchmark runs; the v2 stable runtime currently starts fresh while preserving this slug for legacy checkpoint compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gigolab](https://clawhub.ai/user/gigolab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this companion skill to resume or restart a GIGO Lobster benchmark run, monitor progress, and produce benchmark outputs such as reports, certificates, logs, and optional cloud results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary flags this as a real benchmark runner with high-impact behavior that users should review before installing. <br>
Mitigation: Install only when a GIGO cloud benchmark runner is intended, and review the skill behavior before execution. <br>
Risk: The server security guidance notes local code execution, dependency installation, use of gateway/profile/secret settings, network calls, default result upload, and possible checkpoint reset. <br>
Mitigation: Run in an isolated workspace and use local, offline, skip-upload, or another companion skill when cloud submission or checkpoint changes are not desired. <br>
Risk: The server evidence includes sensitive-credential capability tags. <br>
Mitigation: Confirm gateway and profile credentials before running, and avoid executing the benchmark in shared or production workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gigolab/gigo-lobster-resume) <br>
- [Publisher Profile](https://clawhub.ai/user/gigolab) <br>
- [Skill README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Bundle README](artifact/bundle/README.md) <br>
- [Scoring Specification](artifact/bundle/specs/scoring.md) <br>
- [Task Schema Specification](artifact/bundle/specs/task-schema.md) <br>
- [Judge Protocol Specification](artifact/bundle/specs/judge-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files, Markdown] <br>
**Output Format:** [Markdown progress updates with shell commands and generated benchmark files such as HTML reports, PNG or SVG certificates, logs, and result metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform network calls and upload results by default unless local, offline, or skip-upload options are used.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
