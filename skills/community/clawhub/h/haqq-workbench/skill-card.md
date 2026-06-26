## Description: <br>
Haqq Workbench coordinates Haqq-related skills for Islamic and ethical content creation, verification, publishing workflows, corruption or injustice content, and skill-building workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m7madash](https://clawhub.ai/user/m7madash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to choose and sequence Haqq skills for religious or ethical content creation, claim verification, social publishing preparation, justice-focused content, memory capture, and skill publication workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route broad requests into publishing, messaging, memory, and skill-publishing workflows without clear confirmation controls. <br>
Mitigation: Require explicit user confirmation before publishing, sending messages, saving memory, uploading to ClawHub, or invoking any downstream workflow with external effects. <br>
Risk: The trigger map is broad and may select high-impact workflows from keyword matches alone. <br>
Mitigation: Treat workflow routing as advisory, ask clarifying questions when intent is ambiguous, and review selected steps before execution. <br>
Risk: Religious and factual content may be inaccurate if downstream verification fails or is skipped. <br>
Mitigation: Apply the documented double-gate checks for hadith, religious guidance, and factual claims before sharing or publishing content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/m7madash/haqq-workbench) <br>
- [Publisher Profile](https://clawhub.ai/user/m7madash) <br>
- [Skill Map](references/skill-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance and optional JSON workflow suggestions from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill routes user requests into suggested workflows and may reference publishing, messaging, memory, and skill-publishing actions that require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
