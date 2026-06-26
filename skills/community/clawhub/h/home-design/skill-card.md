## Description: <br>
Home Design helps generate renovation design plans, room rendering prompts, and draft construction documents from floor-plan and household requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yqrpaul](https://clawhub.ai/user/yqrpaul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and design assistants use this skill to turn floor-plan details and household requirements into renovation analysis, layout recommendations, room prompt files, draft construction documents, material lists, and budget guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Construction, wiring, plumbing, structural, or material outputs may be incomplete or unsuitable for a real property. <br>
Mitigation: Treat generated plans as drafts and have qualified local professionals review them before buying materials or starting work. <br>
Risk: Floor plans, addresses, household details, and personal renovation requirements can expose private information. <br>
Mitigation: Redact addresses and identifying household details from floor plans and prompts before using the skill or third-party image services. <br>
Risk: Image-generation backends may require API keys or service accounts. <br>
Mitigation: Keep API-key configuration files private, exclude them from version control, and review third-party image-service privacy terms before uploading plans or prompts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yqrpaul/home-design) <br>
- [README](README.md) <br>
- [Effects Guide](EFFECTS_GUIDE.md) <br>
- [Stable Diffusion Install Guide](INSTALL_SD.md) <br>
- [Construction Standards](references/construction.md) <br>
- [Ergonomics Reference](references/ergonomics.md) <br>
- [Materials Guide](references/materials.md) <br>
- [Style Guide](references/style_guide.md) <br>
- [LiblibAI](https://www.liblib.ai/) <br>
- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and instructions, JSON prompt or material files, Python command examples, and image-generation configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce draft construction files and API configuration examples; rendered images depend on external or local image-generation backends.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
