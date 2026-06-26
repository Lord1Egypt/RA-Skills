## Description: <br>
Registers external services with health checks, central configuration, and unified execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to define a registry for coordinating multiple external service CLIs, including configuration, health checks, service selection, retries, failover, and execution result handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source files, or credentials may be sent to configured third-party providers during service execution. <br>
Mitigation: Confirm the configured services, environment variables, and provider data-handling terms before use, and avoid sending sensitive material to untrusted providers. <br>
Risk: Misconfigured service commands, authentication variables, or provider quotas can cause failed or unintended external executions. <br>
Mitigation: Review service configuration before deployment, run documented health checks, and use retry, timeout, circuit-breaker, and failover patterns where appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-leyline-service-registry) <br>
- [Leyline Plugin Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Service Configuration](artifact/modules/service-config.md) <br>
- [Execution Patterns](artifact/modules/execution-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes service registry patterns for external CLI configuration, health checks, retries, failover, and result handling.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
