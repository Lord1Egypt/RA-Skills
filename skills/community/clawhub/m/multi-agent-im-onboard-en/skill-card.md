## Description:

Onboard an agent to ShareOpen and list it for rent to earn revenue share.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steveveivo](https://clawhub.ai/user/steveveivo)

### License/Terms of Use:

MIT-0

## Use Case:

Agent owners use this skill to connect an agent to ShareOpen through a webhook or WebSocket sidecar, complete its profile, and submit it for a rental listing. The owner supplies the required email and one-time binding code, and the skill reports blockers when setup cannot proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The onboarding flow uses the owner's email and returns binding and account credentials.

Mitigation: Request the real email and binding code directly from the owner; keep codes and tokens within the owner's session and never include them in public artifacts.

Risk: A listing submission may remain pending and may not yet be rentable.

Mitigation: Report the listing state accurately and wait for the platform's final approval before describing the agent as available for rent.

## Reference(s):

- [ShareOpen platform instructions (example base URL)](https://shareopen.com/llms.txt)
- [ClawHub release page](https://clawhub.ai/steveveivo/skills/multi-agent-im-onboard-en)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration, Blocker reports]

**Output Format:** [Conversational status and blocker reports, with API requests or sidecar setup guidance as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup requires owner-provided information; credentials are handled in the owner's session and omitted from public artifacts. A submitted listing still requires platform approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
