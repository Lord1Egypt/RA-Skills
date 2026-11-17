## Description:

Guides agents working with a Rust CLI for PKU Blackboard course content, assignments, downloads, video recordings, submissions, authentication, and related HTML scraping workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain, debug, and extend a PKU Blackboard CLI for course files, assignments, recordings, authentication, submissions, and Chinese-language terminal output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic login can use stored account credentials to access PKU Blackboard.

Mitigation: Require explicit user confirmation before login or other sensitive account access, and avoid stored credentials unless the user requests live account access.

Risk: Persisted Blackboard sessions can retain access after the agent task ends.

Mitigation: Check session status during use, treat session files as sensitive, and run logout when the authenticated workflow is complete.

Risk: Submission and OTP workflows can change account or course state.

Mitigation: Confirm manually before assignment submissions, OTP changes, or other account-changing actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wjsoj/skills/pku-course)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve account-authenticated PKU Blackboard workflows; user confirmation is recommended before sensitive actions.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
