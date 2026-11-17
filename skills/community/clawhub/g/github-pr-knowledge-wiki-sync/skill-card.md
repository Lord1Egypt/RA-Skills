## Description:

Generates structured technical documentation from GitHub pull request metadata and diffs, then syncs it to Feishu Wiki, WeCom Docs, or local Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical leads use this skill to turn GitHub pull request content and code-change analysis into reusable team documentation. It supports publication to Feishu Wiki, WeCom Docs, or a local Markdown file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PR titles, descriptions, file lists, diffs, and generated summaries may be written to external documentation systems or local files.

Mitigation: Use the skill only on trusted repositories, avoid PRs containing secrets or sensitive architecture details, and verify the destination workspace before publication.

Risk: Generated documentation may include incorrect summaries or risk analysis.

Mitigation: Review the generated document before publishing it to Feishu Wiki, WeCom Docs, or a shared Markdown location.

Risk: Inputs for commands and file output are weakly scoped according to the security evidence.

Mitigation: Confirm the PR URL, repository, output target, and local output path before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/github-pr-knowledge-wiki-sync)
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation, command guidance, and publication status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can publish generated PR documentation to Feishu Wiki, WeCom Docs, or a local Markdown file depending on the selected target.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, workflow.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
