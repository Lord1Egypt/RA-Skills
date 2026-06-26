## Description: <br>
Parse raw WhatsApp exports, provided as TXT or JSON, into normalized message objects with timestamp, sender, and content fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalgojha](https://clawhub.ai/user/vishalgojha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external workflow builders use this skill to convert user-provided WhatsApp exports into schema-valid message objects before downstream extraction or analysis. It is intended for parsing only, not lead interpretation, summarization, storage, or action suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WhatsApp exports may contain sensitive personal or business information. <br>
Mitigation: Only provide chat exports that are appropriate to process, and avoid using the skill on data that should not leave the user's controlled workflow. <br>
Risk: Downstream skills could extract leads, summarize conversations, suggest actions, or store parsed data beyond this parser's stated boundary. <br>
Mitigation: Review or approve later skills in the chain before allowing extraction, summaries, action suggestions, or storage. <br>


## Reference(s): <br>
- [Parsed Message Array Schema](references/parsed-message-array.schema.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/vishalgojha/message-parser) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Validated JSON array of message objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each object contains timestamp, sender, and content; additional properties are disallowed by the bundled schema.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
