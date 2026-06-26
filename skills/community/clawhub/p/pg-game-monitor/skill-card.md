## Description: <br>
Provides Prometheus and Grafana monitoring assets for Java game server JVM metrics and self-managed MySQL, with Pushgateway data collection, Alertmanager alerts, Feishu/Lark webhook notifications, and Ansible deployment support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freepengyang](https://clawhub.ai/user/freepengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to deploy and maintain monitoring for single-host Java game servers and self-managed MySQL. It helps configure metrics collection, dashboards, alerting rules, and Feishu/Lark notification delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent monitoring and webhook services on target hosts. <br>
Mitigation: Review the installation scripts and confirm systemd services, ports, and long-running processes are approved before deployment. <br>
Risk: The skill handles MySQL credentials and Feishu/Lark webhook URLs. <br>
Mitigation: Store secrets in Ansible Vault or another secret manager, restrict environment file permissions, and avoid exposing those files in logs or shared terminal output. <br>
Risk: The skill pushes host and application metrics to Pushgateway and forwards alerts to webhook endpoints. <br>
Mitigation: Use trusted internal or HTTPS endpoints and confirm outbound monitoring data is allowed by the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freepengyang/pg-game-monitor) <br>
- [Deployment guide](references/deploy.md) <br>
- [Monitoring architecture planning](references/planning.md) <br>
- [Prometheus alert rule guide](references/rules.md) <br>
- [Grafana configuration guide](references/grafana.md) <br>
- [FAQ](references/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and bundled Python, shell, YAML, and JSON configuration artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scripts, Prometheus rules, Ansible playbook content, webhook code, and Grafana dashboard JSON files.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
