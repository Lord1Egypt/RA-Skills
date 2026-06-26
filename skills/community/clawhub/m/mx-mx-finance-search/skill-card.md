## Description: <br>
Natural language financial information search over EastMoney/Miaoxiang sources for news, announcements, research reports, policies, and market events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akiry09](https://clawhub.ai/user/akiry09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to query timely financial news, announcements, research, and policy updates for companies, sectors, themes, and macro events. It supports event tracking, market sentiment monitoring, announcement review, and investment research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and EM_API_KEY are sent to the EastMoney/Miaoxiang service. <br>
Mitigation: Use only trusted EastMoney/Miaoxiang credentials and keep the key revocable and rotatable. <br>
Risk: Returned content is written to disk by default. <br>
Mitigation: Use no-save behavior for sensitive searches and manage any generated text files according to local data handling policy. <br>
Risk: Financial search results may be time-sensitive or incomplete. <br>
Mitigation: Verify important facts against primary market, issuer, or regulator sources before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/akiry09/mx-mx-finance-search) <br>
- [EastMoney Miaoxiang service](https://ai.eastmoney.com/mxClaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, JSON] <br>
**Output Format:** [Plain text financial search results, optional .txt output file, and JSON-compatible Python dictionary fields for programmatic use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EM_API_KEY; writes results to a local text file by default unless no-save behavior is requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
