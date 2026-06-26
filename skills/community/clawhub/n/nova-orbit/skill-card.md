## Description: <br>
Nova Orbit helps an agent run a recurring workflow for GitHub research, persistent memory, pattern reuse, self-assessment, and human-visible status updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jokerli530](https://clawhub.ai/user/jokerli530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Nova Orbit to structure autonomous research, memory recall, pattern extraction, self-improvement notes, and local status synchronization across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks the agent to maintain persistent cross-session memory, which can capture sensitive task context if used without boundaries. <br>
Mitigation: Decide what may be written to nova-mind and ByteRover before use, and avoid storing secrets or private task content. <br>
Risk: The workflow includes network calls and local status updates that may expose activity or depend on local services. <br>
Mitigation: Review configured endpoints and proxy settings before execution, and run the skill only in environments where those services are expected. <br>
Risk: The workflow references self-evolution and skill or behavior updates, which can change future agent behavior. <br>
Mitigation: Require human review before applying skill updates, behavior updates, or self-assessment recommendations. <br>
Risk: The workflow references running a local self-assessment script. <br>
Mitigation: Inspect or disable the referenced script before use, especially in shared or production environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve network calls, local status updates, persistent memory files, ByteRover curation, and self-assessment script execution when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
