## Description: <br>
openclaw-eho lets agents query Korean apartment real transaction data by region, transaction type, and period through the Everyhouse real-estate service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[novb1492](https://clawhub.ai/user/novb1492) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this plugin to retrieve Korean apartment sale, jeonse, and monthly rent transaction insights for supported regions and date ranges. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: Property-search details such as region, apartment name, transaction type, and date range are sent to the Everyhouse real-estate service. <br>
Mitigation: Provide only the details needed for the lookup and avoid unnecessary personal or confidential information. <br>
Risk: The release is a third-party OpenClaw plugin distributed through npm. <br>
Mitigation: Install only when the publisher and package version are trusted for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/novb1492/korean-apartment-real-transactions) <br>
- [Everyhouse real-estate service](https://www.everyhouse-real-payment.com/?si=%EC%84%9C%EC%9A%B8&sn=0) <br>
- [npm package](https://www.npmjs.com/package/@brokimyeah/openclaw-eho) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Text response containing request details and the external service response, which may be JSON or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires sido, typeDetail, start, and end; gu, dong, and apt are optional for narrower apartment searches.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
