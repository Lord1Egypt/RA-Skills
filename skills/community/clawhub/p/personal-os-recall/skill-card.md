## Description:

Load context from past sessions. Three modes: temporal (what did I work on yesterday/last week), topic (semantic search across sessions and notes), and graph (visual map of session-file relationships). Every recall ends with One Thing - the single highest-leverage next action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borodich](https://clawhub.ai/user/borodich)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Recall to recover project context from prior session memory, chat logs, session state, and notes. It supports temporal, topic, and graph-based recall and ends with a concrete next action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search broad private workspace history, chat logs, session state, and notes.

Mitigation: Use it only for explicit recall requests and review returned excerpts before sharing or acting on them.

Risk: Graph mode may generate HTML that exposes sensitive session or file relationship data.

Mitigation: Review generated HTML before opening or distributing it when sensitive data may appear.

Risk: Optional global QMD installation adds persistent third-party tooling to the environment.

Mitigation: Avoid the optional global npm install unless the package has been independently trusted and pinned.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/borodich/skills/personal-os-recall)
- [Publisher Profile](https://clawhub.ai/user/borodich)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated HTML file references for graph mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local memory files, session state, workspace notes, and generated recall graph HTML.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
