## Description:

Gives AI agents a way to store, recall, and search household context using BlueColumn persistent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Home users and agents managing household tasks use this skill to recall maintenance context, personalize responses, and store post-interaction summaries in BlueColumn persistent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Household notes may be sent to and retained by an external persistent memory service.

Mitigation: Confirm exactly what will be stored before making memory API calls and avoid sensitive household details such as access codes, addresses, landlord contacts, schedules, financial data, or health information.

Risk: Broad post-interaction storage can capture more household context than the user intended.

Mitigation: Store concise summaries only after explicit user approval and omit unrelated conversation details.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/home-memory)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends selected household notes or recall queries to the BlueColumn service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
