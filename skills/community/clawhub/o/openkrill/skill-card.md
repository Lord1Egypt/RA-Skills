## Description: <br>
Enable AI agents to make micropayments via x402 protocol. Use when purchasing browser sessions on Browserbase, scraping with Firecrawl, or any x402-compatible API. Handles wallet creation, funding, and automatic payment flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emilankerwiik](https://clawhub.ai/user/emilankerwiik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use OpenKrill to discover x402-compatible services, manage thirdweb wallets, fund paid requests, and call APIs that require x402 micropayments. It also includes disposable email automation for signup and verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may initiate paid x402 API requests using broad thirdweb authority. <br>
Mitigation: Use a dedicated low-balance thirdweb project and wallet, set a small per-request cap manually, and review each paid URL before execution. <br>
Risk: Disposable email automation can create and store inbox credentials and expose verification links. <br>
Mitigation: Do not use it for important accounts or sensitive verification links, and delete or protect .agent-emails.json after use. <br>
Risk: The required THIRDWEB_SECRET_KEY can expose funds or payment capability if reused broadly. <br>
Mitigation: Use a narrowly scoped key dedicated to this workflow and avoid connecting it to wallets or projects with unrelated funds. <br>


## Reference(s): <br>
- [OpenKrill ClawHub Release](https://clawhub.ai/emilankerwiik/openkrill) <br>
- [x402 API Reference](references/API-REFERENCE.md) <br>
- [x402-Compatible Services](references/SERVICES.md) <br>
- [x402 Protocol](https://x402.org) <br>
- [x402 Bazaar Discovery](https://docs.cdp.coinbase.com/x402/bazaar) <br>
- [thirdweb x402 Documentation](https://portal.thirdweb.com/x402) <br>
- [Browserbase x402 Documentation](https://docs.browserbase.com/integrations/x402/introduction) <br>
- [Firecrawl x402 Documentation](https://docs.firecrawl.dev/x402/search) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command outputs may include wallet addresses, payment links, service catalog JSON, API responses, and disposable email credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter declares 1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
