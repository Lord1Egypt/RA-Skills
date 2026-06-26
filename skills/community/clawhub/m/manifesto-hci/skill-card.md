## Description: <br>
Implement "Explicit State & Continuous Consensus" HCI pattern (v3.0) to combat information entropy, prevent intent drift, and maintain a shared Manifesto source of truth across long-term interactions using Tri-Track Architecture and Git-backed state management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leozhoski](https://clawhub.ai/user/leozhoski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, planners, and other external users use this skill to keep long-running AI projects aligned around an explicit project Manifesto, local conversation logs, and Git-backed state snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records full user and assistant messages into local project history. <br>
Mitigation: Avoid secrets, regulated data, or sensitive business content unless local storage and retention are acceptable. <br>
Risk: Git commits can preserve sensitive content even after working files are edited. <br>
Mitigation: Inspect the created projects/prj_<project_id>/ directory and delete or rewrite both logs and Git history if sensitive content is captured. <br>
Risk: Project state changes are driven by explicit slash-command workflows and may persist across long-running interactions. <br>
Mitigation: Use /manifesto pause or /manifesto stop when persistent state updates are no longer intended. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/leozhoski/manifesto-hci) <br>
- [Specification](references/specification.md) <br>
- [Diff Sub-Agent Prompt](references/diff_agent_prompt.md) <br>
- [Manifesto Template](references/manifesto_template.md) <br>
- [Light Mode Protocol](references/light_mode_protocol.md) <br>
- [Light Mode Guide](references/light_mode_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with command snippets, JSON audit receipts, and local project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local project directories, JSONL logs, Manifesto Markdown files, and Git commits when the slash-command workflow is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
