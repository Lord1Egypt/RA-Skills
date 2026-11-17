## Description:

Import sources into Google NotebookLM and generate user-selected learning artifacts, including podcasts, videos, reports, quizzes, flashcards, mind maps, slides, infographics, and data tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasontsaicc](https://clawhub.ai/user/jasontsaicc)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to turn URLs, YouTube videos, documents, text, audio, images, and Google Drive files into NotebookLM-generated study and presentation materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on an authenticated NotebookLM session and stores browser session state locally.

Mitigation: Use a dedicated NotebookLM or Google account when possible, protect ~/.notebooklm/storage_state.json like a password, and avoid copying it to shared or less-trusted systems.

Risk: Optional cron recovery jobs can continue polling and downloading artifacts without direct user supervision.

Mitigation: Enable recovery jobs only when unattended recovery is needed, run them as a non-root user, and keep output and status files in a private directory.

Risk: The recovery workflow uses local output paths and status files for downloads.

Mitigation: Review output directory paths before enabling recovery, keep the workspace private, and avoid running recovery against untrusted status files.

Risk: The skill requires external CLI dependencies, including notebooklm and ffmpeg.

Mitigation: Install dependencies from trusted sources, prefer pinned versions, and verify authentication with notebooklm auth check --test before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jasontsaicc/skills/notebooklm-studio)
- [Agent Skills Specification](https://agentskills.io)
- [Artifact Types](references/artifacts.md)
- [Artifact Options](references/artifact-options.md)
- [Output Contracts](references/output-contracts.md)
- [Source Types](references/source-types.md)
- [Telegram Delivery Contract](references/telegram-delivery.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON status files, and generated local artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces selected NotebookLM artifacts such as MP3, MP4, Markdown, JSON, PDF/PPTX, PNG, and CSV files; slow audio, video, and slide artifacts may be handled asynchronously.]

## Skill Version(s):

2.1.3 (source: server release evidence; artifact frontmatter says 2.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
