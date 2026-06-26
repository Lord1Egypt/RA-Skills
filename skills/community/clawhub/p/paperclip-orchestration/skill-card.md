## Description: <br>
Connect OpenClaw Gateway to Paperclip, diagnose onboarding and reachability failures, claim and store Paperclip API keys, install the Paperclip skill, and orchestrate Paperclip agents and tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ihebsilence](https://clawhub.ai/user/ihebsilence) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to onboard OpenClaw Gateway into Paperclip, test connectivity, handle pairing and approval, claim API keys, and manage Paperclip agents and tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow shares OpenClaw gateway access and stores Paperclip API credentials. <br>
Mitigation: Use only a trusted Paperclip organization and base URL, explicitly approve token sharing, and protect, rotate, or delete the saved API key file when it is no longer needed. <br>
Risk: The workflow can approve device pairing and install follow-on Paperclip skills. <br>
Mitigation: Review device pairing requests and any additional Paperclip skill before approval or installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ihebsilence/paperclip-orchestration) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes connectivity checks, onboarding payload guidance, local credential handling steps, and outcome summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
