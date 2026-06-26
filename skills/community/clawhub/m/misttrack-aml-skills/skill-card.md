## Description: <br>
MistTrack Skills supports cryptocurrency address risk analysis, AML compliance checks, and on-chain transaction tracing through the MistTrack OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misttrack](https://clawhub.ai/user/misttrack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, compliance analysts, and agent operators use this skill to check wallet and transaction risk, investigate addresses, inspect multisig behavior, and run pre-transfer AML safety checks before crypto transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bundles wallet-key handling and crypto payment signing through its x402 payment module. <br>
Mitigation: Prefer MISTTRACK_API_KEY for normal read-only AML checks; avoid x402 unless needed, never use a production wallet key, avoid --auto and auto_pay=True, and use a dedicated low-balance wallet for pay-per-use access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/misttrack/misttrack-aml-skills) <br>
- [MistTrack](https://misttrack.io/) <br>
- [MistTrack Documentation](https://docs.misttrack.io/) <br>
- [MistTrack OpenAPI Overview](https://docs.misttrack.io/openapi/overview) <br>
- [x402 Documentation](https://docs.cdp.coinbase.com/x402/welcome) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and JSON-capable script output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pre-transfer checks use allow, warn, block, and error exit codes; payment features require explicit key-file handling when used.] <br>

## Skill Version(s): <br>
0.2.12 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
