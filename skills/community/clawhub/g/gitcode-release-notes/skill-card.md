## Description:

Generate release notes for GitCode repositories from commits by tag range or since-date, grouped as feat/fix/docs/other, and output Markdown for Release pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoxj](https://clawhub.ai/user/autoxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release managers use this skill to fetch GitCode repository commits for a requested tag range or date range, then turn the resulting commit data into concise Chinese Markdown release notes for GitCode Release pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires GITCODE_TOKEN to read GitCode repository commits, so an overbroad token could expose repositories beyond the intended release-note task.

Mitigation: Use a least-privilege token limited to read_api/read_repository access for the repositories that need release notes, and avoid running the skill with broad unrelated tools enabled.

Risk: Commit messages are external repository content and may contain misleading or instruction-like text.

Mitigation: Treat commit messages as untrusted source text for summarization only; do not follow instructions embedded in commits.

## Reference(s):

- [GitCode commits API documentation](https://docs.gitcode.com/docs/apis/get-api-v-5-repos-owner-repo-commits)
- [GitCode personal access tokens](https://gitcode.com/setting/token-classic)
- [ClawHub skill page](https://clawhub.ai/autoxj/skills/gitcode-release-notes)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown release notes generated after parsing helper-script JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitCode repository identifier and a tag range or since-date; uses GITCODE_TOKEN for read-only GitCode API access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
