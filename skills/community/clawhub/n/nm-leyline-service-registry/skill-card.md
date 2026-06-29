## Description: <br>
Registers external services with health checks, central config, and unified execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate multiple external service CLIs behind a registry pattern with shared configuration, health checks, execution results, retries, and failover. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured service commands can invoke external CLIs that may transmit prompts, files, or outputs to third-party providers. <br>
Mitigation: Review configured commands before use and avoid sending secrets, private files, or sensitive prompts unless the provider and its data-handling policies are trusted. <br>
Risk: Service integrations commonly require API keys or tokens. <br>
Mitigation: Keep credentials in environment variables or managed secret storage and avoid embedding keys in skill files, prompts, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-leyline-service-registry) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Service configuration patterns](artifact/modules/service-config.md) <br>
- [Execution patterns](artifact/modules/execution-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no bundled executable files.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
