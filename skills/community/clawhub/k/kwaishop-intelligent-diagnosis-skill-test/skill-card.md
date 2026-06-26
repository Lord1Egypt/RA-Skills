## Description: <br>
Looks up seller identifiers for a parsed merchant name through an internal Kuaishou merchant CRM service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimadara](https://clawhub.ai/user/jimadara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized Kuaishou or OpenClaw users use this skill to resolve a merchant name into seller identifiers through an internal merchant CRM service. The returned identifiers are passed back directly to the requester. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries an internal merchant CRM endpoint using a local OpenClaw username and returns raw seller identifiers. <br>
Mitigation: Run it only when the operator is authorized to query the service and disclose the returned seller identifiers to the requester. <br>
Risk: The public label describes domain testing while the behavior queries merchant seller data. <br>
Mitigation: Rename or re-scope the skill and document authorization, consent, and data-minimization expectations before general use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimadara/kwaishop-intelligent-diagnosis-skill-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Raw HTTP response body or authentication error text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contain seller identifiers returned by the internal merchant CRM service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
