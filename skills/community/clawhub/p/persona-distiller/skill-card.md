## Description: <br>
Distills chat records into structured persona JSON profiles and activation snippets that help an agent respond in the represented person's style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcduann](https://clawhub.ai/user/jcduann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to analyze local chat exports, generate persona profiles, and activate a chosen speaking style in an AI conversation. It is intended for consent-based, local persona profiling and manual review of generated snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and manages profiles derived from private chat records. <br>
Mitigation: Use it only with consent from represented people and keep chat extracts and .persona.json files private. <br>
Risk: Automatic persona loading can apply a persona when a name is mentioned. <br>
Mitigation: Prefer explicit persona activation and review the selected persona before injecting its snippet into an agent session. <br>
Risk: The Windows clipboard export path can execute crafted persona text. <br>
Mitigation: Avoid clipboard export for persona files you did not create and trust; inspect snippets before exporting or activating them. <br>


## Reference(s): <br>
- [Persona Distiller on ClawHub](https://clawhub.ai/jcduann/persona-distiller) <br>
- [Persona Distillation Guide](references/distillation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON persona files, text activation snippets, and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated persona files include linguistic, vocabulary, tone, behavior, and system_prompt_snippet fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
