## Description:

Use WeRead through an OOMOL-connected account to search and read books, shelves, highlights, notes, reviews, and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to search WeRead and retrieve reading information such as books, shelves, progress, highlights, notes, reviews, and recommendations through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run downloaded installer code whose payload was unavailable for inspection.

Mitigation: Review and approve CLI installation separately, using a verified release rather than allowing the fallback to execute downloaded scripts automatically.

Risk: Setup may synchronize managed skills and make broader agent changes.

Mitigation: Review oo's managed-skill synchronization and disable it if unwanted.

Risk: The connected account can expose WeRead notes and reading history to OOMOL.

Mitigation: Consider whether you want OOMOL to access your WeRead notes and history.

## Reference(s):

- [WeRead](https://weread.qq.com/)
- [WeChat Reading API documentation](https://github.com/Tencent/WeChatReading/tree/main/skills)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-weread)

## Skill Output:

**Output Type(s):** [Text, JSON data]

**Output Format:** [Natural-language responses and structured WeRead results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the selected WeRead action; paginated lists may require continuation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
