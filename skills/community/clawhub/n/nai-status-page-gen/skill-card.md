## Description: <br>
Generate a dark-themed static HTML status page summarizing health checks, ping, SSL certificates, and uptime for self-hosted services from a JSON config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and homelab administrators use this skill to configure service checks and generate a local or published status page for monitored self-hosted services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring unintended hosts can create unnecessary network traffic or expose internal service names. <br>
Mitigation: Review the service list before running checks and include only hosts the user intends to monitor. <br>
Risk: A published status page can reveal service names, URLs, status history, and certificate details. <br>
Mitigation: Publish the generated page only when those details are safe to share. <br>
Risk: Scheduled checks can continue running in the background after setup. <br>
Mitigation: Enable cron or LaunchAgent scheduling only when recurring checks are desired and document how to remove the schedule. <br>


## Reference(s): <br>
- [Setup Guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JSON check results, uptime history, and a self-contained static HTML status page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
