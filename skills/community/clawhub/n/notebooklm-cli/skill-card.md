## Description: <br>
Comprehensive CLI for Google NotebookLM including notebooks, sources, audio podcasts, reports, quizzes, flashcards, mind maps, slides, infographics, videos, and data tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oconnell-carl](https://clawhub.ai/user/oconnell-carl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to manage Google NotebookLM notebooks, sources, authentication profiles, generated artifacts, and content-generation workflows from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The login flow reads authenticated Chrome session cookies for NotebookLM without enough detail about consent, storage, or deletion. <br>
Mitigation: Use nlm login only after verifying where cookies are stored and how to delete them; prefer an isolated Chrome profile or test Google account. <br>
Risk: Confirmed commands can create, sync, or delete NotebookLM sources and generated artifacts. <br>
Mitigation: Review the active profile, notebook ID, source ID, and artifact ID before running commands that require --confirm or -y. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide commands that produce NotebookLM artifacts, JSON output, quiet ID lists, rich tables, or generated AI documentation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
