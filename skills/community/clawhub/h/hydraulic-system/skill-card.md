## Description: <br>
Guides users in Chinese through generating hydraulic and pneumatic system CAD production sheets using the Jixietools guest workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and engineering teams use this skill to collect hydraulic and pneumatic system parameters, call Jixietools APIs, review calculated values, and create a guest-accessible CAD production sheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Design parameters are sent to jixietools.com and the generated result link is guest-accessible. <br>
Mitigation: Use only data appropriate for that service, and avoid confidential engineering details unless the service's privacy and access controls meet the user's needs. <br>
Risk: The workflow relies on external API availability and responses for calculations and production-sheet creation. <br>
Mitigation: Review returned parameters and output links with the user before treating generated CAD production sheets as final. <br>


## Reference(s): <br>
- [Jixietools API base URL](https://jixietools.com/api/v1) <br>
- [ClawHub release page](https://clawhub.ai/liv09370/hydraulic-system) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls] <br>
**Output Format:** [Chinese Markdown with tables, inline shell commands, API responses, progress updates, and result links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates guest-accessible Jixietools production-sheet links after user-provided parameters are submitted.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
