## Description:

Complete API access for Google NotebookLM that helps agents create notebooks, add sources, chat with content, generate artifacts, and download results in multiple formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmanchu](https://clawhub.ai/user/lmanchu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate NotebookLM workflows: creating notebooks, importing sources, querying notebook content, generating audio/video/reports/quizzes/flashcards/mind maps/slide decks/infographics/data tables, and downloading outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to use a Google account, create notebooks, upload local files or URLs, and change language settings.

Mitigation: Use a dedicated virtual environment and least-privileged Google account, and require confirmation before uploads, notebook creation, or account-level setting changes.

Risk: The skill can install or update external notebooklm-py code and its own agent skill wrapper.

Mitigation: Pin and verify the CLI version, avoid installing from an unpinned main branch, and require confirmation before running `notebooklm skill install`.

Risk: CI or multi-agent use can expose Google authentication material or mix notebook context between concurrent agents.

Mitigation: Avoid CI secrets unless necessary, isolate `NOTEBOOKLM_HOME` per account or agent, and prefer explicit notebook IDs over shared context.

Risk: Long-running generation, background agents, and downloads may write files or continue actions after the main conversation moves on.

Mitigation: Require confirmation before spawning background agents or downloading files, and record artifact and notebook IDs for later review.

## Reference(s):

- [NotebookLM API skill page](https://clawhub.ai/lmanchu/skills/notebooklm-api)
- [Publisher profile: lmanchu](https://clawhub.ai/user/lmanchu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide workflows that create, generate, wait for, and download NotebookLM artifacts through the notebooklm-py CLI.]

## Skill Version(s):

0.3.2 (source: server release metadata and artifact comment)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
