## Description:

Pg Game Monitor provides Prometheus, Pushgateway, Grafana, Alertmanager, and Feishu/Lark webhook monitoring for multiple Java game server JVMs and self-hosted MySQL on physical servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freepengyang](https://clawhub.ai/user/freepengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to deploy and operate monitoring for Java game server JVM memory, GC, threads, class memory, and MySQL health, with Grafana dashboards and Feishu/Lark alert delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer behavior creates persistent monitoring services with insecure defaults and exposed monitoring or webhook ports.

Mitigation: Set unique Grafana credentials before startup, restrict service ports with firewall rules, authentication, and TLS, and run services under dedicated least-privilege users.

Risk: Downloaded components and Python dependencies may be installed without checksum, signature, or hash verification.

Mitigation: Pin dependencies with hashes and verify component checksums or signatures before installing.

Risk: Webhook and database secrets can be stored in environment files on monitored hosts.

Mitigation: Store secrets with strict file permissions or a secret manager, and use Ansible Vault or equivalent controls for database credentials.

## Reference(s):

- [Pg Game Monitor on ClawHub](https://clawhub.ai/freepengyang/skills/pg-game-monitor)
- [Deployment Guide](artifact/references/deploy.md)
- [Prometheus Alert Rules](artifact/references/rules.md)
- [Grafana Configuration Guide](artifact/references/grafana.md)
- [Monitoring Architecture Planning](artifact/references/planning.md)
- [FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and references to Python, YAML, shell, and Grafana dashboard JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment commands, environment variables, Prometheus alert rules, Grafana dashboard references, and troubleshooting guidance.]

## Skill Version(s):

1.3.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
