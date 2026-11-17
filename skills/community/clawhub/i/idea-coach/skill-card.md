## Description:

AI-powered idea/problem/challenge manager with GitHub integration. Captures, categorizes, reviews, and helps ship ideas to repos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[udiedrichsen](https://clawhub.ai/user/udiedrichsen)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to capture ideas, problems, and challenges, review them on adaptive schedules, and move ready work into GitHub repositories or issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored idea content is local plaintext data and may contain sensitive personal or work information.

Mitigation: Avoid storing secrets or sensitive material, and review local idea records before sharing or syncing them elsewhere.

Risk: GitHub commands can act through the user's authenticated gh account and may create repositories or issues containing idea content.

Mitigation: Use GitHub commands only intentionally, review content before syncing, and prefer private repositories unless public disclosure is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/udiedrichsen/skills/idea-coach)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-style command output with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local idea records and, when explicitly invoked, use the authenticated GitHub CLI to create or update repositories and issues.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
