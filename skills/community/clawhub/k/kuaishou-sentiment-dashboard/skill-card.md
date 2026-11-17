## Description:

快手短视频运营增长助手 helps creators, operators, brands, and e-commerce teams analyze Kuaishou content links for sentiment, audience signals, discussion themes, public-opinion risk, conversion leads, and optimization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operations teams, brands, and e-commerce users provide a Kuaishou video link or work ID to receive comment sentiment, audience-feedback themes, discussion focus, public-opinion signals, conversion leads, and recommended follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner sends Kuaishou links, derived content identifiers, and task requests to an external AI Skills service using an API key.

Mitigation: Use the skill only for content that may be shared with that service, and provide a narrowly scoped AISKILLS_API_KEY.

Risk: AISKILLS_BASE_URL is configurable, so a modified environment could send requests and credentials to an unintended service.

Mitigation: Pin AISKILLS_BASE_URL to the trusted HTTPS service before execution and review the environment in automated deployments.

Risk: The agent configuration allows implicit invocation, which could trigger analysis for sensitive business content.

Mitigation: Disable or gate implicit invocation where sensitive campaign, customer, or business data may appear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allinherog-star/skills/kuaishou-sentiment-dashboard)
- [Publisher profile](https://clawhub.ai/user/allinherog-star)
- [Form schema](references/form-schema.json)
- [Skill metadata](references/skill.json)
- [AI Skills service](https://ai-skills.ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown usage guidance and JSON task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Kuaishou content link or work ID and an AISKILLS_API_KEY; the runner polls until the analysis task completes or times out.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
