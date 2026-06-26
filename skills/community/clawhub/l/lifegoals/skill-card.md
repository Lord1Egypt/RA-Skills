## Description: <br>
Lifegoals helps users define goals, break them into milestones, and track progress step by step from a local command-line workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual users use Lifegoals to record personal goals, break them into milestones, review progress, and export or search local goal history from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Goal text and activity history are stored in plaintext on the local filesystem. <br>
Mitigation: Avoid entering secrets or highly sensitive personal details, inspect the Bash script before putting it on PATH, and delete ~/.local/share/lifegoals when the retained history is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text terminal output with optional JSON, CSV, or text export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores command history under ~/.local/share/lifegoals by default.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
