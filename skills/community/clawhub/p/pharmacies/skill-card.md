## Description: <br>
Find nearby pharmacies. Invoke when user asks for drugstores near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for nearby pharmacy or drugstore results from an authorized latitude/longitude, with optional radius, limit, and availability filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs location data to find nearby pharmacies. <br>
Mitigation: Use it only after location sharing is authorized, prefer approximate location when sufficient, and avoid retaining precise coordinates. <br>
Risk: The packaged standard response schema is missing, which may reduce portability across integrations. <br>
Mitigation: Confirm the expected response shape before integration and track a publisher update that packages the response schema. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikeclaw007/pharmacies) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Markdown or structured text describing pharmacy search parameters, filters, errors, and result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authorized latitude/longitude input; response category is pharmacies.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
