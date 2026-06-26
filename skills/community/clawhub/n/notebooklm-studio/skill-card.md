## Description: <br>
Import sources such as URLs, YouTube videos, files, and text into Google NotebookLM, then generate selected learning artifacts including podcasts, videos, reports, quizzes, flashcards, mind maps, slides, infographics, and data tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasontsaicc](https://clawhub.ai/user/jasontsaicc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to turn source material into NotebookLM-generated study, briefing, audio, video, and presentation artifacts. The skill guides the agent through setup checks, artifact option selection, generation, local download, and optional Telegram delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local Google NotebookLM session file that can grant account access if exposed. <br>
Mitigation: Treat ~/.notebooklm/storage_state.json like a password, keep file permissions restricted, and avoid shared servers for this credential. <br>
Risk: Optional Telegram delivery may send generated artifacts to the wrong recipient if the chat ID is incorrect. <br>
Mitigation: Confirm the Telegram chat ID before delivery and verify delivery status for each artifact. <br>
Risk: Optional recovery polling can continue checking and downloading pending artifacts in the background. <br>
Mitigation: Enable the recovery cron only when background polling is intended, and review pending delivery-status.json files. <br>
Risk: The workflow depends on an external notebooklm-py CLI dependency and authenticated access to Google NotebookLM. <br>
Mitigation: Install only from trusted sources, run the auth precheck before generation, and stop if the session check fails. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jasontsaicc/notebooklm-studio) <br>
- [Agent Skills specification](https://agentskills.io) <br>
- [Artifact Types](references/artifacts.md) <br>
- [Artifact Options Reference](references/artifact-options.md) <br>
- [Output Contracts](references/output-contracts.md) <br>
- [Supported Source Types](references/source-types.md) <br>
- [Telegram Delivery Contract](references/telegram-delivery.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated local files such as Markdown, JSON, CSV, PDF, PPTX, PNG, MP3, and MP4 artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires notebooklm CLI authentication; uses ffmpeg for audio compression; optional Telegram delivery is available in OpenClaw environments.] <br>

## Skill Version(s): <br>
2.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
