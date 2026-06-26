## Description: <br>
Kimi Use provides Node.js tools for Kimi AI chat, image understanding, translation, and model-backed search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnlangzi](https://clawhub.ai/user/cnlangzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Kimi models from Node.js for chat, image understanding, translation, and model-backed search. It supports both CLI usage and direct module imports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, translation text, and selected local image files are sent to the configured Kimi API endpoint. <br>
Mitigation: Use only a trusted API host and avoid sending secrets, private documents, regulated data, or sensitive image files. <br>


## Reference(s): <br>
- [Kimi Use on ClawHub](https://clawhub.ai/cnlangzi/kimi-use) <br>
- [Kimi API Key Page](https://www.kimi.com/code/user-center/basic-information/interface-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown responses from Kimi API calls, with CLI output and Node.js function return objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KIMI_API_KEY and optionally KIMI_API_HOST, KIMI_MODEL, and KIMI_VISION_MODEL.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
