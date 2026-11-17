## Description:

Use Supabase through a connected account to read, create, update, or delete Supabase data and manage related projects and resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect Supabase organizations and projects, query data, manage storage and secrets, and perform approved project changes through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback directs the agent to execute downloaded software without a separate approval or integrity check.

Mitigation: Review and approve CLI installation separately, preferably using a pinned and verified release.

Risk: Connected Supabase access can expose or change project data and resources.

Mitigation: Connect only the projects and permissions needed, and retain the required confirmations for writes and deletions.

## Reference(s):

- [Supabase API Documentation](https://supabase.com/docs/reference/api/introduction)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI Installation Guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and structured results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas vary by operation; write and destructive actions require confirmation.]

## Skill Version(s):

1.0.8 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
