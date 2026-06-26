## Description: <br>
Gives an agent access to the NeuBird CLI for production operations investigations across infrastructure health, cloud cost, incidents, latency, error rates, deployment risk, silent failures, and blast radius analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neubird](https://clawhub.ai/user/neubird) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
SREs, platform engineers, and operations teams use this skill to run NeuBird-powered production investigations and summarize findings with scope, evidence, and recommended next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The NeuBird CLI can access production project data according to the local account's permissions. <br>
Mitigation: Use least-privilege NeuBird project access and install the skill only when the publisher and account access are trusted. <br>
Risk: Investigation prompts or outputs may include secrets or unnecessary customer data. <br>
Mitigation: Avoid sending secrets or unnecessary customer data in prompts and review findings before sharing them. <br>
Risk: Temporary NeuBird session files may remain under /tmp after investigations. <br>
Mitigation: Run the documented cleanup command and remove session files when the investigation is complete. <br>
Risk: Running against the wrong production project could produce misleading findings or expose unrelated operational data. <br>
Mitigation: Confirm the target project before starting an investigation, especially when the user's request is ambiguous. <br>


## Reference(s): <br>
- [NeuBird homepage](https://neubird.ai) <br>
- [NeuBird product site](https://neubird.com) <br>
- [ClawHub skill page](https://clawhub.ai/neubird/production-operations-agent) <br>
- [Application & APM Investigation Reference](references/application.md) <br>
- [Cloud Infrastructure Investigation Reference](references/cloud.md) <br>
- [Database & Storage Investigation Reference](references/database.md) <br>
- [Escalation & Incident Communications Reference](references/escalation.md) <br>
- [Kubernetes Investigation Reference](references/kubernetes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized investigation findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [NeuBird CLI runs may stream for 60-180 seconds and use temporary session files under /tmp.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
