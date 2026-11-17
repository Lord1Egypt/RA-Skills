## Description:

NeuBird AI Production Ops Agent helps agents use the authenticated neubird CLI to investigate production health, incidents, cloud cost, performance, deployment risk, silent failures, and blast radius.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neubird](https://clawhub.ai/user/neubird)

### License/Terms of Use:

MIT-0

## Use Case:

SREs, platform engineers, and incident responders use this skill to run NeuBird production-ops investigations and turn CLI findings into concise incident guidance, recommended next steps, and escalation artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated production CLI that can access sensitive operational data.

Mitigation: Use it only where NeuBird is authorized for the relevant environments, and avoid including secrets or customer data in prompts.

Risk: Sensitive investigations may affect production operations or expose operational context.

Mitigation: Confirm sensitive investigations with the user and summarize the scope before recommending action.

Risk: Free-form prompts can become unsafe if converted into shell command strings.

Mitigation: Invoke the CLI with separate arguments rather than constructing shell command strings from user input.

## Reference(s):

- [NeuBird AI Production Ops Agent on ClawHub](https://clawhub.ai/neubird/skills/production-operations-agent)
- [NeuBird Homepage](https://neubird.ai)
- [Application & APM Investigation Reference](references/application.md)
- [Cloud Infrastructure Investigation Reference](references/cloud.md)
- [Database & Storage Investigation Reference](references/database.md)
- [Escalation & Incident Communications Reference](references/escalation.md)
- [Kubernetes Investigation Reference](references/kubernetes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with inline shell commands and incident-response templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes CLI findings from stdout, ignores progress output on stderr, and recommends cleanup of session files after use.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
