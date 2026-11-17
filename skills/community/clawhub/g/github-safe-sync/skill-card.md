## Description:

Inspect, trigger, and clean up GitHub mirror repositories that use a safe-sync GitHub Actions workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grey0758](https://clawhub.ai/user/grey0758)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect GitHub mirror repository health, trigger safe-sync workflows, audit sync artifacts, and clean up false-positive force-push issues or stale backup branches after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository write commands can close force-push issues or delete backup branches in the wrong repository if scoped incorrectly.

Mitigation: Use a GitHub token limited to the target repository, run status first, pass explicit owner/repo and branch values, and preview delete-backups with --dry-run.

Risk: Closing force-push alerts can hide a real upstream history rewrite if the alert was not actually a false positive.

Mitigation: Manually confirm the alert is false, verify the mirror workflow is healthy, and re-run status after each write operation.

## Reference(s):

- [GitHub API root used by the sync helper](https://api.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GITHUB_TOKEN scoped to the target repository for GitHub API operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
