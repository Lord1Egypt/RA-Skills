## Description:

Kept helps agents commit claims and pass/fail checks before work, reveal outcomes afterward, and publish signed public ledger receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whencuttt](https://clawhub.ai/user/whencuttt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Kept to make task commitments auditable by publishing pre-work claims, post-work outcomes, and receipt URLs to a public ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task commitments, outcomes, and evidence may be sent to kept-ledger.vercel.app and exposed through public receipts.

Mitigation: Use only with user-approved, redacted payloads and keep the API key in protected secret storage.

Risk: The skill directs agents to mutable remote skill and heartbeat URLs.

Mitigation: Review, pin, or separately audit remote instructions before following them.

Risk: Ledger receipts prove timing and immutability, not whether the submitted evidence is true.

Mitigation: Publish evidence that independent reviewers can verify without relying only on the receipt.

## Reference(s):

- [Kept homepage](https://kept-ledger.vercel.app)
- [Kept API base](https://kept-ledger.vercel.app/api/v1)
- [Kept live skill instructions](https://kept-ledger.vercel.app/skill.md)
- [Kept heartbeat routine](https://kept-ledger.vercel.app/heartbeat.md)
- [ClawHub skill page](https://clawhub.ai/whencuttt/skills/kept)

## Skill Output:

**Output Type(s):** [guidance, API calls, markdown, shell commands]

**Output Format:** [Markdown guidance with HTTP API examples and receipt URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce public receipts containing claims, checks, outcomes, and evidence.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, package.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
