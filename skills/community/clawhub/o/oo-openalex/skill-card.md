## Description:

Search and read OpenAlex data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers can search OpenAlex works and entities, retrieve records, and get autocomplete suggestions through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may automatically run an unverified online installer.

Mitigation: Install a verified oo CLI release yourself and review its local changes before use.

Risk: The external installer and hosted connector implementation have not been verified.

Mitigation: Review setup and connector behavior, and check whether automatic synchronization of other agent skills is enabled.

## Reference(s):

- [OpenAlex](https://openalex.org/)
- [OpenAlex API documentation](https://developers.openalex.org/how-to-use-the-api/api-overview)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured OpenAlex results (typically JSON) with concise text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and the records returned by OpenAlex.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
