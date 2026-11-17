## Description:

Automates Kuaipu system login, CAPTCHA recognition, automated browser operations, and approval workflow queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chldong](https://clawhub.ai/user/chldong)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or operators with authorized Kuaipu accounts use this skill to automate login, preserve session state, inspect business reminder lists, and identify current approvers for pending workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Kuaipu credentials and stores login session data plus page captures locally.

Mitigation: Run it with a least-privileged Kuaipu account, keep the .env and tmp directory private, and delete session, HTML, screenshot, and text artifacts after use.

Risk: Automatic dependency or browser driver downloads can introduce supply-chain or environment drift.

Mitigation: Prefer pinned dependencies and a pre-provisioned Chrome driver, and review the installed packages before using the skill in a managed environment.

Risk: Saved HTML, screenshots, and extracted approval text may contain business-sensitive workflow data.

Mitigation: Store generated artifacts only in protected local paths and avoid sharing them unless they have been reviewed and sanitized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chldong/skills/kuaipu-skill)
- [Publisher profile](https://clawhub.ai/user/chldong)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Command-line text output with local session, HTML, screenshot, and text artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Kuaipu URL, username, and password in a local .env file; browser automation output depends on the target Kuaipu instance and page state.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter says 0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
