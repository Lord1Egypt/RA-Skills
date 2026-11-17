## Description:

Notebooklm helps agents use the unofficial notebooklm-py interface for Google NotebookLM notebook management, source ingestion, content generation, downloads, and research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content teams use this skill to create and manage NotebookLM notebooks, add web or local sources, generate study and presentation materials, and download produced artifacts. It is intended for agent-assisted workflows that call the notebooklm-py CLI or Python API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install an unpinned unofficial NotebookLM package and browser dependencies.

Mitigation: Use a dedicated virtual environment, review and pin notebooklm-py and browser dependency versions, and approve package installation before agent execution.

Risk: NotebookLM source ingestion may upload local files, URLs, audio, video, images, or other content to Google/NotebookLM.

Mitigation: Treat uploads as external data sharing and require explicit approval for the exact files, URLs, and notebook actions before adding sources.

Risk: Notebook management commands include destructive actions such as deleting notebooks.

Mitigation: Require explicit user confirmation before notebook deletion or any other irreversible NotebookLM action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antonia-sz/skills/notebooklm-py)
- [Publisher profile](https://clawhub.ai/user/antonia-sz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or download NotebookLM-generated files such as audio, video, slides, quizzes, flashcards, mind maps, data tables, reports, and images when the user authorizes the underlying NotebookLM actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
