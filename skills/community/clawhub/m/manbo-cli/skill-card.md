## Description:

Guides users to view Kilamanbo audio drama hot-search rankings with the manbo-cli command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liaofuyan](https://clawhub.ai/user/liaofuyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when a request mentions Manbo, audio dramas, manbo, or hot-search rankings and the user wants the current Manbo hot-search list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to globally install an unpinned external npm CLI that is not included in the reviewed artifact.

Mitigation: Verify the manbo-cli npm package, publisher, source, and version before installation; prefer pinned or local installation when available.

Risk: Running a globally installed CLI with broad privileges can increase local execution risk.

Mitigation: Avoid administrator privileges and require clear user confirmation before installation or execution.

## Reference(s):

- [Kilamanbo](https://kilamanbo.com)
- [ClawHub skill page](https://clawhub.ai/liaofuyan/skills/manbo-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/liaofuyan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
