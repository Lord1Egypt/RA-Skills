## Description: <br>
Guides users through a JXT guest workflow to collect heat exchanger parameters, calculate values, and generate CAD drawing production links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liv09370](https://clawhub.ai/user/liv09370) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and engineers use this skill to collect heat exchanger design inputs, call the JXT mechanical-parts API, review calculated parameters, and obtain a shareable CAD drawing production link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CAD parameters, manufacturing details, generated guest codes, and jixietools.com share links may expose private design information. <br>
Mitigation: Use the guest workflow only for designs that can be sent to the JXT service and shared by link; treat generated links and guest codes as sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liv09370/heat-exchanger) <br>
- [JXT API base URL](https://jixietools.com/api/v1) <br>
- [JXT guest production sheet link pattern](https://jixietools.com/s/GUEST_CODE) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown conversation with tables, JSON examples, and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Chinese-language interaction steps and shareable JXT guest workflow links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
