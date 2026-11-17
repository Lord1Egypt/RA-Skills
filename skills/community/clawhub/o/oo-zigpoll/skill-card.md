## Description:

Zigpoll (zigpoll.com). Use this skill for ANY Zigpoll request — reading, creating, and updating data. Whenever a task involves Zigpoll, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected Zigpoll account can retrieve account, poll, participant, slide, and response data, or generate a trackable survey link. The skill guides the agent to inspect each action's schema and ask for confirmation before generating a link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified remote code and make broader agent changes without clear approval.

Mitigation: Review and approve CLI installation separately, preferably using a verified fixed release; consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Zigpoll data is accessed through the connected account, and link generation changes state.

Mitigation: Connect only the intended account, consider OOMOL's handling of Zigpoll data, and retain the skill's confirmation requirement before generating a survey link.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Zigpoll](https://www.zigpoll.com)
- [Zigpoll Web API documentation](https://docs.zigpoll.com/web-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector requests and results with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May retrieve Zigpoll account data or generate a trackable survey link.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
