## Description:

Comprehensive CLI for Google NotebookLM including notebooks, sources, audio podcasts, reports, quizzes, flashcards, mind maps, slides, infographics, videos, and data tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oconnell-carl](https://clawhub.ai/user/oconnell-carl)

### License/Terms of Use:


## Use Case:

Developers, researchers, analysts, and other NotebookLM users use this skill to manage notebooks and sources from the command line, generate NotebookLM artifacts, query sources, and automate research/import workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication uses active Google session credentials through browser cookie extraction.

Mitigation: Run login only on trusted machines, avoid shared environments, and verify where profiles or cookies are stored before use.

Risk: Notebook sources may include confidential Drive files, pasted text, URLs, or bulk notebook content sent to NotebookLM or Google processing.

Mitigation: Do not import sensitive material unless the user has approved that processing path and the content is appropriate for NotebookLM.

Risk: Some container setups may require privileged Chrome or Docker flags.

Mitigation: Avoid privileged container flags unless the operational impact is understood and approved.

## Reference(s):

- [Command Reference](references/commands.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Workflows](references/workflows.md)
- [ClawHub skill page](https://clawhub.ai/oconnell-carl/skills/notebooklm-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/oconnell-carl)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration instructions]

**Output Format:** [Markdown with command examples and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through NotebookLM CLI authentication, notebook/source management, content generation, chat, research, profiles, aliases, and troubleshooting.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
