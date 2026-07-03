## Description: <br>
Mr. Market helps agents separate emotionally driven market quotes from intrinsic value when advising on investing, fundraising, acquisition, or valuation decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, founders, acquirers, and advisors use this skill to structure decisions where quoted prices or implied valuations are pressuring judgment. It guides the agent to compare market mood against independent intrinsic value, choose whether to transact, ignore, or wait, and document an emotional-contagion check. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may influence investment, fundraising, acquisition, or valuation decisions. <br>
Mitigation: Use it as a structured reasoning aid; independently verify assumptions and obtain qualified review before real financial transactions. <br>
Risk: A market quote may be misclassified as emotional mood when it reflects genuine new business information or a forced-liquidity constraint. <br>
Mitigation: Apply the skill only after checking whether new economic information, forced sale needs, liquidity requirements, or lack of intrinsic-value anchor make the framework inappropriate. <br>


## Reference(s): <br>
- [Sources - mr-market](references/sources.md) <br>
- [Method in Action: Graham 1949, Buffett 1987 + 2008](examples/graham-1949-buffett-1987-2008.md) <br>
- [Buffett 1987 Berkshire Hathaway Letter](https://www.berkshirehathaway.com/letters/1987.html) <br>
- [Buffett 2008 New York Times Op-Ed](https://www.nytimes.com/2008/10/17/opinion/17buffett.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown decision template with structured fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a decision record covering quote, business reality, intrinsic value estimate, market state, response, contagion check, and re-evaluation trigger.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
