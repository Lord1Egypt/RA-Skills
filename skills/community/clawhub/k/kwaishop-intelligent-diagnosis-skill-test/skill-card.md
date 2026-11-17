## Description:

Looks up merchant seller identifiers by using a local OpenClaw username and a merchant name against a Kuaishou internal merchant CRM endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimadara](https://clawhub.ai/user/jimadara)

### License/Terms of Use:

MIT-0

## Use Case:

ClawHub and OpenClaw users use this skill to resolve merchant names into seller lookup results for Kuaishou merchant workflows. Users should install it only when authorized to query the internal merchant CRM and expose returned seller data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use the operator's local OpenClaw username to query a Kuaishou internal merchant CRM.

Mitigation: Install and run it only for operators who are authorized to perform the intended merchant queries.

Risk: The skill returns raw seller lookup results without additional filtering.

Mitigation: Review returned data before sharing it outside the approved workflow or audience.

Risk: The advertised domain testing purpose may not clearly communicate the internal merchant CRM lookup behavior.

Mitigation: Review the skill description and release notes so users understand the CRM query behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimadara/skills/kwaishop-intelligent-diagnosis-skill-test)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Raw API response or plain-text error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns unfiltered seller lookup results from the configured CRM request.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
