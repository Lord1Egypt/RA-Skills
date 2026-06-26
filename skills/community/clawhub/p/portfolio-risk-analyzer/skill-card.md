## Description: <br>
Analyzes crypto portfolios across multiple chains for risk exposures, stress tests, and optimization advice with automated $BANKR buyback monetization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kellyclaudeai](https://clawhub.ai/user/kellyclaudeai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and crypto operators use this skill to analyze wallet exposures, produce risk scores, run stress-test style checks, and generate portfolio optimization guidance. Operators may also configure payment-gated access, voice access, and automated $BANKR buybacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill can grant wallet-spending authority through payment-wallet credentials and buyback scripts. <br>
Mitigation: Do not provide a main wallet private key; use a segregated low-balance wallet, testnet or dry-run flow, explicit approvals, and spending limits. <br>
Risk: Automated buybacks can trigger crypto transactions without per-transaction approval. <br>
Mitigation: Disable or gate scheduled and manual buybacks until audited, and require explicit operator approval before transactions execute. <br>
Risk: Missing transaction helper scripts and configured dependencies may change the effective transaction behavior. <br>
Mitigation: Audit all helper scripts and installed dependencies before deployment, especially transaction construction, signing, and swap execution paths. <br>
Risk: Wallet and optional voice flows can expose financial and personal data. <br>
Mitigation: Provide clear privacy disclosures, limit retained logs, and restrict API and voice credentials to the minimum required access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kellyclaudeai/portfolio-risk-analyzer) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text with JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet risk scores, asset breakdowns, stress-test results, recommendations, payment-gating configuration, and buyback execution commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence, skill.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
