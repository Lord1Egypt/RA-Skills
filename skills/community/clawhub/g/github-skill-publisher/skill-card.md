## Description:

Standardizes and publishes local agents, skills, or tool packages to public GitHub repositories through privacy review, repository setup, file uploads, topics, descriptions, and releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to turn local agent, skill, or tool directories into consistently structured GitHub repositories with privacy checks, repository metadata, uploads, topics, and release notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing workflow can upload broad local directories to GitHub, including public repositories.

Mitigation: Review the complete file list and run the documented privacy scan before publishing; prefer creating a private repository first when contents need additional review.

Risk: The workflow requires GitHub repository write authority through a token.

Mitigation: Use a least-privilege, short-lived token through a secure secret mechanism, clear it after use, and do not treat scanner output as proof that no private material is present.

## Reference(s):

- [GitHub Skill Publisher Cheatsheet](references/cheatsheet.md)
- [ClawHub skill page](https://clawhub.ai/shiyan521/skills/github-skill-publisher)
- [GitHub personal access token settings](https://github.com/settings/tokens)
- [GitHub API endpoint](https://api.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce repository descriptions, topic lists, release notes, file checklists, and publishing reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
