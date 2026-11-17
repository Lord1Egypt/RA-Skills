## Description:

Provides command usage guidance for keyword-based web searches through `miaoda-studio-cli search-summary` with AI-generated summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nice1234-h](https://clawhub.ai/user/nice1234-h)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route internet lookups to a keyword search command and receive summarized search results. JSON output can be requested when another tool or workflow needs to process the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are routed through an external CLI service whose provider handling is not fully disclosed.

Mitigation: Review the provider path before installation and avoid confidential, personal, or proprietary queries unless the service is trusted.

Risk: The skill broadly redirects internet lookup behavior to this search helper before direct URL fetching.

Mitigation: Review agent tool-routing behavior before deployment and preserve direct URL fetching for cases where the user provides a specific URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nice1234-h/skills/miaoda-web-search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash command examples; command output may be text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a 1-500 character search query; JSON output is optional.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
