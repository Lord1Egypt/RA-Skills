## Description:

Detects git forge (GitHub/GitLab/Bitbucket) and maps CLI commands cross-platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers writing workflows or skills for hosted Git repositories use this command reference to choose equivalent forge-specific commands for GitHub, GitLab, and Bitbucket. It is intended for issue, pull request or merge request, review, discussion, and CI/CD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags authenticated GitHub discussion searches and changes as broader than the stated command-mapping purpose; scan coverage is also incomplete because two referenced paths were missing.

Mitigation: Review discussion commands and verify the target repository, intended action, and authentication before running them; inspect the missing paths or obtain a complete scan before relying on scanner coverage.

## Reference(s):

- [Complete Command Mapping](modules/command-mapping.md)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown command reference with tables and inline shell and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform support varies by operation; Bitbucket examples use its REST API or web interface, and discussion operations are GitHub-only. Authenticated operations depend on provider credentials and configuration.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
