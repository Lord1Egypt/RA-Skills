## Description: <br>
Is smart money exiting a token I hold? Net flow direction, seller breakdown by label, and recent SM trades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Nansen token-flow data and assess whether smart-money wallets, whales, exchanges, or other labeled cohorts appear to be selling a token they hold. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party nansen-cli package and requires a Nansen API key. <br>
Mitigation: Confirm trust in the nansen-cli package before installing, supply the API key only in trusted environments, and review any broader nansen command before approving it. <br>


## Reference(s): <br>
- [Nansen Exit Signals on ClawHub](https://clawhub.ai/nansen-devops/nansen-exit-signals) <br>
- [nansen-devops publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Analysis] <br>
**Output Format:** [Markdown with inline bash command examples and concise interpretation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY; commands are scoped to Nansen research queries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
