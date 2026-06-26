## Description: <br>
Fetch specified crypto spot prices from OKX and present them in USD display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chgy123](https://clawhub.ai/user/chgy123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, traders, and developers use this skill to fetch one-shot OKX spot quotes for specified crypto symbols and display them in USD order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OKX-related workflows can affect real funds if paired with live trading tools or credentials. <br>
Mitigation: Use least-privileged OKX credentials where applicable and review any trade, cancel, leverage, or close-position confirmation before execution. <br>
Risk: Market prices are live external data and may be unavailable, delayed, or missing for a requested symbol. <br>
Mitigation: Treat returned prices as point-in-time quotes and verify important financial decisions against OKX or another authoritative market source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chgy123/okx-symbol-prices) <br>
- [OKX](https://www.okx.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands] <br>
**Output Format:** [Plain text price lines or JSON objects per symbol.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results preserve the requested symbol order and report N/A when no supported OKX USD-based ticker is found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
