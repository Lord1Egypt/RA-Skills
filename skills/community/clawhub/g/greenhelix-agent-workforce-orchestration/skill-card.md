## Description:

Agent Workforce Orchestration: Hybrid Human+AI Teams. Build agent-led workforce orchestration: capability matching, escrow-based payments for AI agents and human gig workers, unified reputation scoring, SLA enforcement, dispute resolution, and compliance reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this guide to design an agent-led workforce orchestrator for assigning tasks, managing escrow payments, scoring performance, enforcing SLAs, resolving disputes, and producing compliance records across hybrid human and AI teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide teaches credentialed automated workforce payment workflows, including escrow release and dispute settlement patterns.

Mitigation: Use least-privilege GreenHelix credentials, confirm the endpoint is sandbox or explicitly intended, and require review of payment release and dispute settlement controls before using the examples with real funds.

Risk: The security evidence flags weak scoping and safety guidance around budget limits, worker consent, privacy controls, tax obligations, and compliance obligations.

Mitigation: Redesign and review budget caps, consent handling, privacy controls, tax reporting, and compliance processes before adapting the guide for production operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-workforce-orchestration)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with Python code examples, architecture notes, operational checklists, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GREENHELIX_API_KEY for credentialed examples; artifact declares no installation and is not directly executable.]

## Skill Version(s):

1.3.1 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
