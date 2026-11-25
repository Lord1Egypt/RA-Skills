## Description:

Creates a structured handoff at the end of a coding session and checks its claims against repository state when work resumes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use the skill to freeze task status, file claims, and next actions at the end of a session, then check what still holds when work resumes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions use a remote Git repository, and the security scan was partial with unresolved local path references.

Mitigation: Review and trust the project source and install instructions before installing.

Risk: A verify command stored in a handoff may be untrusted and could run code.

Mitigation: Leave verification disabled by default; use --run-verify only for a handoff you froze yourself or have reviewed, and retain the timeout.

## Reference(s):

- [Handoff Reconciler project on GitHub](https://github.com/RakTikoo/handoff-reconciler)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown handoff and text drift report with a corrected resume pack]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports claim status as MATCH, DRIFT, BROKEN, or NOT-RUN.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
