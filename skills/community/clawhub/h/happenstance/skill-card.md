## Description:

Search your professional network and research people using the Happenstance API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[almostimplemented](https://clawhub.ai/user/almostimplemented)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to search professional networks, research individual profiles, page through Happenstance results, list searchable groups, and check API credit usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, person descriptions, network-scope choices, and returned profile details may contain sensitive personal or professional data.

Mitigation: Submit only necessary information to Happenstance and avoid unnecessary sensitive personal data about third parties.

Risk: The HAPPENSTANCE_API_KEY grants authenticated access to paid API operations and usage data.

Mitigation: Store the key in an environment variable or secret manager and avoid including it in prompts, logs, code snippets, or shared transcripts.

Risk: Search and research operations consume Happenstance credits and may fail when credits are insufficient or concurrent request limits are reached.

Mitigation: Check usage before starting batches and handle 402 and 429 responses with appropriate user confirmation or retry behavior.

## Reference(s):

- [Happenstance Developer Documentation](https://developer.happenstance.ai)
- [Happenstance Skill on ClawHub](https://clawhub.ai/almostimplemented/skills/happenstance)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HAPPENSTANCE_API_KEY and curl; Happenstance searches and research requests run asynchronously and require polling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
