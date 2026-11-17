## Description:

Organizes an agent's local knowledge with PARA folders, curated memory, daily logs, searchable notes, session transcript indexing guidance, and a memory flush protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halthelobster](https://clawhub.ai/user/halthelobster)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to create a workspace-local second brain for project continuity, organized notes, daily logs, and retained decisions. It is suited to teams or individuals who want file-based memory that can be searched by an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad note indexing or whole-folder symlinks can expose secrets, credentials, private personal data, regulated data, or confidential material to agent memory search.

Mitigation: Link only vetted folders, exclude sensitive files before indexing, and review the searchable memory scope before enabling the setup.

Risk: Session transcript indexing can retain more personal or confidential conversation history than intended.

Mitigation: Enable transcript indexing only in workspaces where long-term memory is appropriate, prefer concise summaries over full conversations, and maintain a process to review and delete memory files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halthelobster/skills/para-second-brain)
- [Publisher profile](https://clawhub.ai/user/halthelobster)
- [PARA methodology by Tiago Forte](https://fortelabs.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and reusable Markdown templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file-organization guidance and setup commands; users should review memory scope before indexing notes or session transcripts.]

## Skill Version(s):

2.0.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
