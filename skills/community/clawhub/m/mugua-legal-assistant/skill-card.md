## Description: <br>
对接木瓜法律 API，提供法律咨询、案件要素提取和案件完整分析能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzw23333](https://clawhub.ai/user/yzw23333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and legal operations teams use this skill to submit legal questions, case text, files, parties, facts, and demands to a configured Mugua Legal API endpoint for legal consultation, element extraction, and case analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Legal questions, case data, uploaded files, and API credentials are sent to the configured Mugua endpoint. <br>
Mitigation: Verify the base URL, review the provider's privacy terms, use a scoped and rotatable API key, and avoid uploading privileged or highly sensitive legal materials unless that external processing is acceptable. <br>
Risk: The default base URL is a test endpoint, which may be unsuitable for real matters. <br>
Mitigation: Replace or verify the configured base URL before using the skill with production or sensitive legal data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yzw23333/mugua-legal-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/yzw23333) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, JSON, Guidance] <br>
**Output Format:** [JSON response containing code, message, data, request_id, and success fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided API key and configured Mugua Legal API base URL.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence, artifact metadata, and skill.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
