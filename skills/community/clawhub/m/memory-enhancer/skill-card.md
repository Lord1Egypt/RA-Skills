## Description: <br>
Automatically extracts structured facts from daily memory logs and maintains long-term memory summaries and stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xpneuma](https://clawhub.ai/user/xpneuma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to process daily memory logs, extract preferences, contacts, habits, and project status, and maintain structured long-term memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private daily logs are analyzed by an external model agent. <br>
Mitigation: Enable the skill only when users intentionally want those logs sent for analysis, and confirm the configured provider and model before running it. <br>
Risk: Extracted personal details are written into long-term memory files without a built-in review step. <br>
Mitigation: Add a manual review or diff approval step before committing changes to MEMORY.md and memory/stats JSON files. <br>
Risk: Hard-coded workspace paths and execution logging can expose private data or fail outside the original environment. <br>
Mitigation: Review and parameterize paths, create log directories deliberately, and avoid logging full model results or raw error stacks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xpneuma/memory-enhancer) <br>
- [Publisher profile](https://clawhub.ai/user/xpneuma) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Markdown summaries, JSON memory stats, and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates long-term memory files and logs execution status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
