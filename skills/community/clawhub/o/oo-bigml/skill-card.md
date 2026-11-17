## Description:

BigML (bigml.com). Use this skill for ANY BigML request — reading, creating, updating, and deleting data. Whenever a task involves BigML, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use the skill to inspect BigML models and predictions, submit predictions, and manage stored prediction resources through their connected BigML account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented CLI installer runs downloaded software whose behavior was not verified.

Mitigation: Review the installation source and prefer a separately verified CLI installation; require approval before installing software or changing other agent skills.

Risk: Prediction creation changes BigML state, and prediction deletion permanently removes a resource.

Mitigation: Review the exact action and payload with the user before a write, and confirm the deletion target before removing a prediction.

## Reference(s):

- [BigML homepage](https://bigml.com/)
- [BigML API authentication documentation](https://bigml.com/api/authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-bigml)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [JSON action results with concise guidance and oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results may include model or prediction data; prediction creation changes state and prediction deletion is destructive.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
