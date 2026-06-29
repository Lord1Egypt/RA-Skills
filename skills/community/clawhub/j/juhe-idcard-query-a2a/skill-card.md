## Description: <br>
This skill queries basic information encoded in an 18-digit Chinese resident ID number, including gender, birth date, and household registration region, through Juhe Data's paid A2M service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents use this skill when a user explicitly asks to look up the gender, birth date, or household registration region associated with an 18-digit Chinese resident ID number. The skill is for paid lookup or parsing workflows and is not suitable for validating whether an ID document is genuine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a full national ID number to a third-party API provider. <br>
Mitigation: Confirm the user explicitly wants the lookup before sending the ID number, and avoid real ID numbers unless the provider, retention terms, and legal basis are acceptable. <br>
Risk: Users may mistake the output for identity verification. <br>
Mitigation: Present the result only as information derived from ID-number format or encoding, and state that the skill cannot determine whether an ID document is genuine. <br>
Risk: The lookup is a paid workflow that depends on HTTP 402 payment handling. <br>
Mitigation: Show the requested parameters and order information before payment, preserve the payment response without modification, and stop if the user declines payment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/juhemcp/juhe-idcard-query-a2a) <br>
- [Publisher Profile](https://clawhub.ai/user/juhemcp) <br>
- [Juhe A2A Query Endpoint](https://apis.juhe.cn/a2a/query) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns or routes paid lookup results after HTTP 402 payment handling; expected result fields are gender, birth date, and household registration region.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
