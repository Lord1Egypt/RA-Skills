## Description: <br>
Visual identity discovery for AI agents: the skill guides an agent through self-reflection, image prompt definition, image generation, comparative evaluation, and an evolving visual identity file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahaaiclub](https://clawhub.ai/user/ahaaiclub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to create or evolve an AI agent's visual identity from personality files, memory, and user relationship context. It supports a quick two-image path and a fuller five-phase identity design workflow with checkpoints and scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to read personality, memory, identity, and recent conversation context, which may include private or sensitive details. <br>
Mitigation: Remove secrets and private details before running the workflow, and only install it where using those files for visual identity creation is acceptable. <br>
Risk: Generated prompts may pass personality or relationship details to external image generation tools. <br>
Mitigation: Review generated prompts before sending them to any external image service. <br>
Risk: The workflow writes a persistent visual identity file under ~/.openclaw/identity/visual-identity.md. <br>
Mitigation: Review the saved identity file after creation and remove any details that should not persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahaaiclub/knowyourself) <br>
- [AHA AI](https://ahaai.ai) <br>
- [Evaluation Frameworks Reference](references/evaluation-frameworks.md) <br>
- [Visual Identity File Template](references/identity-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance, image-generation prompts, scoring tables, and a visual-identity.md file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose image-generation prompts and persistent identity documentation; image creation depends on the agent's available image generation tool.] <br>

## Skill Version(s): <br>
1.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
