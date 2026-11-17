## Description:

Automated AI code review for GitLab Merge Requests via polling, including diff review, inline comments, and a summary note on GitLab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gotoloops](https://clawhub.ai/user/gotoloops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to automate recurring GitLab merge-request review, identify security, bug, performance, and maintainability issues, and post review comments back to GitLab.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recurring worker can post GitLab comments and notes without interactive approval.

Mitigation: Use a narrowly scoped project or group token, restrict the worker to explicit projects, require HTTPS and a trusted GitLab host, and test manually before enabling the cron worker.

Risk: Merge-request branch content can influence review instructions through project-level review prompt files.

Mitigation: Treat branch-provided prompt and policy text as untrusted data, and do not let it override trusted operating rules or credential-handling requirements.

Risk: State tracking failures can cause duplicate MR reviews and repeated GitLab comments.

Mitigation: Confirm the reviewed-MR state file is writable and that the worker records each MR immediately after posting its summary note.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gotoloops/skills/gitlab-auto-review)
- [Cron Worker Setup](references/cron-setup.md)
- [Review Guidelines](references/review-guidelines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown review comments and summary notes, JSON payloads for inline comments, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GitLab API credentials from GITLAB_URL and GITLAB_TOKEN and requires node.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
