## Description: <br>
Create temporary handoff docs and propose/apply permanent knowledge updates in a shared Obsidian vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RadonX](https://clawhub.ai/user/RadonX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create temporary project handoff notes, load recent handoffs, and propose permanent knowledge updates in a shared Obsidian-style vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared handoff or work-log files may capture secrets, credentials, or sensitive command output. <br>
Mitigation: Review proposed content before confirming writes and keep secrets or sensitive command output out of handoff and work-log files. <br>
Risk: The agent may prepare writes to an unexpected shared vault path or project folder. <br>
Mitigation: Require the agent to state resolved absolute paths before writes and proceed only after explicit user confirmation. <br>
Risk: Permanent knowledge updates may add incorrect or stale long-term guidance. <br>
Mitigation: Review the proposed patch before applying permanent documentation changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RadonX/handoff) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown handoff documents, proposed patches, summaries, and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include YAML frontmatter, Obsidian-friendly links, and confirmation-gated file updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
