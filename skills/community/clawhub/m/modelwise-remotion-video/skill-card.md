## Description: <br>
Creates Remotion-based animated videos using reusable React animation components, scene transitions, and product, title, and data visualization templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deerleo](https://clawhub.ai/user/deerleo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to create, preview, and render animated videos with Remotion, React, and TypeScript. It provides reusable animation components, video templates, and common commands for studio preview and MP4 rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Third-party npm dependencies and bundled JavaScript may run local development tooling. <br>
Mitigation: Review package.json and package-lock.json before installation, run in a separate project folder or container when possible, and start Remotion Studio from a shell without unrelated API keys or secrets. <br>
Risk: Generated video code or templates may produce incorrect, inaccessible, or platform-mismatched output. <br>
Mitigation: Preview compositions in Remotion Studio, run TypeScript checks, verify contrast and timing, and render test videos before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deerleo/modelwise-remotion-video) <br>
- [Remotion audio buffer data URL documentation](https://remotion.dev/docs/audio-buffer-to-data-url) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify Remotion React components, composition registrations, video presets, and render commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
