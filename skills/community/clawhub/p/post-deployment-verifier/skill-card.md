## Description: <br>
Verify deployments are healthy after release by checking endpoints, comparing response schemas, validating metrics, running smoke tests, verifying database migrations, and producing a deployment confidence report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill after deployment to check service health, response shape, version alignment, logs, migrations, and resource usage before accepting a release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect broad Docker and systemd logs or probe endpoints discovered from environment values. <br>
Mitigation: Run it only where the agent is authorized to inspect local service logs and configured endpoints, and prefer an explicit .deploy-verify.json with known targets. <br>
Risk: Logs and endpoint responses can contain secrets, customer data, or other sensitive operational details. <br>
Mitigation: Avoid broad log checks on shared hosts or sensitive environments; review output before sharing deployment reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/post-deployment-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable status text, JSON summaries, Markdown reports, and Slack-formatted text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose a .deploy-verify.json configuration and deployment confidence report.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
