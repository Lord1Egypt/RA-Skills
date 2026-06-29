## Description: <br>
Retrieves a full personal profile, including name, email, LinkedIn URL, title, and employer, for one Apollo person ID through the paid OpenMerch API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kernel-gd](https://clawhub.ai/user/kernel-gd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, sales operators, and recruiting operators use this skill to enrich a single known Apollo person ID into a normalized contact profile. Users should run it only when they have a lawful basis to process the returned personal contact data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill returns sensitive personal contact data such as names, email addresses, and LinkedIn URLs. <br>
Mitigation: Use it only with a lawful basis for processing personal data, minimize storage and sharing, and follow applicable privacy obligations. <br>
Risk: Each enrichment can spend OpenMerch account credits. <br>
Mitigation: Review the planned price from the OpenMerch plan step before execution and proceed only when the cost is acceptable. <br>
Risk: The OpenMerch API key grants access to a paid external service. <br>
Mitigation: Keep OPENMERCH_API_KEY private and avoid exposing it in prompts, logs, command history, or shared outputs. <br>
Risk: Changing OPENMERCH_BASE_URL can redirect requests to a non-default endpoint. <br>
Mitigation: Use the default OpenMerch API URL unless you deliberately trust and control the alternate endpoint. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kernel-gd/skills/openmerch-people-enrichment) <br>
- [OpenMerch documentation](https://docs.openmerch.dev) <br>
- [OpenMerch API base URL](https://api.openmerch.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON result examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns one normalized profile per Apollo person ID; fields absent from the upstream response are omitted rather than synthesized.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
