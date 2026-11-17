## Description:

This skill helps internal users query merchant seller IDs from a seller name for diagnosis workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimadara](https://clawhub.ai/user/jimadara)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to parse a merchant name from a request, resolve matching seller IDs, and support merchant diagnosis or domain-testing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local username credential and sends it to an internal merchant endpoint.

Mitigation: Document the credential access clearly and require explicit user consent before sending the username.

Risk: The skill can return raw merchant-system responses to the user.

Mitigation: Return only sanitized fields needed for the diagnosis workflow.

Risk: The release is labeled as domain testing while the behavior is merchant lookup.

Mitigation: Rename and document the skill as an internal merchant lookup or diagnosis tool before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimadara/skills/intelligent-diagnosis-skill-test)
- [Publisher profile](https://clawhub.ai/user/jimadara)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON response containing merchant lookup results or an authentication error.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return raw merchant-system response fields unless the output is sanitized.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
