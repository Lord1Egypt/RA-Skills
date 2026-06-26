## Description: <br>
MaskClaw provides on-device privacy protection tools for visual masking, behavior monitoring, and self-evolving privacy rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theodora-y](https://clawhub.ai/user/theodora-y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use MaskClaw to add an on-device privacy guard between agents and mobile or desktop UI workflows. It identifies and masks sensitive visual content, records user corrections, and evolves user-specific privacy rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can record detailed local behavior traces and sensitive image-derived content. <br>
Mitigation: Require explicit opt-in, disable raw OCR/content logging by default, and add retention, deletion, and encryption controls before deployment. <br>
Risk: Trace-derived prompts are sent to a local model endpoint and may contain sensitive user context. <br>
Mitigation: Keep model calls local, redact prompt inputs where possible, and review endpoint access controls before use. <br>
Risk: The evolution workflow can generate and publish active per-user rules. <br>
Mitigation: Require human approval and security review before generated rules or skills are activated. <br>


## Reference(s): <br>
- [MaskClaw ClawHub release page](https://clawhub.ai/theodora-y/maskclaw) <br>
- [MaskClaw homepage](https://github.com/your-org/maskclaw) <br>
- [Architecture](references/ARCHITECTURE.md) <br>
- [Skills API](references/SKILLS_API.md) <br>
- [RAG Schema](references/RAG_SCHEMA.md) <br>
- [Prompt Templates](references/PROMPT_TEMPLATES.md) <br>
- [Self Evolution](references/SELF_EVOLUTION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python/API examples and JSON-style result structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create masked image files, JSONL behavior traces, ChromaDB-backed rule records, and user-specific SOP or skill drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
