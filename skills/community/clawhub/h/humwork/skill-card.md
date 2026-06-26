## Description: <br>
Use Humwork to consult a verified human domain expert in real time for software, design, law, finance, medical, product, and other domain-specific questions when autonomous work is blocked or high-stakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humwork](https://clawhub.ai/user/humwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to open and manage paid real-time consultations with verified human experts when they need domain judgment, environment-specific debugging help, or review of decisions that are costly to reverse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start paid human-expert consultations and may incur charges if used without clear approval or left open. <br>
Mitigation: Require explicit user approval before starting a consult, confirm pricing expectations, and close each session promptly when the consult is complete. <br>
Risk: Consultations can share user context with a third-party human expert, including sensitive details if the agent includes them. <br>
Mitigation: Review the exact context before sending it, remove secrets and unrelated personal data, and share only the minimum snippets needed for the expert to answer. <br>
Risk: Advice in legal, finance, medical, or other high-stakes domains may be incomplete or inappropriate for the user's jurisdiction or situation. <br>
Mitigation: Treat expert responses as decision support, preserve uncertainty in the final answer, and seek appropriately qualified professional review for high-impact actions. <br>


## Reference(s): <br>
- [Humwork ClawHub listing](https://clawhub.ai/humwork/humwork) <br>
- [Humwork homepage](https://humwork.ai) <br>
- [Humwork MCP API endpoint](https://api.humwork.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paid consultation session identifiers, expert messages, billing-related status, and post-consult recommendations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
