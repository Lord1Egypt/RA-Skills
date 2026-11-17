## Description:

Security auditing skill that reviews OpenClaw SKILL.md files for prompt injection, data exfiltration, obfuscation, privilege escalation, persistence, and related malicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hichana](https://clawhub.ai/user/hichana)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to evaluate OpenClaw skill files before installation or release, receiving severity-based findings, evidence, and remediation guidance. When explicitly requested, it can draft a cleaned version for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally applies a strict, assume-malicious review posture and may produce false positives.

Mitigation: Review the reported evidence and remediation recommendations before acting on them or treating a verdict as conclusive.

Risk: The skill analyzes potentially untrusted skill content, which may contain malicious examples, prompt injection text, or unsafe commands.

Mitigation: Use it only on files you have permission to inspect, and do not execute code or commands from analyzed content during review.

Risk: Optional cleaned SKILL.md output is best-effort and may miss subtle attacks or remove legitimate functionality.

Mitigation: Manually review and test any cleaned version in a sandbox before installation or release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hichana/skills/one-skill-to-rule-them-all)
- [Publisher profile](https://clawhub.ai/user/hichana)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown security report with verdict, evidence, remediation recommendations, optional cleaned SKILL.md content, and disclaimer text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes content hashes, timestamps, line-numbered evidence, severity labels, and explicit warnings that results are not a security certification.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact notes SKILL.md v1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
