## Description: <br>
비라틴 문자(한글, 일본어, 중국어 등)를 AI 이미지에 정확히 렌더링하는 스킬. Canvas 프리렌더링과 Gemini를 활용하여 텍스트 깨짐 없이 이미지를 생성합니다. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wonyoung-Huh](https://clawhub.ai/user/wonyoung-Huh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and content creators use this skill to generate images that include Korean and other non-Latin text by pre-rendering text with Canvas and passing it into Gemini image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images may be sent to Google's Gemini service. <br>
Mitigation: Avoid sensitive text or reference images unless you intend to upload them to Gemini. <br>
Risk: Setup installs npm dependencies and may download font files. <br>
Mitigation: Review the dependency installation and font download behavior before running setup in controlled environments. <br>
Risk: The skill requires access to a Gemini API key for the full analyze and generate workflow. <br>
Mitigation: Use a limited Gemini API key scoped for this workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wonyoung-Huh/nano-banana-korean-rendering) <br>
- [Publisher Profile](https://clawhub.ai/user/wonyoung-Huh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI commands emit JSON status and PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY for Gemini analysis and image generation; setup may install npm dependencies and download font files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
