## Description: <br>
Memory Guard monitors and verifies agent workspace files to detect unauthorized changes, injection attacks, personality drift, and cross-agent contamination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Memory Guard to add local integrity checks around agent memory and workspace files, review verification or audit reports, and update trust baselines only after human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accepting a new trust baseline can preserve unauthorized file changes if it is run before review. <br>
Mitigation: Run verify and audit first, review the reported changes, and use accept only for states the user intends to trust. <br>
Risk: Stamping a file rewrites the selected file in place. <br>
Mitigation: Use stamp only on intended memory files and review or back up important content before rewriting it. <br>
Risk: Integrity checks are only as reliable as the baseline captured during initialization. <br>
Mitigation: Initialize tracking from a trusted workspace state and run verification regularly before relying on memory files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cassh100k/memory-guard) <br>
- [Publisher homepage](https://nixus.pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local hash registries, audit logs, and optional provenance stamps when the user runs the bundled shell commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
