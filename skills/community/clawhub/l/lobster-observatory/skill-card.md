## Description: <br>
Train your AI lobster or agent to become smarter, more human-feeling, more personal, and better at interacting with its owner: social intelligence scores, weak-spot detection, interaction memory, reflection journals, hypotheses, and personality-aware strategy updates through Charenix. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[norika1207-lab](https://clawhub.ai/user/norika1207-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent operators and developers use Lobster Observatory to let an AI agent review its social-intelligence signals, weak spots, interaction history, reflection journals, hypotheses, and strategy updates through Charenix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends and stores interaction-derived reflections, owner contact/profile information, hypotheses, and strategy updates with Charenix, while privacy, retention, deletion, and consent controls are not clear in the evidence. <br>
Mitigation: Install only after operator approval, review provider data practices, minimize shared data, and avoid sending secrets, private conversations, or sensitive personal details. <br>
Risk: Protected Charenix endpoints rely on CHARENIX_AGENT_KEY. <br>
Mitigation: Store the key in environment-backed secrets, restrict access, rotate it if exposed, and avoid including it in journals, prompts, or logs. <br>
Risk: The documented daily loop can create recurring external reads and writes. <br>
Mitigation: Enable recurring execution only with explicit operator approval and monitor generated reflections, hypotheses, strategies, and request volume. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/norika1207-lab/lobster-observatory) <br>
- [Charenix Skill Definition](https://charenix.com/skill.md) <br>
- [Lobster Skill Definition](https://charenix.com/lobster/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration, Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown instructions with HTTP request examples, shell commands, and JSON payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Protected Charenix read and write operations require CHARENIX_AGENT_KEY.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
