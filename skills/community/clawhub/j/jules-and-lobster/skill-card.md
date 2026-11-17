## Description:

Uses the Jules REST API (v1alpha) via curl to list sources, create and monitor sessions, approve plans, send messages, and retrieve outputs such as PR URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanjacob99](https://clawhub.ai/user/sanjacob99)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to delegate coding work to Jules through the REST API, monitor sessions, approve plans, and collect pull request outputs for connected GitHub repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled shell helper may execute local Python code when crafted task text is passed through its JSON encoding path.

Mitigation: Use only trusted task text until scripts/jules_api.sh is fixed to pass values into JSON encoding as data rather than generated Python source.

Risk: The skill uses JULES_API_KEY to operate against connected repositories through the Jules API.

Mitigation: Keep JULES_API_KEY scoped and protected, rotate it as needed, and limit Jules GitHub app access to intended repositories.

Risk: Automatic PR creation or skipping plan approval can allow changes to proceed with less human review.

Mitigation: Avoid --auto-pr and --no-plan-approval on sensitive repositories, and require plan approval for production or high-impact work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sanjacob99/skills/jules-and-lobster)
- [Jules API documentation](https://jules.google/docs/api/reference/overview/)
- [Jules sessions reference](https://jules.google/docs/api/reference/sessions/)
- [Jules activities reference](https://jules.google/docs/api/reference/activities/)
- [Jules sources reference](https://jules.google/docs/api/reference/sources/)
- [Google Developers Jules API](https://developers.google.com/jules/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JULES_API_KEY and access to connected GitHub repositories through Jules.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
