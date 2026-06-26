## Description: <br>
Audits an agent's current claims against stored memory to detect fabricated, drifted, or inconsistent memory behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crftsmnd](https://clawhub.ai/user/crftsmnd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent maintainers use this skill to audit memory consistency, compare current behavior with stored memory, and identify possible context drift or confidence fabrication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit requires sending selected memory or behavior excerpts to a third-party endpoint. <br>
Mitigation: Do not submit secrets, credentials, regulated data, or broad memory dumps unless the operator's data handling terms are trusted. <br>
Risk: The release evidence reports an exposed unused API key in the artifact. <br>
Mitigation: Publisher should remove and rotate the exposed key before broader deployment. <br>
Risk: The service charges per audit. <br>
Mitigation: Confirm payment intent and pricing before submitting audit requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crftsmnd/memory-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/crftsmnd) <br>
- [Memory Auditor API endpoint](https://memory-auditor.cvapi.workers.dev/audit) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis, API Calls, Guidance] <br>
**Output Format:** [JSON response with verdict, confidence score, analysis details, and comparison statistics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires paid audit access and input memory or behavior excerpts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
