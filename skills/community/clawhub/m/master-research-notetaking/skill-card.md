## Description:

系统研究一位大师、思想家或名人的核心体系，提炼最值得学的内容并写入 Obsidian 笔记库，重点产出可复用的思维框架而非百科摘录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[realpda](https://clawhub.ai/user/realpda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to research a public figure's ideas, extract reusable mental models, and produce a structured Obsidian note with sources, contradictions, practical actions, and honest limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to use private user context and an Obsidian vault when creating research notes.

Mitigation: Confirm the exact vault path, constrain which notes may be read, and avoid sharing unrelated private notes with delegated research tasks.

Risk: The skill writes research output into an Obsidian vault, which can introduce unwanted or misleading notes if the scope is wrong.

Mitigation: Require preview-before-write and user confirmation before creating or updating vault files.

Risk: The artifact includes a shell search example for checking existing notes.

Mitigation: Replace ad hoc shell search with a safer file-search method scoped to the confirmed vault path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realpda/skills/master-research-notetaking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research note with tables, source lists, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or proposes structured Obsidian note content after a research quality checkpoint.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
