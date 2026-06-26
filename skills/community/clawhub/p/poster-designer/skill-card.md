## Description: <br>
Creates professional posters and visual designs with AI image generation for events, product showcases, announcements, and social media graphics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andylikescodes](https://clawhub.ai/user/andylikescodes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, marketers, and developers use this skill to generate poster concepts and production assets for events, products, announcements, sales, and social media campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The composition helper can turn poster text or file paths into shell command execution on the user's machine. <br>
Mitigation: Use only trusted poster text and trusted file paths, and avoid the composition helper until it calls ImageMagick with argument arrays or uses a safe image library. <br>
Risk: Poster prompts, private images, or sensitive marketing details may be sent to Gemini during generation. <br>
Mitigation: Do not submit confidential content unless that use is approved, and treat prompts and reference images as data shared with the external image-generation service. <br>
Risk: The skill requires a Gemini API key. <br>
Mitigation: Store the key in environment variables or managed secret storage, and do not commit or share real credentials in .env files. <br>


## Reference(s): <br>
- [Poster Designer Skill Page](https://clawhub.ai/andylikescodes/poster-designer) <br>
- [Gemini Image Generation API Reference](references/api-docs.md) <br>
- [Poster Templates Reference](references/templates.md) <br>
- [Rate Limiting Configuration](references/rate-limiting.md) <br>
- [Job Queue System for Image Generation](references/queue-system.md) <br>
- [Google AI Studio API Key Page](https://makersuite.google.com/app/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus generated PNG image files, optional HTML composition files, and optional JSON metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key and may write generated poster assets to local output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
