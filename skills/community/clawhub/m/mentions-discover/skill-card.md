## Description: <br>
Discover the queries worth tracking for a brand's AI visibility, including informational, commercial, and comparison-intent prompts, via MentionsAPI.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikhonit](https://clawhub.ai/user/nikhonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate a starting set of brand visibility queries before measuring or monitoring how often a brand appears in AI answers. It is intended for explicit requests to discover prompts or questions to track for a brand, industry, or competitive comparison set. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a local MENTIONSAPI_KEY for a paid external service. <br>
Mitigation: Install only if the user trusts MentionsAPI, store the key locally, and rotate the key if it is rejected or exposed. <br>
Risk: Each discover_queries call is documented as costing $0.50. <br>
Mitigation: Confirm the brand, industry context, and requested count before calling the tool. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nikhonit/mentions-discover) <br>
- [MentionsAPI Homepage](https://mentionsapi.com) <br>
- [MentionsAPI Endpoint Reference](https://mentionsapi.com/docs/api/check) <br>
- [MentionsAPI OpenAPI Spec](https://mentionsapi.com/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration] <br>
**Output Format:** [JSON object containing candidate query strings, intents, cost and balance fields, or an error object.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MENTIONSAPI_KEY and sends brand, optional industry, and count values to MentionsAPI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
