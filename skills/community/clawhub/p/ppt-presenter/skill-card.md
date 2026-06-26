## Description: <br>
Creates professional reveal.js HTML presentations with AI-generated whiteboard images, presenter view, and complete word-for-word speaker scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lewislulu](https://clawhub.ai/user/lewislulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and presenters use this skill to turn topics, notes, or markdown into structured slide decks with full speaker scripts, presenter notes, and generated visual prompts or assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide prompts are sent to Google Gemini for image generation, which can expose confidential or proprietary material if users include it. <br>
Mitigation: Use only content approved for external processing, prefer a dedicated Gemini API key, and avoid confidential or proprietary material unless that processing is approved. <br>
Risk: The image helper can write outside the intended image folder if slide names include '/', absolute paths, or '..'. <br>
Mitigation: Review or sanitize slide names before running image generation, and supervise or patch the helper so generated output paths stay inside the target image directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lewislulu/ppt-presenter) <br>
- [Publisher profile](https://clawhub.ai/user/lewislulu) <br>
- [Google Gemini image generation endpoint](https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent) <br>
- [reveal.js 5.1.0 CDN stylesheet](https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown plans and scripts, reveal.js HTML, JSON image prompts, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local presentation files and image-generation prompts that require a Gemini API key for image assets.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
