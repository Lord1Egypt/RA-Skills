## Description:

Hook Auditor scans active Claude Code hooks, distinguishes effective hooks from inactive cache files, estimates per-turn cost, and guides cleanup of unexpected hook behavior after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianyangzhai](https://clawhub.ai/user/jianyangzhai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to audit installed skill and plugin hooks, understand their token, latency, and behavior impact, and remove unwanted active hooks only after review and confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented dry-run procedure can execute hook scripts from unknown skills or plugins on the user's machine.

Mitigation: Inspect unknown hook source statically first, or run dry-run tests only in an isolated sandbox without home-directory, credential, or network access.

Risk: Scan reports can expose local Claude Code skill and plugin configuration details.

Mitigation: Review scan output before sharing it and redact local paths, plugin IDs, or configuration details that should remain private.

Risk: Hook cleanup changes user-level Claude Code configuration and may affect workflows that rely on those hooks.

Mitigation: Require explicit user confirmation, create backups before edits, preserve skill and script files, and verify the scan result after cleanup.

## Reference(s):

- [Hook event semantics quick reference](artifact/references/hook-events.md)
- [ClawHub skill page](https://clawhub.ai/jianyangzhai/skills/hook-auditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with inline shell commands and optional JSON scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports active and inactive hook sources, per-turn cost signals, cleanup recommendations, and verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
