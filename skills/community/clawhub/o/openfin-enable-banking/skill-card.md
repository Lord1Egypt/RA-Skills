## Description: <br>
PSD2 Open Banking integration via Enable Banking API for onboarding DACH bank connections, fetching balances and transactions, and renewing sessions for tax advisory automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppronobis](https://clawhub.ai/user/ppronobis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and tax-advisory automation teams use this skill to connect client bank accounts through Enable Banking, manage mandant sessions, and retrieve structured balance and transaction data. <br>

### Deployment Geography for Use: <br>
Germany and Austria <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live bank authorization and stored financial records. <br>
Mitigation: Install only for intended Enable Banking account access and protect or periodically delete config.json, private keys, mandanten, pending_callbacks, and data outputs. <br>
Risk: Callback handling can expose authorization codes if deployed with weak transport or broad network access. <br>
Mitigation: Restrict the callback server to localhost or a trusted HTTPS reverse proxy, and avoid HTTP mode for real use. <br>
Risk: Authorization links may grant sensitive access if sent to the wrong recipient. <br>
Mitigation: Share authorization URLs only through channels where recipient control has been verified. <br>
Risk: Unpinned dependency ranges can change the runtime security profile. <br>
Mitigation: Pin reviewed dependency versions before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppronobis/openfin-enable-banking) <br>
- [Enable Banking API reference](https://enablebanking.com/docs/api/reference/) <br>
- [Bundled Enable Banking API quick reference](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON data outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch operations write structured account, balance, transaction, mandant, and callback files locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
