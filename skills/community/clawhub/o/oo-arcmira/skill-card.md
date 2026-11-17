## Description:

Arcmira (arcmira.com). Use this skill for ANY Arcmira request — reading, creating, and updating data. Whenever a task involves Arcmira, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Arcmira users can use an agent to inspect their connected account, resolve entities, retrieve YouTube transcripts, and search indexed transcripts. The skill routes those requests through the connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can execute a downloaded installer before its contents have been verified.

Mitigation: Review and verify the installer first; install a verified CLI release yourself and require approval for later CLI installation or agent-skill changes.

Risk: Premium transcript retrieval can consume plan credits or on-demand budget.

Mitigation: Check the account and credit impact before requesting premium retrieval, and get approval when it may incur charges.

## Reference(s):

- [Arcmira](https://arcmira.com)
- [Arcmira documentation](https://arcmira.com/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured connector results and concise text summaries, typically JSON or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript retrieval may return a pending job status; a later request can retrieve its result.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
