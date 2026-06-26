## Description: <br>
Create product demo videos with voiceover, text overlays, and real browser interactions using Puppeteer, edge-tts, PIL/Pillow, and FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiazai77](https://clawhub.ai/user/xiazai77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to plan and generate browser-based product walkthrough videos with narration, overlays, and MP4 output for launches or showcases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation can make broad system changes, including global npm and pip installs, package-manager font installs, and copying FFmpeg binaries into a system path. <br>
Mitigation: Review or patch the install script first; prefer package-manager FFmpeg or verified downloads, and avoid global or system installs where possible. <br>
Risk: Customized narration and scene text are passed through shell command construction during demo generation. <br>
Mitigation: Use test sites and non-confidential narration, sanitize customized scene content, and review the scripts before running them. <br>
Risk: Generated overlays may include privacy or client-side claims that are not automatically verified. <br>
Mitigation: Review generated videos before sharing and remove any privacy badges or claims unless they have been independently verified. <br>


## Reference(s): <br>
- [Demo Planning Guide](references/demo-planning.md) <br>
- [Product Demo Video Creator on ClawHub](https://clawhub.ai/xiazai77/product-demo-video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JavaScript and shell snippets; generated demo output is an MP4 file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires customized scene definitions and local browser, audio, and video tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
