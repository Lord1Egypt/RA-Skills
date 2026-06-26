## Description: <br>
Search local OpenClaw session and transcript history with the openclaw-session-grep CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to search local OpenClaw session and transcript history when debugging prior conversations, tool usage, cron behavior, panel failures, historical errors, or expensive runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evidence security summary says the available scan context did not provide a concrete reason to block installation, while advising review of the actual skill files before installing. <br>
Mitigation: Review the artifact skill file and requested local binary path before installation, especially setup steps, filesystem access, network calls, credentials, and persistent behavior. <br>
Risk: The skill caveat says broad search targets can include non-transcript files and produce noisy or unintended local search results. <br>
Mitigation: Use the skill for session and transcript discovery first, and narrow searches with path, session, channel, time-window, or tool-only filters when results are too broad. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pfrederiksen/openclaw-session-grep) <br>
- [Publisher profile](https://clawhub.ai/user/pfrederiksen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the local ocgrep wrapper at /root/.openclaw/workspace/tools/ocgrep and may return file and line references from local session history.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
