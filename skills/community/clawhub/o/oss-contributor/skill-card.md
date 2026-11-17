## Description:

Discover and resolve open source GitHub issues across community repositories during idle time by finding suitable issues, forking repositories, implementing fixes, and opening pull requests on the user's behalf.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kbo4sho](https://clawhub.ai/user/kbo4sho)

### License/Terms of Use:


## Use Case:

Developers and maintainers use this skill to find approachable open source issues, prepare fixes, and submit pull requests with activity logging and optional notifications. It is intended for community contribution workflows where the user is comfortable granting GitHub access and reviewing automated actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish code and pull requests under the user's GitHub identity.

Mitigation: Use a narrowly scoped, revocable GitHub token and review the selected issues, code changes, and PR body before allowing submission.

Risk: Automated modes can bypass interactive review.

Mitigation: Avoid --auto, --yes, heartbeat, or cron use until the workflow and generated PR content have been reviewed.

Risk: Credential handling is identified as unsafe in the security evidence, including token reads, token-prefix logging, and token-in-URL cloning.

Mitigation: Fix credential handling before unattended use and avoid exposing token values in logs, command history, remotes, or cloned repository URLs.

## Reference(s):

- [OSS Contributor ClawHub page](https://clawhub.ai/kbo4sho/skills/oss-contributor)
- [Publisher profile](https://clawhub.ai/user/kbo4sho)
- [OpenClaw](https://openclaw.ai)
- [GitHub REST API user endpoint](https://api.github.com/user)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status tables, summaries, PR links, shell command snippets, code changes, commits, and pull request body text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create forks, branches, commits, pull requests, local activity logs, and configured notifications.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
