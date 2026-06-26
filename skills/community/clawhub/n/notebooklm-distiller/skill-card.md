## Description: <br>
NotebookLM Distiller batch-extracts knowledge from Google NotebookLM into Obsidian, with support for Q&A generation, structured summaries, glossary extraction, web research sessions, and direct Markdown persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anchor-jevons](https://clawhub.ai/user/anchor-jevons) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn NotebookLM notebooks or research sessions into structured Obsidian notes, quiz questions, answer evaluations, and saved Markdown records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an authenticated NotebookLM session and create NotebookLM resources. <br>
Mitigation: Confirm the Google account, target notebook or research topic, and whether NotebookLM writeback is intended before running side-effecting commands. <br>
Risk: The skill can write or overwrite Markdown notes in a selected vault. <br>
Mitigation: Confirm the vault directory and exact output path before execution, and avoid sensitive content until path containment and overwrite safeguards are reviewed. <br>


## Reference(s): <br>
- [NotebookLM Distiller on ClawHub](https://clawhub.ai/anchor-jevons/notebooklm-distiller) <br>
- [OpenClaw](https://github.com/openclaw) <br>
- [OpenClaw DeepReader](https://github.com/astonysh/OpenClaw-DeepReeder) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter, JSON quiz and evaluation payloads, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write files into a selected vault and can optionally write distilled content back into NotebookLM.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
