## Description:

liuduoduo helps agents find Liuyang-area handymen, restaurants, and hotels with contact and pricing details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[malinguo](https://clawhub.ai/user/malinguo)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent for local-life recommendations in Liuyang, including handyman services, restaurants, and hotels. The agent calls the skill's MCP tools and returns merchant names, phone numbers, prices, addresses, and relevant features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local-life queries are sent to the configured MCP endpoint.

Mitigation: Install only when that endpoint is acceptable for the intended users and data handling expectations.

Risk: Merchant listings, phone numbers, and prices may be demo or publisher-provided data.

Mitigation: Present results as listings to verify independently before purchase, booking, or service dispatch.

Risk: Self-hosted deployments may use broad dependency ranges.

Mitigation: Pin and review backend dependencies before deploying the MCP service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/malinguo/skills/liuduoduo-life-skill)
- [MCP endpoint](https://xilejie-silk.com/liuyang-life/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API Calls]

**Output Format:** [Markdown or text with MCP tool call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns merchant names, phone numbers, prices, addresses, ratings, service times, and feature summaries from read-only listing tools.]

## Skill Version(s):

0.1.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
