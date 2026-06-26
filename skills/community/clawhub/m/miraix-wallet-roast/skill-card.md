## Description: <br>
Use this skill when the user wants to analyze or roast a Solana wallet, score memecoin exposure, explain portfolio risks, generate rebalance ideas, draft a share post, or return a branded Miraix share card URL powered by OKX OnchainOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to analyze Solana wallet addresses, get a sharp portfolio risk summary, review rebalance ideas, and generate share-ready wallet roast text or card links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided Solana wallet addresses to Miraix public APIs for analysis and share-card generation. <br>
Mitigation: Use only wallet addresses the user intentionally provides, and do not send seed phrases, private keys, exchange credentials, or unrelated personal data. <br>
Risk: Returned rebalance ideas or swap command text may affect financial decisions if followed without review. <br>
Mitigation: Present actions as suggestions for review, preserve API-returned command text when useful, and avoid treating the output as automatically safe to execute. <br>


## Reference(s): <br>
- [Miraix wallet audit API](https://app.miraix.fun/api/wallet-audit) <br>
- [Miraix wallet roast share image API](https://app.miraix.fun/api/wallet-roast/share-image) <br>
- [ClawHub skill page](https://clawhub.ai/richard7463/miraix-wallet-roast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with wallet analysis, risk list, action list, and share image URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should be based on Miraix API output and preserve returned action commands when the user may execute them later.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
