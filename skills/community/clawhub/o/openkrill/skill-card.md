## Description:

Enable AI agents to make micropayments via x402 protocol. Use when purchasing browser sessions on Browserbase, scraping with Firecrawl, or any x402-compatible API. Handles wallet creation, funding, and automatic payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emilankerwiik](https://clawhub.ai/user/emilankerwiik)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to discover x402-compatible services, create or fund thirdweb-backed wallets, and make paid API requests for browser sessions, scraping, and other micropayment-enabled workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend funds through broad x402 payment calls.

Mitigation: Use a low-funded wallet, require explicit approval for each payment, and enforce spending caps outside the skill.

Risk: The skill can call arbitrary x402 URLs.

Mitigation: Restrict use to reviewed service endpoints and avoid arbitrary or untrusted x402 URLs.

Risk: The disposable-email workflow creates and reads inboxes while storing credentials locally.

Mitigation: Do not use disposable inboxes for sensitive accounts unless credential storage is fixed and reviewed.

## Reference(s):

- [OpenKrill ClawHub Skill Page](https://clawhub.ai/emilankerwiik/skills/openkrill)
- [x402 API Reference](references/API-REFERENCE.md)
- [x402-Compatible Services](references/SERVICES.md)
- [x402 Protocol](https://x402.org)
- [x402 Bazaar Discovery](https://docs.cdp.coinbase.com/x402/bazaar)
- [thirdweb x402 Documentation](https://portal.thirdweb.com/x402)
- [Browserbase x402 Docs](https://docs.browserbase.com/integrations/x402/introduction)
- [Firecrawl x402 Docs](https://docs.firecrawl.dev/x402/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, TypeScript command examples, JSON snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include paid API request commands, wallet funding instructions, service discovery results, and disposable email account details.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
