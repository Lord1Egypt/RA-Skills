## Description: <br>
Extracts specified entities and relationships from Chinese police incident report text and returns only strict structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy020326](https://clawhub.ai/user/andy020326) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to extract predefined entities and relationship triples from police incident report text for downstream structured review or case-data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to extract sensitive personal data from police-report text, including IDs, phone numbers, bank card numbers, case details, people, locations, and alleged behavior. <br>
Mitigation: Use it only in workflows authorized to process that data, and avoid submitting real personal or case information unless the agent runtime and downstream systems are approved for it. <br>
Risk: Incorrect extraction or reversed relationship direction could misrepresent people, organizations, actions, or case facts. <br>
Mitigation: Have a qualified reviewer check the JSON output before using it for operational, investigative, or legal decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy020326/police-nerre-test) <br>
- [Publisher profile](https://clawhub.ai/user/andy020326) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis] <br>
**Output Format:** [Strict JSON object with entity arrays and relationship triples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The output must preserve the required Chinese field names and relationship labels, include empty arrays when no entity values are found, and contain no Markdown or explanatory text.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
