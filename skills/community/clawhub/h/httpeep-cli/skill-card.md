## Description:

Use HTTPeep from the terminal with httpeep-cli for proxy lifecycle control, HTTP/HTTPS traffic capture, session inspection, rule injection, request replay, recording flows, certificate troubleshooting, CI scripting, and agent-driven network debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imchrischen](https://clawhub.ai/user/imchrischen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate HTTPeep from an agent terminal: start and inspect proxies, capture HTTP/HTTPS sessions, manage DNS and rules, replay requests, record flows, and troubleshoot certificates while redacting sensitive data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run unpinned remote npx skill update commands.

Mitigation: Disable or ignore automatic update instructions unless the updater and target version can be reviewed and pinned.

Risk: HTTP/HTTPS interception, system proxy changes, and root CA certificate commands can expose sensitive traffic or affect local network trust.

Mitigation: Use these commands only on machines and traffic the user is authorized to inspect, and verify proxy and certificate state before and after use.

Risk: Captured sessions, recordings, headers, cookies, and bodies may contain secrets.

Mitigation: Redact sensitive values in reports and avoid committing or sharing recording files or captured sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imchrischen/skills/httpeep-cli)
- [CLI overview](artifact/references/overview.md)
- [CLI basics](artifact/references/basics.md)
- [Proxy](artifact/references/proxy.md)
- [Sessions](artifact/references/sessions.md)
- [Rules](artifact/references/rules.md)
- [Request](artifact/references/request.md)
- [Replay](artifact/references/replay.md)
- [Record](artifact/references/record.md)
- [Certificate](artifact/references/cert.md)
- [DNS](artifact/references/dns.md)
- [Launch](artifact/references/launch.md)
- [Monitor](artifact/references/monitor.md)
- [Shell](artifact/references/shell.md)
- [License](artifact/references/license.md)
- [Import](artifact/references/import.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command traces, session or rule identifiers, statuses, timings, and entitlement disclosures; sensitive values should be redacted.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
