## Description: <br>
NAS Dashboard generates an alert-first text health report for Linux NAS and HomeLab systems covering system load, ZFS, disks, Docker, Frigate, GPU, UPS, backups, updates, and security signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wudi488](https://clawhub.ai/user/wudi488) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Self-hosted NAS, HomeLab, and home-server operators use this skill to collect host telemetry and receive compact daily health reports with severity levels, root-cause notes, and suggested fix commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dashboard output can expose operational details such as hostnames, IP addresses, open ports, service names, Docker details, disk health, and login counts. <br>
Mitigation: Review the generated report before forwarding it to Telegram or other shared channels, and treat the output as operationally sensitive. <br>
Risk: Privileged checks can read sensitive host health and security data when passwordless sudo is enabled. <br>
Mitigation: Configure passwordless sudo narrowly for the checks you intend to run, and allow unavailable sections to degrade instead of granting broad privileges. <br>
Risk: Automatic cron delivery or broad trigger phrases can create recurring collection and sharing of NAS telemetry. <br>
Mitigation: Use specific triggers and scheduled delivery only when recurring collection and transmission are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wudi488/nas-dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text dashboard report suitable for Markdown or Telegram delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime output may include hostnames, IP addresses, service names, open ports, disk health, Docker details, and failed-login counts.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
