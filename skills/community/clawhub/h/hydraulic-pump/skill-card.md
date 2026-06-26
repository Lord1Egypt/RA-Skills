## Description: <br>
Guides Chinese-speaking users through generating hydraulic pump CAD drawings with the JXT mechanical parts platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and mechanical design users can use this skill to collect hydraulic pump parameters, call the JXT service, review calculated values, and create a guest production sheet for CAD drawing generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends pump design details and filenames to jixietools.com. <br>
Mitigation: Review before installing and avoid entering confidential designs, dimensions, customer data, or proprietary filenames unless third-party sharing is acceptable. <br>
Risk: The workflow uses guest-style output and session links whose expiration and authorization scope are not clarified in the evidence. <br>
Mitigation: Treat generated links and codes as shareable access tokens, avoid posting them publicly, and confirm access controls before using the skill with sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liv09370/hydraulic-pump) <br>
- [JXT mechanical tools API](https://jixietools.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls] <br>
**Output Format:** [Chinese conversational guidance with Markdown tables, curl commands, API responses, and generated production-sheet links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses guest-style production-sheet links and polls the third-party service for drawing status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
