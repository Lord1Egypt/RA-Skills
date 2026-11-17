## Description:

Use this skill to read, create, and update MailGenius data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email operators can create MailGenius test addresses for deliverability audits, check audit results, list audits, and review daily test limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified code and may make broader changes to agent installations without clearly explaining them.

Mitigation: Review and approve CLI installation separately using a verified release. Disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1 when only MailGenius operations are needed.

## Reference(s):

- [MailGenius](https://www.mailgenius.com/)
- [MailGenius API documentation](https://app.mailgenius.com/api-docs/index.html)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [MailGenius API results as JSON, with text summaries where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can create test audit records; check the relevant action and payload before use.]

## Skill Version(s):

1.0.4 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
