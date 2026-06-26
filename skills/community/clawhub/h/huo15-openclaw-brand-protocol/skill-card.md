## Description: <br>
Guides agents through a five-step workflow to collect authoritative brand visuals and produce a structured brand-spec.md for downstream frontend design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and design-focused agents use this skill when they need to research an existing brand from official sources and codify colors, typography, logo usage, tone, and local reference assets into a reusable brand specification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl, Playwright, ImageMagick, or grep commands may fetch from an unintended URL or write to an unexpected local path. <br>
Mitigation: Review each generated command, URL, and output path before execution, and use only official, public brand sources. <br>
Risk: Downloaded brand assets may be subject to third-party usage rights or brand restrictions. <br>
Mitigation: Confirm that the assets are official and that the intended use is permitted before using them in production work. <br>
Risk: Brand specifications can become inaccurate if based on unofficial logos, visual guesses, or a single source. <br>
Mitigation: Follow the skill's verification gate by checking exact colors and fonts against multiple authoritative sources before codifying the brand spec. <br>


## Reference(s): <br>
- [Huo15 Openclaw Brand Protocol on ClawHub](https://clawhub.ai/zhaobod1/huo15-openclaw-brand-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command blocks and a brand-spec.md template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-reviewed download and extraction commands plus a local brand-spec.md structure; it does not claim to execute downloads itself.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
