## Description:

Packages claims-ledger-approved proof into reusable stat cards, case snippets, testimonial blocks, and comparison proofs tied to message-house pillars and ledger claim IDs, while flagging unsupported pillar claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and narrative teams use this skill to turn approved claims and proof materials into reusable proof modules that can be placed where each message-house pillar makes a claim. It also identifies proof gaps for follow-up claim review instead of inventing missing evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads claims ledgers, story banks, message-house files, and pasted proof material that may contain sensitive commercial information.

Mitigation: Install and run it only in projects where that access is acceptable, and limit supplied proof material to information the team is allowed to process.

Risk: Memory saves or claim-gap proposals could preserve inaccurate proof packaging if approved without review.

Mitigation: Review proof modules, source labels, as-of dates, ledger claim IDs, and gap proposals before approving any persistent writes.

Risk: User-provided proof material may contain untrusted instructions or unsupported claims.

Mitigation: Treat proof inputs as evidence only, keep unverified or ledger-absent proofs marked as needing a source, and route them to claim review instead of shipping them as substantiated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/proof-point-packager)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown proof module sets, gap lists, and handoff summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each proof module is expected to include a pillar tag, ledger claim ID, source label, and as-of date.]

## Skill Version(s):

19.0.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
