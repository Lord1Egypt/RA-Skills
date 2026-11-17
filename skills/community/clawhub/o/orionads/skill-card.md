## Description:

Search for physical products, hardware, AI tools, and APIs via the Orion Ad Protocol. Returns structured data (JSON) optimized for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[celsojr2013](https://clawhub.ai/user/celsojr2013)

### License/Terms of Use:


## Use Case:

Agents and developers use Orion Ads to search for structured product offers, APIs, SDKs, and tools, and to optionally register, post ads, or check account balance when explicitly directed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command examples can create command-injection risk if user-controlled queries or JSON payloads are interpolated into shell strings.

Mitigation: Pass curl arguments without shell interpretation, use --data-urlencode for query values, escape JSON safely or write payloads to a temporary file, and only use ORION_API_KEY for posting ads or balance checks when explicitly directed.

Risk: Searches and optional account or ad actions send queries, account data, or ad data to OrionAds.

Mitigation: Install and invoke the skill only when this data sharing is acceptable for the user and task.

## Reference(s):

- [Orion Ads ClawHub Skill](https://clawhub.ai/celsojr2013/skills/orionads)
- [celsojr2013 ClawHub Publisher Profile](https://clawhub.ai/user/celsojr2013)
- [OrionAds Search API](https://orionads.net/api/v1/search)
- [OrionAds Register API](https://orionads.net/api/v1/register)
- [OrionAds Ads API](https://orionads.net/api/v1/ads)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON response schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses are described as structured JSON optimized for agents. ORION_API_KEY is optional and only needed for posting ads or checking account balance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
