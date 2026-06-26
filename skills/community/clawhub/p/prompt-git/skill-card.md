## Description: <br>
Git for your prompts. Track every change, diff versions, rollback mistakes, never lose a good prompt again. All local, zero dependencies, works offline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, prompt engineers, and AI users use Prompt Git to keep local version history for text prompts, compare revisions, roll back changes, search prompt libraries, and move prompt records through JSON or Markdown export/import workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt history is persisted locally and may include sensitive prompt content. <br>
Mitigation: Avoid storing secrets unless local persistence is intended, and protect or back up the storage directory according to your environment. <br>
Risk: Importing with overwrite can replace existing prompt history without an atomic rollback path. <br>
Mitigation: Review imported JSON before use and back up important prompt history before running import --overwrite. <br>
Risk: Concurrent writes to the same local repository can corrupt prompt history. <br>
Mitigation: Avoid running multiple Prompt Git processes against the same repository at the same time. <br>


## Reference(s): <br>
- [Prompt Git on ClawHub](https://clawhub.ai/TheShadowRose/prompt-git) <br>
- [TheShadowRose ClawHub profile](https://clawhub.ai/user/TheShadowRose) <br>
- [PromptGit README](README.md) <br>
- [PromptGit Limitations](LIMITATIONS.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code references, shell command examples, JSON exports, Markdown exports, and text diffs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores prompt history locally, usually under ~/.promptgit; import/export workflows can read or write JSON and Markdown files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
