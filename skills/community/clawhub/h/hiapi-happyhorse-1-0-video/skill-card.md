## Description: <br>
Use when a user asks to create text-to-video with HappyHorse 1.0, HiAPI HappyHorse 1.0, or this specific skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiapiai](https://clawhub.ai/user/hiapiai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to generate short HappyHorse 1.0 text-to-video clips through HiAPI, with configuration checks, parameter guidance, and JSON output that points to a saved video file or remote video URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts and generation settings are sent to HiAPI under the user's account. <br>
Mitigation: Do not include secrets, regulated personal data, or confidential business material in prompts unless the organization has approved that use. <br>
Risk: The skill requires a paid HiAPI service account and sensitive API credentials. <br>
Mitigation: Store HIAPI_API_KEY in the runtime environment, avoid printing keys, and verify account billing or quota before running live generation. <br>
Risk: The npx installer can replace an existing skill folder with the same name. <br>
Mitigation: Review the installer behavior and target directory before installation, especially in shared or locked-down agent environments. <br>


## Reference(s): <br>
- [HiAPI HappyHorse 1.0 Video API](references/api.md) <br>
- [Output Handling](references/output.md) <br>
- [HiAPI Docs](https://docs.hiapi.ai) <br>
- [HiAPI Registration](https://www.hiapi.ai/en/register) <br>
- [HiAPI Pricing](https://www.hiapi.ai/en/pricing) <br>
- [ClawHub Skill Page](https://clawhub.ai/hiapiai/hiapi-happyhorse-1-0-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; the generation CLI prints JSON containing a saved video path or remote video URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and HIAPI_API_KEY; sends text prompts and generation settings to HiAPI and saves downloadable videos under outputs/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
