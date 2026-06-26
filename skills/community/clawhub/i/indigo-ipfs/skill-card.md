## Description: <br>
Store and retrieve data on IPFS and query collector UTXOs for the Indigo Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and protocol operators use this skill to store or retrieve plain-text IPFS content and inspect Indigo Protocol collector UTXOs for fee-distribution analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plain text stored on IPFS can be durable, public, and difficult to remove. <br>
Mitigation: Use the skill only for content intended for durable storage; redact or encrypt secrets, private keys, personal data, and sensitive business or financial records before storage. <br>
Risk: Collector UTXO queries and stored snapshots may expose wallet-linked financial information. <br>
Mitigation: Review outputs before sharing them and avoid publishing wallet-linked balances or position snapshots unless disclosure is intended. <br>


## Reference(s): <br>
- [Indigo IPFS on ClawHub](https://clawhub.ai/adacapo21/indigo-ipfs) <br>
- [Concepts](references/concepts.md) <br>
- [MCP Tools Reference](references/mcp-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown and plain text summaries with IPFS CIDs, retrieved content, or collector UTXO analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include durable IPFS content identifiers and wallet-linked financial data returned by tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
