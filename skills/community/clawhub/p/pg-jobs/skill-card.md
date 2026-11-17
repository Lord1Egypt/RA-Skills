## Description:

Use when interacting with the ProxyGate job marketplace and bounty board to list jobs, create bounties, claim work, submit results, or manage job lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwelten](https://clawhub.ai/user/jwelten)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to work with ProxyGate marketplace jobs, including browsing listings, creating escrow-backed bounties, claiming tasks, submitting work, and reviewing submissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through real ProxyGate escrow and marketplace actions.

Mitigation: Require confirmation of the active account, job or listing ID, USDC amount, and exact action before creating, claiming, accepting, rejecting, canceling, depositing, withdrawing, proxying requests, or exposing services.

Risk: Casual job-search requests could unintentionally trigger marketplace workflows.

Mitigation: Use this skill only when the user intentionally asks for ProxyGate marketplace help.

## Reference(s):

- [ProxyGate CLI Command Reference](references/commands.md)
- [ProxyGate gateway docs](https://gateway.proxygate.ai/docs)
- [ClawHub skill page](https://clawhub.ai/jwelten/skills/pg-jobs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ProxyGate CLI commands, SDK examples, account or job identifiers, USDC amounts, and marketplace lifecycle guidance.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
