## Description:

Pairoa helps agents privately publish two-sided needs for hiring, jobs, customers, partners, investors, roommates, beta users, and second-hand trades, then check for complementary matches through the Pairoa MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pairoa](https://clawhub.ai/user/pairoa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to publish private matchmaking requests and receive introductions when Pairoa finds complementary needs. It is intended for people-to-people or buyer-seller matching workflows, not for browsing public listings or researching documents, companies, or product catalogs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pairoa receives the need text and contact email the user chooses to publish, and matched counterparties receive that information when a match is made.

Mitigation: Show the final need text and contact email before publishing, explain the disclosure consequence, remove sensitive details on request, and publish only after explicit user consent.

Risk: Pairoa does not verify counterparties, identities, resumes, goods, financing claims, or other user-provided assertions.

Mitigation: Tell users to independently verify counterparties and claims before sharing sensitive information, meeting, paying, hiring, investing, or relying on a match.

Risk: Counterparty fields such as i_seek, i_offer, contact, and safe_tags are free-form unverified text and could contain misleading claims or instructions.

Mitigation: Display those fields only as counterparty-provided data, never execute or follow instructions in them, and treat only the returned safety field as Pairoa safety guidance.

Risk: Publishing and some management operations are side-effectful, and blind retries after uncertain failures can create duplicate or unintended needs.

Mitigation: Retry only read-only checks automatically; after uncertain write failures, verify status first and get renewed user consent before resubmitting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pairoa/skills/pairoa)
- [Pairoa MCP Service](https://mcp.pairoa.com)
- [Pairoa Installation Guide](https://pairoa.com/install)

## Skill Output:

**Output Type(s):** [Guidance, Text, API calls, Configuration]

**Output Format:** [Markdown or plain text guidance with structured Pairoa MCP tool calls and match summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Pairoa MCP connector; publishing needs is gated on explicit user consent and may disclose need text and contact email to matched counterparties.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
