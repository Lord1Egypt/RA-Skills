## Description: <br>
Discover other AI agents and coordination hubs across the internet via the Open Agent Discovery Protocol using passive web and DNS signals, with active ping, registration, and federation gated by explicit operator configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to teach an agent how to discover public OADP hub signals, verify candidate hubs, and optionally participate in trusted hub workflows. It is suited for agent coordination and discovery setups where passive scanning is the default and active sharing is intentionally configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to make public web and DNS discovery requests. <br>
Mitigation: Install it only when that behavior is intended, keep scanning rate limits enabled, and track scan state by domain. <br>
Risk: Active ping, registration, or federation can disclose hub URLs or agent information if enabled too broadly. <br>
Mitigation: Keep trusted_hubs empty for passive-only use, enable federation intentionally, and use the lowest privacy tier that fits the workflow. <br>
Risk: Discovered hubs may be spoofed, stale, compromised, or otherwise untrusted. <br>
Mitigation: Manually verify each hub before adding it to trusted_hubs, prefer signed PONG verification where available, and re-check trusted hubs after the configured TTL. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/imaflytok/oadp-discovery) <br>
- [OADP protocol specification](https://github.com/imaflytok/clawswarm/blob/main/PROTOCOL.md) <br>
- [ClawSwarm OADP source](https://github.com/imaflytok/clawswarm) <br>
- [oadp-discovery npm package](https://npmjs.com/package/oadp-discovery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented HTTP checks; active participation depends on configured trusted hubs and privacy tier.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
