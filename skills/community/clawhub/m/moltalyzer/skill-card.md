## Description: <br>
Moltalyzer gives agents real-time intelligence feeds for Polymarket markets, Moltbook community sentiment, GitHub trends, Pulse narratives, token signals, and cross-source intelligence digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcislo](https://clawhub.ai/user/jcislo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Moltalyzer to connect agents to market, community, repository, narrative, and token intelligence feeds without building those polling and response-format integrations themselves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may send sensitive prompts or feedback to Moltalyzer's external API endpoints. <br>
Mitigation: Do not send secrets, private business plans, personal data, credentials, wallet details, or payment details in advisor prompts or feedback submissions. <br>
Risk: Some endpoints are paid x402 routes and can incur per-call charges. <br>
Mitigation: Default agents to free index, brief, sample, and preview routes, and require explicit approval before using paid endpoints. <br>
Risk: Token Signals is disclosed as temporarily offline, so token endpoints may return offline status or 503 responses. <br>
Mitigation: Check token index status before relying on token outputs and handle 503 responses without retry loops that assume immediate availability. <br>


## Reference(s): <br>
- [Moltalyzer ClawHub listing](https://clawhub.ai/jcislo/moltalyzer) <br>
- [Moltalyzer website](https://moltalyzer.xyz) <br>
- [Moltalyzer API docs](https://api.moltalyzer.xyz/docs) <br>
- [Moltalyzer OpenAPI spec](https://api.moltalyzer.xyz/openapi.json) <br>
- [Moltalyzer API changelog](https://api.moltalyzer.xyz/api/changelog) <br>
- [Moltalyzer API Reference](references/api-reference.md) <br>
- [Moltalyzer Code Examples](references/code-examples.md) <br>
- [Moltalyzer Response Formats](references/response-formats.md) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with endpoint tables, TypeScript examples, shell install commands, and JSON response schemas.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node for the documented examples; free routes have rate limits, and paid routes use x402.] <br>

## Skill Version(s): <br>
2.4.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
