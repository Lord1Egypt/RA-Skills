## Description: <br>
Manage mihomo (Clash Meta) proxy instances via REST API for status checks, proxy switching, delay tests, connection management, cache flushing, configuration reloads, restarts, and traffic or log monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonasgao](https://clawhub.ai/user/jonasgao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer mihomo or Clash Meta proxy instances through the REST API. It helps check status, switch proxy groups, test proxy delay, inspect or close connections, flush caches, reload configuration, restart the service, and monitor traffic or logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer a mihomo proxy instance, including switching nodes, closing connections, flushing caches, reloading configuration, upgrading, or restarting the service. <br>
Mitigation: Ask the user to confirm before performing disruptive proxy administration actions. <br>
Risk: The mihomo API secret can grant administrative access to the proxy instance. <br>
Mitigation: Keep the API secret private, pass it through the session environment only when needed, and avoid exposing it in shared logs or messages. <br>
Risk: Using an untrusted or exposed mihomo API host can allow unintended proxy control. <br>
Mitigation: Prefer localhost or a trusted host for MIHOMO_URL and verify the target instance before sending API requests. <br>


## Reference(s): <br>
- [Mihomo API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jonasgao/mihomo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-provided mihomo API host and secret; disruptive proxy administration actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
