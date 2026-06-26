## Description: <br>
Gpu Check polls two local RTX 3090 and RTX 4090 GPU status endpoints and reports memory usage and node availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fainaltn](https://clawhub.ai/user/fainaltn) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and operators use this skill in chat to check whether local AI compute nodes are online and how much GPU memory is currently in use before routing work to them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured private IP addresses may not be the intended GPU nodes in another environment. <br>
Mitigation: Confirm the two node addresses and /gpu endpoints before installing or running the skill. <br>
Risk: GPU status data from the /gpu endpoints may be visible in chat output. <br>
Mitigation: Expose only status data that is acceptable for chat display and restrict endpoint access to trusted local network users. <br>
Risk: Dependency installation may pull packages from an untrusted or unexpected source. <br>
Mitigation: Install with the included lockfile or a trusted npm registry. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fainaltn/gpu-check) <br>
- [Publisher profile](https://clawhub.ai/user/fainaltn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API status] <br>
**Output Format:** [Markdown text with GPU usage percentages, progress bars, and node status lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries two configured private-network /gpu endpoints with a short timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
