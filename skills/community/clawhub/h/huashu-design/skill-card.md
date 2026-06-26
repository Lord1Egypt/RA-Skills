## Description: <br>
Huashu Design helps agents produce high-fidelity HTML-based prototypes, interactive demos, slide decks, motion design exports, design variants, and expert design reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swang066](https://clawhub.ai/user/swang066) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Designers, developers, and agent users use this skill to turn short creative briefs into visual deliverables such as clickable product prototypes, HTML slide decks, animations, infographics, design direction explorations, and review punch lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to search the web and download brand, product, or media assets. <br>
Mitigation: Review downloaded assets for source trust, licensing, and relevance before including them in deliverables. <br>
Risk: Generated browser prototypes or demos may ask for API credentials for optional LLM or TTS integrations. <br>
Mitigation: Use short-lived or scoped keys when possible, avoid hard-coding long-lived credentials into generated files, and remove keys before sharing outputs. <br>
Risk: The workflow may create local project files and run Playwright or ffmpeg tooling for verification and media export. <br>
Mitigation: Run generated commands in a project workspace, inspect produced files, and review media outputs before publication. <br>
Risk: The optional personal asset index can expose private brand or project context to the agent workflow. <br>
Mitigation: Keep the asset index limited to information appropriate for agent use and omit confidential material that is not needed for the task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/swang066/huashu-design) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Workflow reference](references/workflow.md) <br>
- [Design styles reference](references/design-styles.md) <br>
- [Verification reference](references/verification.md) <br>
- [Video export reference](references/video-export.md) <br>
- [Voiceover pipeline reference](references/voiceover-pipeline.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, JSX, JavaScript, shell commands, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser-rendered HTML, PPTX/PDF exports, MP4/GIF media, screenshots, timelines, and review notes depending on the task.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
