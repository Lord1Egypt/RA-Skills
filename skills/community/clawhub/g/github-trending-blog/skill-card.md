## Description:

Automates a GitHub Trending content workflow that collects repository signals, summarizes project details, generates developer-style knowledge cards, and drafts WeChat-ready technical blog articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Technical bloggers, independent developers, and newsletter authors use this skill to monitor open source trends and turn selected GitHub repositories into summaries, social knowledge-card assets, and long-form Markdown blog drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell command templates could allow crafted inputs or repository content to execute commands.

Mitigation: Review and harden command templates before use, quote or validate all user-controlled values, and avoid running the workflow on untrusted repository content without isolation.

Risk: The workflow summarizes remote repository content and turns it into public-facing blog drafts, which can propagate misleading or injected content.

Mitigation: Manually review source summaries, generated cards, and Markdown drafts before publication, especially when content comes from unfamiliar repositories.

Risk: The workflow writes generated drafts and outputs to /tmp paths.

Mitigation: Confirm output paths before execution and avoid placing sensitive source material or credentials in generated draft files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON-like workflow outputs, and generated draft or image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce repository summaries, PNG knowledge-card paths, and Markdown blog draft paths under /tmp.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
