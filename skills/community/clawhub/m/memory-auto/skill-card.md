## Description: <br>
Automatically archives daily chat logs with keyword highlights and optional AI summaries into organized memory files without manual setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanshijun607-png](https://clawhub.ai/user/yanshijun607-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to automatically capture important daily chat highlights from local session transcripts into markdown memory files. It supports configurable keywords, paths, scheduling, and optional refinement into MEMORY.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic transcript scanning can capture sensitive local conversation content. <br>
Mitigation: Limit keywords to non-sensitive terms and review generated memory files after each archive run. <br>
Risk: Default or configured keywords can match passwords, tokens, keys, and secrets. <br>
Mitigation: Remove password, token, key, and secret-style terms from the configured keyword list before enabling the skill. <br>
Risk: Optional refinement may send memory content to the configured model provider if enabled. <br>
Mitigation: Keep refinement disabled unless the configured model destination and data handling are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanshijun607-png/memory-auto) <br>
- [Public README](artifact/PUBLIC-README.md) <br>
- [Configuration guide](artifact/CONFIGURATION.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown files, configuration snippets, and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily memory logs and optional MEMORY.md updates in the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
