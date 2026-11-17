## Description:

Autonomous GitHub contribution agent using the Architect-Builder pattern. Buck handles git and network I/O while subagents handle focused cognitive work for scouting issues, implementing fixes, and submitting pull requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahajahmed010](https://clawhub.ai/user/wahajahmed010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to identify suitable GitHub issues, prepare targeted fixes, validate changes, and submit pull requests with AI assistance disclosure. It is intended for controlled open-source contribution workflows where the user is responsible for actions taken under their GitHub identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub credentials may be exposed or overused by automation.

Mitigation: Use a fine-grained token with the smallest possible repository permissions, avoid storing the token in skill configuration, rotate it regularly, and revoke it immediately if misuse is suspected.

Risk: The nightly runner performs shell-based GitHub and git operations that can fork, push, and create public pull requests.

Mitigation: Do not run the nightly runner until shell command construction and token handling are fixed; require manual review before any fork, push, or pull request is made.

Risk: Autonomous fixes can introduce low-quality or incorrect changes under the user's GitHub identity.

Mitigation: Start in dry-run or approval-first mode, keep complexity low, require tests where available, and monitor rejection rates before enabling fuller automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wahajahmed010/skills/open-source-contributor)
- [Publisher Profile](https://clawhub.ai/user/wahajahmed010)
- [ClawHub README Link](https://clawhub.ai/wahajahmed010/open-source-contributor)
- [GitHub Repository Link](https://github.com/wahajahmed010/open-source-contributor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON status data, shell commands, and code diffs or file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create commits, branches, pull requests, logs, reports, and local configuration when run with GitHub credentials.]

## Skill Version(s):

3.0.0 (source: server release metadata and install.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
