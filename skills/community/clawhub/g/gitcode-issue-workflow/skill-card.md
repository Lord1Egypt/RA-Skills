## Description:

End-to-end GitCode issue workflow covering issue pickup, analysis, code modification, and PR submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guitenbay](https://clawhub.ai/user/guitenbay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to handle GitCode issues end to end, from reading issue details through confirmed design planning, code changes, branch management, and pull request submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitCode access tokens may be exposed when stored in repo-visible files or passed through URL query strings.

Mitigation: Prefer the GitCode CLI login flow, avoid storing tokens in MEMORY.md or repository files, avoid API examples that put tokens in URLs, and use least-privilege short-lived tokens.

Risk: Cleanup commands can remove the entire temp/ directory.

Mitigation: Review cleanup commands before execution and keep any artifacts that must be preserved outside the temp/ directory.

## Reference(s):

- [GitCode API Reference](references/gitcode-api.md)
- [GitCode CLI](https://github.com/codeasier/gitcode-cli)
- [ClawHub Skill Page](https://clawhub.ai/guitenbay/skills/gitcode-issue-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, API examples, and pull request templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitCode CLI authentication, local git repository access, and explicit user confirmation before code changes or external write operations.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
