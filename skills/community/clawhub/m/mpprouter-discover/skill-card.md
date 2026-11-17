## Description:

Discover paid API services available via MPP Router (apiserver.mpprouter.dev) that accept Stellar USDC payments, match a service to the user's intent, and hand off to the pay-per-call skill for invocation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnmuggle](https://clawhub.ai/user/shawnmuggle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover live MPP Router services, choose an appropriate paid API for a user task, and route invocation through a Stellar USDC payment handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent toward paid Stellar mainnet API calls.

Mitigation: Rely on the pay-per-call confirmation gate before any mainnet spend and review prompts carefully when a task could be handled without paid routing.

Risk: Session-only MPP Router services can charge successfully but fail upstream when used through charge mode.

Mitigation: Refuse session-only services by default unless the user explicitly accepts the warned risk of losing the fee without a result.

Risk: Unverified or changing catalog entries may have stale pricing, availability, or payment behavior.

Mitigation: Fetch the service catalog fresh, avoid caching it for more than a minute, and warn before proceeding with unverified services.

Risk: The router forwards request bodies as-is, so malformed requests can waste paid calls or return incorrect results.

Mitigation: Read the matched service documentation from the catalog before building a request body and ask the user when the API format is unclear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shawnmuggle/skills/mpprouter-discover)
- [MPP Router](https://www.mpprouter.dev)
- [MPP Router Service Catalog](https://apiserver.mpprouter.dev/v1/services/catalog)
- [MPP Router Verified Runs](https://github.com/mpprouter/rozo-mpprouter/blob/main/docs/verified-runs.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live service-selection guidance and payment-handoff instructions; the skill does not itself produce persistent output files.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
