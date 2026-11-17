## Description:

Helps agents organize bookmarks and research into a persistent Markdown knowledge wiki with ingest, query, relink, lint, Deep Research, and URL-level source traceability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangmengyang](https://clawhub.ai/user/zhangmengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to turn collected links and research topics into a structured personal wiki, then query and maintain it with linting and relinking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers can lead the agent to make persistent local wiki edits beyond the user's intended scope.

Mitigation: Use a dedicated, backed-up wiki folder and review proposed file changes before execution.

Risk: Deep Research and query workflows can introduce unverified or misleading source material into the wiki.

Mitigation: Approve search queries before execution and require URL-level source traceability with confidence annotations.

Risk: Periodic linting or relinking can change wiki relationships without enough explicit consent.

Mitigation: Run maintenance only when explicitly requested or clearly enabled for the configured wiki.

## Reference(s):

- [Andrej Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Karpathy Wiki Improve ClawHub listing](https://clawhub.ai/zhangmengyang/skills/karpathy-wiki-improve)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with wiki plans, source links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create persistent local wiki files within the configured wiki folder.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
