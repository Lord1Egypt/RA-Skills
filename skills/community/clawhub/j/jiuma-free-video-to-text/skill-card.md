## Description: <br>
Jiuma AI skill for downloading Douyin videos and extracting text from video content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dddcn1](https://clawhub.ai/user/dddcn1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to resolve Douyin share links into downloadable video URLs and, when requested, submit the resolved video for text extraction through Jiuma's service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided Douyin links, resolved video URLs, task IDs, and extracted text to Jiuma's service. <br>
Mitigation: Avoid private, sensitive, proprietary, or token-bearing links unless the user trusts Jiuma's handling and retention practices. <br>
Risk: Text extraction depends on an external API and may fail, return delayed status, or produce incomplete content. <br>
Mitigation: Check task status before relying on extracted text and review returned content before using it in downstream work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dddcn1/jiuma-free-video-to-text) <br>
- [Jiuma API endpoint](https://api.jiuma.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-like command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return resolved video URLs, download URLs, task IDs, task status, errors, and extracted text.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
