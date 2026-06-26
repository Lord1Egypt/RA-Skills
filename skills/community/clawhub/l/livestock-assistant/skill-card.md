## Description: <br>
AI-powered livestock management assistant for Spanish-speaking farmers, with guidance on herd management, animal health, reproduction, genetics, nutrition, breed selection, and REST API-based herd record keeping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonygiomarxdev](https://clawhub.ai/user/antonygiomarxdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Spanish-speaking farmers, livestock operators, and developers use this skill to get livestock management guidance, consult domain references, and operate a local REST API for animal records. The assistant is intended for advisory support and record workflows, not definitive veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Livestock health guidance could be mistaken for definitive veterinary diagnosis. <br>
Mitigation: Keep health responses advisory, recommend a licensed veterinarian for emergencies or definitive diagnosis, and escalate zoonotic or urgent symptoms as the skill directs. <br>
Risk: Animal record API calls can create, update, or delete local herd records. <br>
Mitigation: Confirm the user's intent and review payloads before issuing create, update, or delete requests against the local API. <br>
Risk: AI provider API keys are required for normal assistant operation. <br>
Mitigation: Load keys from environment variables only and avoid including secrets in prompts, records, logs, or committed files. <br>


## Reference(s): <br>
- [REST API Reference](references/api.md) <br>
- [Livestock Breed Reference](references/breeds.md) <br>
- [Livestock Disease Reference](references/diseases.md) <br>
- [Nutrition & Forage Reference](references/nutrition.md) <br>
- [Project homepage](https://github.com/antonygiomarxdev/openclaw-livestock-assistant) <br>
- [ClawHub release page](https://clawhub.ai/antonygiomarxdev/livestock-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are expected to be in Spanish; REST API examples use localhost endpoints and provider configuration through environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
