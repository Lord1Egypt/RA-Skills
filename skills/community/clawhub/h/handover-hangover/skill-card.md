## Description: <br>
Seamless model handoff for OpenClaw agents that preserves continuity when the gateway switches to a fallback model mid-session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tensusds](https://clawhub.ai/user/tensusds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve task continuity when OpenClaw switches models during a session. It records handoff notes, checks for pending handoffs, and helps the incoming model recover context before continuing work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Handoff notes may contain task names, file paths, git status, or other workspace context. <br>
Mitigation: Review or delete memory/handoff-note*.md in sensitive workspaces and avoid recording secrets in handoff notes. <br>
Risk: The optional integration installer enables a persistent local OpenClaw hook. <br>
Mitigation: Run the installer only when automatic handoff continuity is desired, and use the included status script to confirm hook state. <br>


## Reference(s): <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown handoff notes, local state files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes handoff state under memory/ and can optionally install a local OpenClaw hook.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
