## Description:

The Agent Incident Response Playbook helps agent operators detect, contain, recover from, and learn from AI agent commerce incidents such as runaway spending, escrow exploitation, identity compromise, service degradation, and cascade failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and incident responders use this guide to build and adapt runbooks for AI agent commerce failures, including detection, containment, recovery, forensics, and post-mortem workflows. It is aimed at teams operating GreenHelix or OpenClaw-compatible agent systems that need practical response procedures and example code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can automatically freeze budgets and cancel escrows when run with production GreenHelix credentials.

Mitigation: Test in the GreenHelix sandbox first, use least-privilege keys scoped to specific agents and actions, and require approval gates before production containment actions.

Risk: Webhook-triggered response flows could be abused if request authenticity and replay protection are not implemented.

Mitigation: Add webhook signature verification and replay protection before enabling automated response from webhook events.

Risk: Auto-containment or fleet shutdown can interrupt legitimate agent activity and business processes.

Mitigation: Enable automated containment gradually, document rollback procedures, and keep human approval for fleet-wide shutdown until operational confidence is established.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-incident-response)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix developer documentation](https://api.greenhelix.net/docs)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guide with Python code examples, runbooks, checklist items, and inline command/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GREENHELIX_API_KEY for API-backed examples; the artifact itself is non-executable and does not install dependencies.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
