## Description: <br>
Agent-to-agent cloud service: deploys and runs your apps and services - domains, logs, real status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyxory](https://clawhub.ai/user/nyxory) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent to nyxory, deploy Git repositories or long-running services to live URLs, manage domains and secrets, inspect logs, and check deployment status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector can grant broad, persistent cloud deployment access across projects. <br>
Mitigation: Review OAuth or API-token permissions before installation and prefer least-privilege, non-production, or tightly scoped projects where possible. <br>
Risk: Build logs, runtime logs, and configured secrets may contain sensitive information. <br>
Mitigation: Treat logs and secrets as sensitive, restrict who can access the connector, and avoid exposing credentials through shared agent sessions. <br>
Risk: Persistent MCP access may continue to provide deployment authority after initial setup. <br>
Mitigation: Install only when persistent deployment access is acceptable, periodically review access, and revoke credentials when the connector is no longer needed. <br>


## Reference(s): <br>
- [nyxory homepage](https://nyxory.com) <br>
- [ClawHub skill listing](https://clawhub.ai/nyxory/nyxory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide OAuth or API-token based MCP setup, cloud deployment operations, domain configuration, secret management, log review, and status checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
