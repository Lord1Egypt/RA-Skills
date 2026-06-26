## Description: <br>
Musashi provides conviction-weighted crypto token analysis through seven elimination gates, cross-domain pattern detection, adversarial debate, and optional on-chain STRIKE publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yeheskieltame](https://clawhub.ai/user/yeheskieltame) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, crypto analysts, and agent operators use Musashi to confirm token identity, run gate-based due diligence, compare social, on-chain, safety, and market signals, and produce a PASS/FAIL conviction report before optionally publishing a STRIKE on-chain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuring OG_CHAIN_PRIVATE_KEY enables wallet-signing operations and can spend gas or create durable public records. <br>
Mitigation: Use analysis mode without a private key when possible; if publishing is needed, use a dedicated low-funds wallet and require explicit user confirmation before signing. <br>
Risk: The bundled binary exposes additional wallet-signing admin commands beyond the normal analysis flow. <br>
Mitigation: Review the installed binary commands before use and only provide wallet credentials if those admin capabilities are acceptable in the deployment environment. <br>
Risk: Token intelligence can be wrong or stale and may influence financial decisions. <br>
Mitigation: Treat outputs as due-diligence support, verify token identity and chain selection with the user, and do not treat a PASS verdict as financial advice. <br>


## Reference(s): <br>
- [Musashi ClawHub page](https://clawhub.ai/yeheskieltame/musashi) <br>
- [Gate Reference](references/GATES.md) <br>
- [Pattern Detection Reference](references/PATTERNS.md) <br>
- [API Endpoints Reference](references/API_ENDPOINTS.md) <br>
- [0G Storage CLI install docs](https://docs.0g.ai/developer-hub/building-on-0g/storage/storage-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PASS/FAIL gate reports, STRIKE transaction hashes, 0G Storage root hashes, and setup guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
