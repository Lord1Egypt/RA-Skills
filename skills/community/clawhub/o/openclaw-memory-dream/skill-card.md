## Description: <br>
Auto-consolidates agent memory files after sessions by using an LLM to prune stale context, resolve contradictions, tighten remaining memory, and support persistent channels through session-gap detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mitchelldavis44](https://clawhub.ai/user/mitchelldavis44) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Memory Dream to keep persistent agent memory files concise and current across repeated sessions. It is most relevant for OpenClaw workspaces where automatic capture of corrections, preferences, decisions, and memory consolidation is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically capture conversation details and stage memory-worthy signals from agent turns. <br>
Mitigation: Use it only in workspaces where automatic capture is acceptable, consider setting enableCapture to false, and avoid sensitive sessions unless disclosure and review controls are in place. <br>
Risk: The skill reads recent transcript and summary data to inform memory consolidation. <br>
Mitigation: Avoid using it with secrets or sensitive personal or business data, and keep transcript retention expectations clear for affected users. <br>
Risk: The skill can rewrite configured memory files in the workspace. <br>
Mitigation: Keep memoryFiles narrowly scoped, keep memory files under version control, and review diffs after consolidation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mitchelldavis44/openclaw-memory-dream) <br>
- [Publisher profile](https://clawhub.ai/user/mitchelldavis44) <br>
- [README](artifact/README.md) <br>
- [Plugin metadata](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown memory files, JSON status output, and configuration fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs automatically in the OpenClaw agent runtime and may rewrite configured workspace memory files.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
