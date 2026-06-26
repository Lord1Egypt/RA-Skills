## Description: <br>
Full AI image creation workflow: intent classification, prompt enhancement, multi-direction generation via fal.ai, and error recovery for image creation requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to plan, enhance, and run AI image generation or image-editing workflows through fal.ai, including prompt refinement, model selection, batch directions, result presentation, and error recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and reference images may be processed by fal.ai. <br>
Mitigation: Use a dedicated FAL_API_KEY and avoid submitting confidential prompts or private images unless third-party processing is acceptable. <br>
Risk: Generated images may be saved locally under ~/Pictures/ai-image. <br>
Mitigation: Review local output paths and remove generated files that should not be retained. <br>
Risk: Referenced prompt-library files are not included in this package. <br>
Mitigation: Expect inspiration and template lookup features to require those files to exist separately, or fall back to direct prompt guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-ai-image) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Skill homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with prompt text, tables, Python code blocks, generated image URLs, and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call fal.ai with FAL_API_KEY and save generated images locally under ~/Pictures/ai-image.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
