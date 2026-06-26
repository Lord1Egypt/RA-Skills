## Description: <br>
Universal image and poster generator with Chinese/English text support for posters, social media images, cover images, infographics, comparison charts, tutorial cards, and other visual content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate poster and social image assets from titles, prompts, template choices, and size presets. It can produce AI-backed image backgrounds, HTML-rendered layouts, or simple PIL text posters with Chinese and English text support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default AI mode can send prompts and poster text to a third-party image service. <br>
Mitigation: Use only non-sensitive content with AI mode; choose local text mode for private content. <br>
Risk: HTML mode renders user-supplied text into templates and uses Chromium without sandboxing. <br>
Mitigation: Avoid HTML mode with untrusted text unless the skill is updated to escape HTML input and run the browser with appropriate isolation. <br>


## Reference(s): <br>
- [Poster Forge on ClawHub](https://clawhub.ai/huuuwnnn-droid/poster-forge) <br>
- [Pollinations image endpoint](https://image.pollinations.ai/) <br>
- [Noto CJK fonts](https://github.com/googlefonts/noto-cjk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces image files through local Python execution; auto mode may call a third-party image service before falling back to local rendering.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
