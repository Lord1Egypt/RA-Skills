## Description: <br>
Helps developers use JF device APIs to authenticate devices, check device status, capture snapshots, and retrieve livestream URLs across devices and channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent to JF devices with user-provided credentials, then check status, log in, capture images, obtain device tokens, or retrieve livestream playback URLs. <br>

### Deployment Geography for Use: <br>
Global, with documented API endpoints for international and mainland China access. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access JF device status, snapshots, and livestream URLs using supplied credentials. <br>
Mitigation: Install only for agents that should access those JF devices, and provide least-privilege credentials through environment variables. <br>
Risk: Printed tokens, session IDs, snapshot URLs, and livestream URLs can expose private device access while valid. <br>
Mitigation: Treat generated credentials and URLs as private, avoid sharing logs that contain them, and rotate or expire access when exposure is suspected. <br>
Risk: Changing the API endpoint can send credentialed requests to an unexpected service. <br>
Mitigation: Use the documented JF endpoints unless the replacement endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/jftech/jftech-open-pro-capture-livestream) <br>
- [JF Open Platform](https://open.jftech.com/) <br>
- [JF API Documentation](https://docs.jftech.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance and may print device tokens, session IDs, snapshot URLs, and livestream URLs returned by the JF APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
