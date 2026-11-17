## Description:

Prompt Injection Firewall for AI agents. 113 detection patterns, 14 threat categories, zero dependencies. Protects against fake authority, command injection, memory poisoning, skill malware, crypto spam, and more. Hash-chain tamper-proof whitelist with mandatory peer review. Claude Code hook integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stlas](https://clawhub.ai/user/stlas)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Prompt Shield to scan prompts or batches for prompt injection, spam, and malicious skill behavior. It can also be wired into Claude Code hooks to warn on or block risky input before an agent processes it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the Claude Code hook makes Prompt Shield run on future Claude Code inputs.

Mitigation: Review the hook script before installation and enable it only in environments where this persistent prompt-scanning behavior is expected.

Risk: The whitelist peer-review model is not a strong security boundary without authenticated approver identity.

Mitigation: Use authenticated review controls outside the whitelist file before relying on whitelist approvals for sensitive workflows.

Risk: Dependency drift or unsafe local environments can affect scanner behavior.

Mitigation: Run the skill in an isolated environment with a pinned PyYAML version.

Risk: The hook stdout leak noted by security evidence may expose unintended output during prompt handling.

Mitigation: Fix and retest hook output behavior before installing it as an active Claude Code hook.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stlas/skills/prompt-shield)
- [SCORING.md](artifact/SCORING.md)

## Skill Output:

**Output Type(s):** [text, json, markdown, shell commands, configuration, guidance]

**Output Format:** [Text and JSON scan results with Markdown usage guidance and shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan output classifies input as CLEAN, WARNING, or BLOCK with a bounded score from 0 to 100.]

## Skill Version(s):

3.0.6 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
