## Description: <br>
Provides macOS screenshot and basic screen recording guidance using native screencapture commands for personal capture workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual macOS users and developers use this skill to generate shell-command guidance for full-screen, region, and window screenshots, plus basic screen recordings for bug reports, documentation, and content capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screen capture or recording can include sensitive on-screen information. <br>
Mitigation: Use only for explicit capture tasks, close or mask sensitive windows, prefer region or window capture over full-screen capture, and review files before sharing. <br>
Risk: Broad trigger language could lead to capture guidance outside a clearly intended screenshot or recording task. <br>
Mitigation: Require explicit user confirmation before running capture or recording commands and avoid automatic invocation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/mac-node-snapshot-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with bash command examples and JSON-style result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create local PNG screenshots, MOV screen recordings, and logs on macOS.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
