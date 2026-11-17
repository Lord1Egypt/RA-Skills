## Description:

Automates publishing Weitoutiao posts to Toutiao using Playwright and a local or headless Chrome session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chellen021](https://clawhub.ai/user/chellen021)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to publish Toutiao micro-posts from command-line content or a local text file, optionally with an image, through an authenticated browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public content through an authenticated Toutiao browser session without a final approval step.

Mitigation: Review the complete post text before execution and use a dedicated Chrome profile for publishing.

Risk: Remote debugging on the local Chrome profile can expose logged-in browser state while it remains enabled.

Mitigation: Close unrelated tabs and disable Chrome remote debugging after use.

Risk: Installing dependencies system-wide can affect the host Python environment.

Mitigation: Install Playwright in a virtual environment with pinned dependencies instead of using a system-wide pip command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chellen021/skills/personal-toutiao-pub)
- [Toutiao publisher console](https://mp.toutiao.com/profile_v4/weitoutiao/publish?from=toutiao_pc)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and Python script behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write success or error screenshots to the user's Desktop.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
