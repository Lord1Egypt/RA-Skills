## Description: <br>
Manage PagerDuty incidents, on-call schedules, services, and maintenance windows directly from your agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdbotworker](https://clawhub.ai/user/clawdbotworker) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect PagerDuty services, incidents, schedules, on-call assignments, and maintenance windows from an agent workflow. With appropriate credentials, it can also create, acknowledge, resolve, and annotate incidents or create maintenance windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change PagerDuty account data, including incidents and maintenance windows. <br>
Mitigation: Use a least-privileged PagerDuty API key and require explicit confirmation before write operations. <br>
Risk: The PAGERDUTY_BASE_URL setting can direct the PagerDuty API token to a configured HTTP or HTTPS endpoint. <br>
Mitigation: Keep PAGERDUTY_BASE_URL unset unless the endpoint is fully trusted, and avoid any http:// endpoint. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clawdbotworker/pagerduty-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/clawdbotworker) <br>
- [PagerDuty API Base Endpoint](https://api.pagerduty.com) <br>


## Skill Output: <br>
**Output Type(s):** [json, text, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON on stdout; setup and invocation guidance may include shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and PAGERDUTY_API_KEY; PAGERDUTY_FROM_EMAIL is required for write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, CHANGELOG released 2026-03-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
