## Description:

AI-powered livestock management assistant for Spanish-speaking farmers that provides guidance on herd management, animal health, reproduction, genetics, nutrition, breed selection, and REST API herd record-keeping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonygiomarxdev](https://clawhub.ai/user/antonygiomarxdev)

### License/Terms of Use:

MIT-0

## Use Case:

External farmers, livestock operators, and developers use this skill for Spanish-language livestock management guidance and for operating a local REST API to record animals, health events, reproduction, nutrition, and herd status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests multiple AI-provider credentials and executable installation authority beyond what its packaged files fully justify.

Mitigation: Provide only the intended provider key, run in a least-privileged environment, and review supplied server/runtime files before deployment.

Risk: Livestock health guidance may be mistaken for definitive veterinary diagnosis or emergency treatment instructions.

Mitigation: Keep the built-in requirement to avoid definitive diagnoses and route emergencies, zoonotic disease concerns, and legally notifiable diseases to licensed veterinarians or authorities.

## Reference(s):

- [Livestock Assistant on ClawHub](https://clawhub.ai/antonygiomarxdev/skills/livestock-assistant)
- [Project homepage](https://github.com/antonygiomarxdev/openclaw-livestock-assistant)
- [REST API Reference](references/api.md)
- [Livestock Breed Reference](references/breeds.md)
- [Livestock Disease Reference](references/diseases.md)
- [Nutrition & Forage Reference](references/nutrition.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Spanish Markdown or plain text with optional shell, HTTP, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should avoid definitive disease diagnosis, flag zoonotic and emergency cases, and direct users to licensed veterinary support when appropriate.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
