## Description:

记忆雷达 helps agents scan memory files, logs, and workspace configuration for prompt injection patterns, credential exposure, exfiltration instructions, and related security concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and security reviewers use this skill to inspect AI agent memory files for prompt injection, leaked credentials, suspicious instructions, and cross-file threat patterns. It is intended for explicit memory-security scanning and review workflows, not unauthorized security assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags broad activation language, unclear scan scope, and read/execute/write authority.

Mitigation: Review the skill before installation, run it only for explicit memory-security scanning, and verify the exact files it will scan before granting access.

Risk: The artifact references scripts such as memory-scan.py, quarantine.py, and schedule-scan.sh, but the release artifact contains only SKILL.md.

Mitigation: Confirm the referenced scripts exist in the installed environment before following command examples or enabling scheduled scanning.

Risk: The optional --allow-remote mode may send redacted memory context to a remote LLM.

Mitigation: Keep local mode unless remote analysis is explicitly approved and the remaining context is acceptable to transmit.

Risk: Quarantine, restore, and cron setup behaviors can modify files or automate future scans.

Mitigation: Approve quarantine or scheduled execution only after checking backups, target paths, and the files that may be changed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memory-radar)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text guidance with shell command examples; described scan reports may use JSON, text, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include severity labels, file and line references, cross-file correlation notes, quarantine or restore guidance, and remediation recommendations.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact frontmatter says 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
