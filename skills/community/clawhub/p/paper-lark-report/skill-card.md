## Description:

Generates Chinese daily and weekly research-paper reports by retrieving arXiv papers, using an LLM to score and summarize them, and publishing the result to Feishu Wiki.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leogoat2004](https://clawhub.ai/user/leogoat2004)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, research engineers, and developer teams use this skill to automate daily and weekly monitoring of arXiv papers for a configured research direction and publish concise Chinese reports to Feishu Wiki.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu credentials may be exposed or over-permissioned because the workflow reads app credentials from OpenClaw configuration and security evidence reports unsafe credential handling.

Mitigation: Use a Feishu app whose permissions are narrowly scoped to the intended Wiki location and avoid shared logs until token-fragment logging is removed.

Risk: The security evidence reports an argument path issue that can overwrite JSON files outside the intended log directory.

Mitigation: Run save and register commands only with trusted arguments, and review file paths before scheduled execution.

Risk: Using `npx clawhub@latest` can pull an installer version that differs from the reviewed release environment.

Mitigation: Pin the installer version in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leogoat2004/skills/paper-lark-report)
- [arXiv API](https://export.arxiv.org/api/query)
- [Feishu Open API](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown report templates, JSON paper data, shell commands, and Feishu Wiki document content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily and weekly workflows are configured by research direction, arXiv limits, cron schedules, and Feishu Wiki identifiers.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
