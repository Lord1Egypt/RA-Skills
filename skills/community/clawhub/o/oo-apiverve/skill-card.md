## Description:

APIVerve (apiverve.com). Use this skill for ANY APIVerve request — searching and reading data. Whenever a task involves APIVerve, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search and read APIVerve data through their connected OOMOL account, including age, currency, word, air quality, airline, and airport lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes piping a remote installer directly into a shell, and the installed CLI release has not been verified.

Mitigation: Review and verify a separate oo CLI release before installation; inspect installer contents before executing them.

Risk: Automatic skill synchronization could make broader agent changes without clear user control.

Mitigation: Inspect the synchronization behavior and disable automatic skill synchronization if it is not needed.

Risk: Information submitted through the connected account may be shared with OOMOL and APIVerve.

Mitigation: Submit only information you intend to share with both services.

## Reference(s):

- [APIVerve](https://apiverve.com/)
- [APIVerve API documentation](https://docs.apiverve.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Connector action calls with JSON payloads and JSON results, accompanied by shell command examples and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require a connected APIVerve account; input fields are determined by the connector action schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
