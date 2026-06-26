## Description: <br>
Token screener with a smart money filter cross-referenced against netflow to identify tokens showing early accumulation signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Nansen CLI token research commands, compare smart money screener results with Smart Trader netflow, and identify candidate tokens for further analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external Nansen CLI package with a Nansen API key and may consume account quota. <br>
Mitigation: Use a revocable or dedicated NANSEN_API_KEY and confirm expected CLI behavior before broad deployment. <br>
Risk: Token accumulation output can be mistaken for investment advice. <br>
Mitigation: Treat results as research signals only and review them with independent market, liquidity, and risk checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-smart-money-alpha) <br>
- [nansen-cli npm package](https://www.npmjs.com/package/nansen-cli) <br>
- [nansen-cli GitHub repository](https://github.com/nansen-ai/nansen-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, text] <br>
**Output Format:** [Markdown with inline bash code blocks and command-result guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nansen binary and NANSEN_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
