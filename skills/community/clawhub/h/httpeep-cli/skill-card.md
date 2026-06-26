## Description: <br>
Use HTTPeep from the terminal with httpeep-cli for proxy lifecycle control, HTTP/HTTPS traffic capture, session inspection, rule injection, request replay, recording flows, certificate troubleshooting, CI scripting, and agent-driven network debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imchrischen](https://clawhub.ai/user/imchrischen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate HTTPeep from an agent-driven terminal workflow for local HTTP API debugging, traffic capture, session inspection, request replay, DNS overrides, rule management, and certificate troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through high-impact proxy capture and traffic manipulation workflows. <br>
Mitigation: Use it in local or test environments, review commands before execution, avoid production credentials, and scope capture to the requested app, domain, process, status, or time range. <br>
Risk: Captured traffic and recordings may contain credentials, cookies, API keys, or sensitive request and response bodies. <br>
Mitigation: Redact secrets from reports, inspect only the fields needed to support conclusions, and do not store recordings in source control. <br>
Risk: HTTPS interception requires installing and trusting an HTTPeep root CA certificate. <br>
Mitigation: Verify certificate status before use, use HTTPS interception only where appropriate, and uninstall the root CA when finished. <br>
Risk: The skill includes guidance for checking and updating the installed skill from HTTPeep/agent-skills. <br>
Mitigation: Do not allow automatic skill updates unless the HTTPeep/agent-skills source is trusted, and avoid interrupting active investigations with maintenance updates. <br>


## Reference(s): <br>
- [CLI Overview](references/overview.md) <br>
- [CLI Basics](references/basics.md) <br>
- [Proxy](references/proxy.md) <br>
- [Sessions](references/sessions.md) <br>
- [Rules](references/rules.md) <br>
- [Request](references/request.md) <br>
- [Replay](references/replay.md) <br>
- [Record](references/record.md) <br>
- [DNS](references/dns.md) <br>
- [Certificate](references/cert.md) <br>
- [License](references/license.md) <br>
- [Monitor](references/monitor.md) <br>
- [Shell](references/shell.md) <br>
- [Launch](references/launch.md) <br>
- [Import](references/import.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown with inline shell commands and structured JSON-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should redact credentials, cookies, tokens, API keys, and sensitive captured bodies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
