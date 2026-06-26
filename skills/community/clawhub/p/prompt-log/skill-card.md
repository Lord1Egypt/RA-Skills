## Description: <br>
Extract conversation transcripts from AI coding session logs (Clawdbot, Claude Code, Codex). Use when asked to export prompt history, session logs, or transcripts from .jsonl session files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesash](https://clawhub.ai/user/thesash) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to export readable Markdown transcripts from local AI coding session logs, with optional time filters and a custom output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated transcripts may contain sensitive local AI session history. <br>
Mitigation: Treat transcript files as sensitive, avoid committing .prompt-log or transcript files to shared repositories, and choose an explicit protected output path when needed. <br>
Risk: Running a separately obtained extractor could differ from the reviewed artifact. <br>
Mitigation: Inspect any separately obtained extract.sh before running it. <br>


## Reference(s): <br>
- [Prompt Log on ClawHub](https://clawhub.ai/thesash/prompt-log) <br>
- [thesash publisher profile](https://clawhub.ai/user/thesash) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown transcript written to a local file, with shell command guidance for running the extractor.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output path is .prompt-log/YYYY-MM-DD-HHMMSS.md unless an explicit output path is provided.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
