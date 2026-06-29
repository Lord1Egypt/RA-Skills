## Description: <br>
Use when the user asks to inspect, triage, summarize, export, or safely update GitHub security alerts for code scanning, Dependabot, malware, or secret scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nick2bad4u](https://clawhub.ai/user/nick2bad4u) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect, triage, summarize, export, and safely update GitHub repository security alerts across code scanning, Dependabot, malware, and secret scanning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub tokens may be exposed if pasted into command arguments, logs, reports, or chat output. <br>
Mitigation: Use a least-privilege token from an environment variable or secret manager, keep secret values redacted, and avoid copying sensitive values into persistent outputs. <br>
Risk: Bulk alert updates can dismiss or resolve many findings incorrectly. <br>
Mitigation: Run dry-run mode first, apply narrow filters and limits, require clear dismissal or resolution comments, and verify the affected alerts afterward. <br>
Risk: The packaged scan did not include the helper scripts referenced by the documentation. <br>
Mitigation: Confirm the expected helper files are present before relying on command examples, or treat the skill as procedural guidance for equivalent GitHub REST API calls. <br>


## Reference(s): <br>
- [Source repository](https://github.com/Nick2bad4u/Github-Security-CodeScanning-Alerts-Skill) <br>
- [ClawHub skill page](https://clawhub.ai/nick2bad4u/skills/github-security-codescanning-alerts-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide GitHub REST API inspection and alert mutation workflows; use dry-run mode before bulk changes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
