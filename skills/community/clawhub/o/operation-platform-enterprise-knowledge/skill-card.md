## Description: <br>
Resolves a merchant name to seller IDs by querying an internal Kuaishou merchant CRM service with a locally configured username. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimadara](https://clawhub.ai/user/jimadara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized internal operators use this skill to resolve a merchant or seller name into seller IDs from an internal CRM lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a locally configured username and parsed merchant name to an internal Kuaishou merchant CRM service. <br>
Mitigation: Use only in authorized environments, confirm the username configuration before lookup, and disclose the identity use to users. <br>
Risk: The security summary reports that the skill is labeled as domain testing while its behavior is merchant CRM seller lookup. <br>
Mitigation: Treat the skill as an internal merchant lookup tool and rename or describe it accordingly before broader release. <br>
Risk: The artifact returns raw seller lookup results without filtering. <br>
Mitigation: Review returned fields before sharing or storing results, and limit output to the seller IDs or fields required for the task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jimadara/operation-platform-enterprise-knowledge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls] <br>
**Output Format:** [Raw JSON or text returned from the seller lookup API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the upstream lookup response without filtering according to the artifact behavior.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
