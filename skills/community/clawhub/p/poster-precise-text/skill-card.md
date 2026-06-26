## Description: <br>
Helps agents create Chinese posters with precise, readable text by combining AI-generated illustration prompts with HTML-rendered text layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leosheep821-debug](https://clawhub.ai/user/leosheep821-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to create Chinese health, education, activity, and operations posters where the text must remain exact and readable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive images or health-related poster content may be processed by external image generation or deployment tools. <br>
Mitigation: Confirm the privacy terms of the selected image generation and deployment tools before using sensitive content. <br>
Risk: The bundled HTML template requests Google Fonts, which can create an external network request when rendered. <br>
Mitigation: Use local fonts instead of the Google Fonts link when external font requests are not acceptable. <br>
Risk: Generated posters may contain inaccurate or misleading health or educational claims if source content is not reviewed. <br>
Mitigation: Review poster text and visual claims before publishing, especially for health-related materials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leosheep821-debug/poster-precise-text) <br>
- [poster_prompt_guide.md](references/poster_prompt_guide.md) <br>
- [bone_health_template.html](references/bone_health_template.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with HTML template code and deploy instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce HTML poster files and optional browser-based export guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
