## Description:

Connect OpenClaw Gateway to Paperclip, diagnose onboarding and reachability failures, claim and store Paperclip API keys, install the Paperclip skill, and orchestrate Paperclip agents and tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ihebsilence](https://clawhub.ai/user/ihebsilence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an OpenClaw instance to Paperclip, troubleshoot onboarding and reachability issues, claim API keys, install Paperclip skills, and create or manage Paperclip agents and tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can expose sensitive OpenClaw gateway tokens if used with an untrusted Paperclip URL.

Mitigation: Use only a trusted Paperclip deployment, verify the reachable base URL before onboarding, and avoid sending the primary gateway token to arbitrary URLs.

Risk: The workflow may grant broad operator access and persist claimed Paperclip API keys locally.

Mitigation: Avoid operator.admin unless specifically needed, store claimed credentials with restrictive permissions, and review the installed Paperclip skill before use.

Risk: Approving device pairings without checking identity can authorize the wrong device.

Mitigation: Approve device pairings by verified ID rather than by the latest pending request.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ihebsilence/skills/paperclip-orchestration)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request payloads, curl commands, and concise outcome summaries.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
