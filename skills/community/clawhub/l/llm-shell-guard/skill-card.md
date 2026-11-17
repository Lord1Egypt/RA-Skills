## Description:

Blocks destructive Linux commands by enforcing allowlist execution, denylist checks, regex detection, protected paths, and approval for risky actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jurgenw81](https://clawhub.ai/user/jurgenw81)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to evaluate proposed Linux shell commands before execution, returning allow/block decisions and reasons based on allowlists, deny rules, protected paths, and approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Treating the skill as a complete security boundary could allow unsafe command execution if an integration relies only on its advisory decision.

Mitigation: Use it as a defensive advisory layer with a locked-down sandbox or microVM, non-root execution, restricted mounts, network limits, resource limits, canonical trusted paths, a sanitized environment, and fail-closed parser handling.

Risk: Parser gaps or policy misconfiguration could allow commands outside the operator's risk tolerance.

Mitigation: Keep the allowlist small and mostly read-only, review rule files before deployment, require manual approval for high-risk binaries, and test policy changes against bypass attempts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jurgenw81/skills/llm-shell-guard)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [CLI text or JSON decision output with Markdown skill guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory allow/block decisions can include the reason, matched rule, base command, and policy guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
