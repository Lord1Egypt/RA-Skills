## Description: <br>
Formats and converts developer data across JSON, YAML, XML, SQL, numeric bases, HTML entities, and Cron expressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiebang-tools](https://clawhub.ai/user/jiebang-tools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert and format JSON/YAML, XML, SQL, numeric bases, HTML entities, and Cron expressions during development and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided data is sent to an external jiebang.site service. <br>
Mitigation: Do not use the skill with secrets, production SQL, internal configuration files, customer data, proprietary XML/HTML, or other sensitive content unless that data transfer is approved. <br>
Risk: The service call uses an admin-style credential. <br>
Mitigation: Review the credential handling, permissions, and retention practices before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiebang-tools/jiebang-data-formatter) <br>
- [Jiebang service endpoint](https://www.jiebang.site) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration] <br>
**Output Format:** [JSON response containing converted or formatted data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include success status and result data; some operations also include length, validation, description, or next-run fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
