## Description:

Pre-install security scanner for AI agent skills. Detects malicious patterns before you trust code. Local-first - code never leaves your machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamthompson33](https://clawhub.ai/user/adamthompson33)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use Moltcops to scan agent skill directories before installing or running them, then review PASS, WARN, or BLOCK findings for malicious patterns such as prompt injection, code execution, credential access, persistence, and data exfiltration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning an untrusted extracted skill may cause the scanner to read files outside the chosen folder.

Mitigation: Scan untrusted skills inside a sandbox or container with limited filesystem access until the symlink issue is fixed.

Risk: A PASS verdict is a triage signal, not a guarantee that a skill is safe.

Mitigation: Review scanner findings and the skill contents before installing or running the skill.

## Reference(s):

- [Moltcops ClawHub Skill Page](https://clawhub.ai/adamthompson33/skills/moltcops)
- [MoltCops Website](https://moltcops.com)
- [MoltCops Web Scanner](https://scan.moltcops.com)
- [MoltCops Moltbook Profile](https://moltbook.com/u/MoltCops)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with verdict summary and findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses exit code 0 for PASS, 1 for WARN, and 2 for BLOCK.]

## Skill Version(s):

1.1.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
