## Description: <br>
AI agents borrow USDC based on their Moltbook karma score. Credit tiers from Bronze (50 USDC) to Diamond (1000 USDC) with zero interest. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[abdhilabs](https://clawhub.ai/user/abdhilabs) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and hackathon builders use KarmaBank to scaffold and test an AI-agent credit workflow that checks Moltbook reputation, assigns USDC borrowing tiers, and records borrow or repay activity with a demo ledger. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is finance-oriented and can involve USDC borrow or repay flows. <br>
Mitigation: Review the full source, transaction limits, and ledger behavior before installation or use. <br>
Risk: The skill asks for Circle wallet credentials and references local wallet code that is not fully reviewed in the evidence. <br>
Mitigation: Use sandbox or testnet credentials only, and do not provide production Circle credentials until the wallet integration is audited. <br>
Risk: Borrow and repay commands may support confirmation-bypass behavior. <br>
Mitigation: Avoid confirmation-bypass flags for borrow or repay actions unless the transaction path has been reviewed and tested. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abdhilabs/karmabank-minimal) <br>
- [Project GitHub Resource](https://github.com/abdhilabs/karmabank) <br>
- [Moltbook](https://moltbook.com) <br>
- [Moltbook API Base](https://www.moltbook.com/api/v1) <br>
- [Circle Console](https://console.circle.com) <br>
- [USDC Agentic Hackathon](https://moltbook.com/m/usdc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI usage, environment variable guidance, credit-tier details, and loan workflow descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
