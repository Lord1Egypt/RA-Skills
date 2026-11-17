## Description:

Gitbeacon gives agents GitHub trend intelligence from daily scans of trending new repositories, including structured digests, category and language trends, notable projects, and enriched repository rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcislo](https://clawhub.ai/user/jcislo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to discover current GitHub repository trends, inspect daily digests, and call free or paid gitBeacon API endpoints when trend data is useful for analysis or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid endpoints can spend USDC through x402 payment on Base Mainnet.

Mitigation: Use free endpoints to inspect response shapes first, and provide a low-balance payment wallet or private key only when intentional spending is acceptable.

Risk: Digest analysis is model-generated and may be imperfect or stale.

Mitigation: Check the scanDate or digestDate provenance returned by the API and review important conclusions before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcislo/skills/gitbeacon)
- [gitBeacon homepage](https://gitbeacon.dev)
- [gitBeacon API](https://api.gitbeacon.dev)
- [Latest digest endpoint](https://api.gitbeacon.dev/v1/digests/latest)
- [OpenAPI specification](https://api.gitbeacon.dev/openapi.json)
- [Discovery JSON](https://api.gitbeacon.dev/discovery)
- [x402 payment manifest](https://api.gitbeacon.dev/.well-known/x402)
- [A2A agent card](https://api.gitbeacon.dev/.well-known/agent-card.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with endpoint tables, curl commands, TypeScript examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free endpoints need no account, API key, or payment; paid endpoints require x402 payment on Base Mainnet.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
