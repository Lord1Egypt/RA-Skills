## Description:

Returns today's lunch menu of a German university canteen via the public OpenMensa API, with one-time city and canteen setup and no API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rifatdevelopment](https://clawhub.ai/user/rifatdevelopment)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up today's or another date's lunch menu for a configured German university canteen, including student prices and vegan or vegetarian tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Menu and date lookups are sent to OpenMensa.

Mitigation: Install only if users are comfortable with OpenMensa receiving canteen and date lookup requests.

Risk: The selected city and canteen are stored in a local config file.

Mitigation: Re-run setup to change the saved default and review local skill storage policies before deployment.

Risk: A runtime with broad shell or network access can increase the impact of any skill script behavior.

Mitigation: Review the script before deployment and limit runtime access to the documented OpenMensa HTTPS use case where possible.

## Reference(s):

- [OpenMensa](https://openmensa.org)
- [OpenMensa API v2](https://openmensa.org/api/v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown bullet list with a date header; setup and debugging steps use inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; sends canteen and date lookups to OpenMensa; creates a local config.json during setup.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
