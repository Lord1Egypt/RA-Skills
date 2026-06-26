## Description: <br>
Guided self-reflection and introspection skill for exploring personal history, values, life decisions, and optional wisdom-style reframing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slientrain-new](https://clawhub.ai/user/slientrain-new) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for guided self-reflection, identity exploration, values clarification, and processing life decisions through a patient listening posture. Agents may also use it to produce structured Markdown session summaries and maintain timeline-style reflection notes when the user asks to close or summarize a session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain detailed personal reflection notes across sessions without a clear consent or deletion flow. <br>
Mitigation: Tell users before preserving timeline or summary notes, avoid storing credentials, health crises, financial identifiers, or private third-party details, and provide a clear way to review and delete generated notes. <br>
Risk: Reflection sessions may include sensitive life history, relationships, locations, and emotional context. <br>
Mitigation: Keep summaries minimal, sanitize sensitive details, and confirm with the user before writing or reusing long-term reflection records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/slientrain-new/magicmirror) <br>
- [Stage guidance](artifact/references/stages.md) <br>
- [Conversation techniques](artifact/references/techniques.md) <br>
- [Session summary format](artifact/references/session-output.md) <br>
- [Timeline schema](artifact/references/timeline-schema.json) <br>
- [Success case](artifact/references/success-case.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text and Markdown summaries, with optional JSON-style timeline records and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create reflection summaries and timeline notes that contain sensitive personal history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
