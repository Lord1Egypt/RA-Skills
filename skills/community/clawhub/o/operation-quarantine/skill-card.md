## Description:

Operation Quarantine scans email content and skill installations for prompt injection risk using pattern matching and optional LLM analysis before untrusted content reaches an OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dank-varley](https://clawhub.ai/user/dank-varley)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a local quarantine service and wrapper commands that scan untrusted emails or skill packages before an OpenClaw agent processes them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports verified gaps that can produce overly trusted clean results.

Mitigation: Treat the skill as an imperfect additional safety layer and retain human review plus least-privilege controls for sensitive content or skill installs.

Risk: Optional LLM analysis or webhook alerting can send scanned content outside the local machine when enabled.

Mitigation: Keep the default localhost binding, alerts disabled, and webhook egress disabled unless the deployment explicitly requires and reviews those settings.

Risk: Detection patterns can become stale as prompt injection techniques change.

Mitigation: Update or patch the scanner before relying on it for skill-install decisions.

## Reference(s):

- [ClawHub skill documentation](https://clawhub.ai/skills/operation-quarantine)
- [Signatures Directory](artifact/signatures/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown instructions with shell commands and JSON quarantine responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a localhost Node.js service; optional LLM analysis and webhook alerts require explicit configuration.]

## Skill Version(s):

1.0.3 (source: server release metadata and service/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
