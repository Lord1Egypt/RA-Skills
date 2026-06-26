## Description: <br>
Queries real-time global package tracking status and shipment history through Juhe, using a local courier-code list for supported carriers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check where a package is, whether it has been signed for, and which recent shipment events are available for a supplied tracking number and courier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracking numbers, courier codes, and any required phone-number suffix are sent to Juhe for lookup. <br>
Mitigation: Query only shipments where sharing that data with Juhe is acceptable, and provide phone-number suffixes only when the carrier requires them. <br>
Risk: A Juhe API key can be exposed if it is passed on the command line or committed in a local environment file. <br>
Mitigation: Prefer a shell or managed secret for JUHE_EXPRESS_KEY, avoid passing keys as command arguments, and do not commit scripts/.env. <br>


## Reference(s): <br>
- [Juhe Global Express Tracking API](https://www.juhe.cn/docs/api/id/43) <br>
- [Juhe Data Service](https://www.juhe.cn) <br>
- [Express Company List](references/express-company-list.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text tracking summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, a Juhe API key in JUHE_EXPRESS_KEY, and a courier company code for each tracking query.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
