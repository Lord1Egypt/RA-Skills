## Description: <br>
limtdesign helps agents turn visual creative requests into structured AI image-generation prompts for posters, banners, product imagery, social media graphics, concept art, branding materials, and related visual assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitlmt](https://clawhub.ai/user/hitlmt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creative, marketing, product, and design teams use this skill to guide an agent from a visual brief to a richer image-generation prompt. It covers common commercial visual formats, including ecommerce images, posters, brand visuals, packaging concepts, social media assets, infographics, entertainment posters, concept art, photography styles, event visuals, and interior concepts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users who do not read Chinese may misunderstand the skill's prompt-generation guidance. <br>
Mitigation: Have a Chinese reader review generated creative direction before using it in production or translate the guidance before handoff. <br>
Risk: User-supplied product, model, scene, or style images may be sent to a downstream image-generation service. <br>
Mitigation: Only provide images that are approved for the downstream service and do not contain sensitive or restricted material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hitlmt/limtdesign) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Scene guidance index](artifact/scenes/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text creative direction with structured image-generation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language guidance; prompts may reference user-provided product, model, scene, or style images when supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
