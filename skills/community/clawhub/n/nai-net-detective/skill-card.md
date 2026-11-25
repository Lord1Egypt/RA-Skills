## Description:

Run structured network diagnostics and produce a plain-English diagnosis explaining what's wrong and why.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support staff, and technically capable users use this skill to investigate slow or unreliable network connections and turn DNS, ping, traceroute, MTU, speed, and baseline data into a concise diagnosis with next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full diagnostics contact outside services and can reveal local network metadata such as hostname, local IP, gateway, traceroute hops, DNS timing, latency, and optional speed-test results.

Mitigation: Confirm that active network diagnostics are appropriate before use on enterprise, VPN, or sensitive networks; use --no-traceroute, --no-mtu, or omit --speed when less external traffic is desired.

Risk: Recording history stores diagnostic metrics locally for baseline comparison.

Mitigation: Avoid --record for sensitive environments or review and clear the local history file when baseline retention is not desired.

Risk: Speed tests download fixed-size payloads from Cloudflare and may consume bandwidth or affect metered connections.

Mitigation: Run diagnostics without --speed unless throughput testing is needed, or use quick speed checks where appropriate.

## Reference(s):

- [Net Detective Diagnostic Guide](references/diagnostic-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/nai-net-detective)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with JSON diagnostic data and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local network metadata, traceroute hops, DNS timing, latency, optional speed-test results, and historical baseline comparisons.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
