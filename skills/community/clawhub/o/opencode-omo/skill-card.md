## Description: <br>
Turn coding requests into completed work. Plan with Prometheus, execute with Atlas, and iterate with Sisyphus in OpenCode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IISweetHeartII](https://clawhub.ai/user/IISweetHeartII) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run coding tasks through OpenCode with Oh-My-OpenCode workflows, including one-shot implementation, planning with Prometheus, execution with Atlas, and iteration with Sisyphus. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-directed coding workflows can produce incorrect or unwanted code changes. <br>
Mitigation: Use the skill in a git-controlled project and review, test, and approve agent-made changes before accepting them. <br>
Risk: The artifact references local helper scripts that were not included in the reviewed artifact. <br>
Mitigation: Inspect any local helper scripts before running them and verify that they match the documented OpenCode workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IISweetHeartII/opencode-omo) <br>
- [Project homepage](https://github.com/IISweetHeartII/opencode-omo) <br>
- [agent-selfie integration](https://clawhub.org/skills/agent-selfie) <br>
- [gemini-image-gen integration](https://clawhub.org/skills/gemini-image-gen) <br>
- [agentgram integration](https://clawhub.org/skills/agentgram) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes OpenCode, git, and ClawHub CLIs are installed when following commands.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
