## Description: <br>
Provides global exchange-rate lookup and currency conversion from currency codes using Juhe's exchange-rate API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to answer exchange-rate questions, convert amounts between currencies, or list supported currencies. It is suited for reference-rate lookups and should not be treated as authoritative trading or settlement data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Juhe API key may be exposed if committed to files, passed on the command line, or handled in an unprotected environment. <br>
Mitigation: Store the key in a protected environment variable or secret manager, do not commit scripts/.env, and avoid passing the key on the command line. <br>
Risk: The provided script uses plain HTTP endpoints for exchange-rate requests. <br>
Mitigation: Use only on trusted networks unless the endpoint is changed to HTTPS and verified. <br>
Risk: Exchange-rate data is reference information and may not match bank settlement or trading rates. <br>
Mitigation: Present results as indicative reference rates and direct users to authoritative financial sources for transactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-exchange-rate) <br>
- [Juhe exchange-rate API documentation](https://www.juhe.cn/docs/api/id/80) <br>
- [Juhe API platform](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the JUHE_EXCHANGE_KEY environment variable or equivalent local key configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
