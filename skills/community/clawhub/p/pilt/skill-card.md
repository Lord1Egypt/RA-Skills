## Description:

Access Pilt fundraising data -- investor matches, campaign stats, outreach events, and deck analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[babpilt](https://clawhub.ai/user/babpilt)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect an agent to their Pilt account and retrieve fundraising data, including investor matches, campaign statistics, outreach events, and deck analysis summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a Pilt API key that grants access to account-scoped fundraising data.

Mitigation: Store the key only through the intended OpenClaw secret mapping, expose it as PILT_API_KEY at runtime, and rotate or revoke it if it may have been disclosed.

Risk: The skill can retrieve fundraising and outreach information from the user's Pilt account.

Mitigation: Install it only for agents that should access Pilt data, and review returned investor, campaign, and deck analysis data before using it in external workflows.

## Reference(s):

- [Pilt homepage](https://pilt.ai)
- [Pilt API gateway endpoint](https://pilt.ai/api/v1/gateway)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a PILT_API_KEY environment variable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
