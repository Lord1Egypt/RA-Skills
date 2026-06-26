## Description: <br>
Query Indian mutual fund NAV data, scheme info, and history via the free MFapi.in REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kanaksinghal](https://clawhub.ai/user/kanaksinghal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to look up Indian mutual fund schemes, latest NAVs, and historical NAV data through MFapi.in. It can also resolve an ISIN to a scheme code before fetching the latest NAV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fund names, scheme codes, and ISINs are sent to the third-party MFapi.in service when queries run. <br>
Mitigation: Avoid using the skill for sensitive portfolio analysis unless third-party disclosure to MFapi.in is acceptable. <br>
Risk: Mutual fund data is retrieved from an external service and may be unavailable or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Verify NAV and scheme data against authoritative fund or AMFI sources before relying on results. <br>


## Reference(s): <br>
- [ClawHub Mfapi release page](https://clawhub.ai/kanaksinghal/mfapi) <br>
- [MFapi.in](https://www.mfapi.in) <br>
- [MFapi REST API base URL](https://api.mfapi.in) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with shell commands, Python helper usage, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Python helper may return a JSON object for one ISIN or a JSON array for multiple ISINs.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
