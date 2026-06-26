## Description: <br>
Generate PowerPoint presentations via GoAI API from text, ideas, outlines, reference images, reference PDF URLs, or reference content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goai](https://clawhub.ai/user/goai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate PowerPoint decks from a prompt or outline through the GoAI PPT API, optionally adding reference images, PDF URLs, reference content, page count, language, aspect ratio, and resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, and generated deck links are sent to GoAI using an API-key-backed account. <br>
Mitigation: Use the skill only with content intended for GoAI, avoid confidential files unless authorized, and store GOAI_API_KEY only in the skill environment. <br>
Risk: The script may auto-open the downloaded PPTX locally. <br>
Mitigation: Handle generated files according to local file safety policy and review the deck source before sharing or trusting its contents. <br>
Risk: When credits are insufficient, the skill returns a generic demo PPT URL rather than a generated presentation. <br>
Mitigation: Treat the demo URL as a preview sample only and do not present it as user-specific output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goai/goai-ppt-gen) <br>
- [GoAI publisher profile](https://clawhub.ai/user/goai) <br>
- [GoAI homepage](https://mustgoai.com) <br>
- [GoAI PPT service](https://ppt.mustgoai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text status lines with a generated PPTX file path and public URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful runs report MEDIA, MEDIA_URL, RESULT_PATH, and RESULT_URL; the skill requires uv and GOAI_API_KEY and may upload local reference images before generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and pyproject.toml report 0.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
