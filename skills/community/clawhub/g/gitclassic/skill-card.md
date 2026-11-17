## Description:

Fast, no-JavaScript GitHub browser optimized for AI agents. Browse public repos, read files, view READMEs with sub-500ms load times. PRO adds private repo access via GitHub OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heythisischris](https://clawhub.ai/user/heythisischris)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent operators use GitClassic to browse GitHub repositories, read files and READMEs, search GitHub content, and inspect documentation through lightweight server-rendered HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using GitClassic PRO for private repositories grants a third-party service OAuth-based access to selected private repository content.

Mitigation: Confirm GitClassic is trusted, review GitHub OAuth scopes and repository selection, and avoid granting access to sensitive or regulated repositories unless that exposure is acceptable.

Risk: GitClassic is read-only and cannot create issues, open pull requests, modify repositories, or view GitHub Actions workflow runs and logs.

Mitigation: Use GitHub, the gh CLI, or the GitHub API for write operations and GitHub Actions workflow data.

## Reference(s):

- [GitClassic homepage](https://gitclassic.com)
- [ClawHub GitClassic skill page](https://clawhub.ai/heythisischris/skills/gitclassic)
- [ClawHub publisher profile](https://clawhub.ai/user/heythisischris)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with URL patterns and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only browsing guidance; private repositories require GitClassic PRO and GitHub OAuth authorization.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
