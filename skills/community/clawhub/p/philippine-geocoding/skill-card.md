## Description:

Provides access to a Philippine Standard Geographic Code (PSGC) API through tool functions for Philippine geographic hierarchy lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up Philippine island groups, regions, provinces, cities, municipalities, barangays, districts, and code hierarchies through PSGC-oriented API tools. It is intended for geography lookup and code validation workflows that need structured Philippine administrative data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports mismatched Gaokao/XiaoBenYang remnants in a Philippine geography skill, which may confuse provider identity and intended behavior.

Mitigation: Verify the XiaoBenYang service and MCP identifier are the intended provider for Philippine PSGC data before installing or using the skill.

Risk: The scanner reports that the skill persists an API key in a local plaintext .env file.

Mitigation: Use a limited or disposable API key, avoid shared or version-controlled workspaces, and check or remove the generated .env file after use.

Risk: The scanner guidance calls out dependency and API-destination hardening needs.

Mitigation: Pin dependencies and restrict the API destination and allowed tool names before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/philippine-geocoding)
- [XiaoBenYang service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API data, configuration guidance]

**Output Format:** [Markdown summaries with structured API result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key before API-backed tools can return results.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
