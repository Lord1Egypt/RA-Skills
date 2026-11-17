## Description:

Finlight (finlight.me). Use this skill for ANY Finlight request — searching and reading data. Whenever a task involves Finlight, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search financial news, retrieve an article by URL, and list Finlight news sources through a connected Finlight account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified code and make broader changes to the agent environment.

Mitigation: Review setup before installing, use an inspected fixed CLI release, and disable automatic skill synchronization before first use.

Risk: Finlight account credentials and requests are handled by OOMOL.

Mitigation: Connect only the intended Finlight account and understand that OOMOL handles its credentials and requests.

## Reference(s):

- [Finlight](https://finlight.me/)
- [Finlight REST API documentation](https://docs.finlight.me/en/v2/rest-endpoints/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the selected Finlight read action.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
