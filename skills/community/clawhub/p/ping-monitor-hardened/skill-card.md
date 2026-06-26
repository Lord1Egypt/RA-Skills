## Description: <br>
ICMP health check for hosts, phones, and daemons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check whether explicitly named hosts are reachable with local ICMP ping while keeping results local and requiring confirmation for internal or metadata addresses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may ping targets they are not authorized to test. <br>
Mitigation: Use the skill only for hosts the user is allowed to test, and preserve confirmation before internal, loopback, or metadata-address pings. <br>
Risk: Ping output can reveal network intelligence such as hostnames, IP addresses, reachability, response times, or packet loss. <br>
Mitigation: Display ping results only to the local user and do not send ping-derived data to external APIs, webhooks, messages, or other network-transmitting commands. <br>
Risk: Untrusted documents, logs, or configuration files may contain hostnames that could trigger unintended reachability checks. <br>
Mitigation: Initiate pings only from a direct user request naming the target, not from discovered hostnames or embedded instructions. <br>
Risk: A different executable named ping-monitor could appear earlier in PATH. <br>
Mitigation: Verify that the ping-monitor executable in PATH is the intended one before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/ping-monitor-hardened) <br>
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/ping-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Displays ping results locally; does not send ping-derived network information to external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
