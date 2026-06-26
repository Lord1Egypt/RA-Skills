## Description: <br>
Generate operational runbooks from project files by scanning Dockerfiles, docker-compose.yml, systemd units, Makefiles, package.json, and configuration files for start, stop, restart, deploy, rollback, and troubleshooting procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations teams use this skill to draft service runbooks from existing project infrastructure files. It helps turn detected build, deployment, lifecycle, health check, rollback, troubleshooting, monitoring, and contact details into reviewable operational documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated runbooks can include project paths, service names, ports, commands, environment variable names, and some raw configuration values. <br>
Mitigation: Run the generator on reviewed project directories, avoid production folders containing real secrets when possible, and inspect Markdown or JSON output before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/ops-runbook-generator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown by default, with optional structured JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the generated runbook to a specified file with the -o flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
