## Description:

Batch clones or updates GitLab group projects, checks out key branches, preserves group structure, and generates an Excel index of project and branch metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pangfan](https://clawhub.ai/user/pangfan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to clone or update many GitLab repositories from groups, subgroups, or direct project paths while keeping local folders aligned with GitLab structure. It also creates an Excel index that summarizes project metadata, checked-out branches, commit times, and repository links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitLab personal access tokens are used for API access and HTTPS cloning, and mishandling could expose repository credentials.

Mitigation: Use a short-lived token with only read_api and read_repository scopes, run on a trusted machine, and confirm remotes do not retain embedded credentials after cloning.

Risk: TLS certificate verification is disabled for GitLab API calls, which can expose requests to interception on untrusted networks.

Mitigation: Fix GitLab certificate trust or restore TLS verification before production use, especially outside controlled internal networks.

Risk: Bulk clone and sync operations can make many local filesystem changes and may run without a global timeout by default.

Mitigation: Set an explicit local base directory, choose an appropriate worker count, and configure GITLAB_TOTAL_TIMEOUT for bounded runs.

Risk: The generated Excel workbook contains GitLab metadata supplied by remote projects and groups.

Mitigation: Treat the workbook as untrusted output, review it before sharing, and avoid opening it in high-trust contexts without normal spreadsheet precautions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pangfan/skills/gitlab-batch-cloner)
- [ClawHub publisher profile](https://clawhub.ai/user/pangfan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces cloned Git repositories under the configured local path and an Excel workbook named 01.Index.xlsx.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
