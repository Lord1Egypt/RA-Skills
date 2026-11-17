## Description:

Financial data SDK for AI Agents. 218+ read-only endpoints for market data, prices, fundamentals. Built for Cursor, Claude, OpenClaw. Data retrieval only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strykragent](https://clawhub.ai/user/strykragent)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this SDK to connect AI agents and trading workflows to PRISM financial market data, analytics, risk, prediction market, and agent-context endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is advertised as read-only, while authoritative security evidence says it includes account key management and transaction-related capabilities.

Mitigation: Review and restrict any non-read-only modules before installation or agent use; require human approval for developer key-management and execution workflows.

Risk: The skill requires a PRISM API key and supports a custom baseUrl.

Mitigation: Use least-privilege or non-production credentials, keep secrets in environment variables, and avoid custom endpoints unless they have been reviewed.

Risk: Execution, webhook, and watch behavior can create higher-risk remote account activity.

Mitigation: Treat these features as active operations rather than passive market-data lookup; gate them behind policy controls, logging, and explicit operator approval.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/strykragent/skills/prism-finance-os)
- [PRISM API Documentation](https://api.prismapi.ai/docs)
- [PRISM API Home](https://api.prismapi.ai)
- [npm Package](https://www.npmjs.com/package/prism-finance-os)
- [GitHub Repository](https://github.com/Strykr-Prism/PRISM-OS-SDK)
- [Architecture](docs/ARCHITECTURE.md)
- [Real API Coverage](docs/REAL_API_COVERAGE.md)
- [Universal SDK](docs/UNIVERSAL_SDK.md)

## Skill Output:

**Output Type(s):** [API Calls, Code, Configuration instructions, JSON]

**Output Format:** [TypeScript SDK calls and structured JSON-like API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PRISM_API_KEY; supports configurable baseUrl and timeout.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence, released 2026-02-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
