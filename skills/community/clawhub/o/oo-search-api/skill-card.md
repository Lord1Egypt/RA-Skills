## Description:

SearchApi (searchapi.io). Use this skill for ANY SearchApi request — searching and reading data. Whenever a task involves SearchApi, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search SearchApi and retrieve search results, cached results, location data, and connected account usage through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified remote code and introduce broader agent changes without clear user control.

Mitigation: Review and install a verified CLI release yourself before enabling the skill, and check which additional agent skills it installs or updates.

Risk: SearchApi requests involve a connected account, and OOMOL may handle requests and billing.

Mitigation: Connect only the intended SearchApi account and consider OOMOL's role in handling requests and billing.

## Reference(s):

- [SearchApi Google documentation](https://www.searchapi.io/docs/google)
- [SearchApi](https://www.searchapi.io)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, HTML, Shell commands]

**Output Format:** [oo CLI commands and SearchApi results in JSON, HTML, or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected SearchApi action and its live input schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
