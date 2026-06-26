## Description: <br>
OneABC lets agents call OneABC-compatible chat, image, video, music, and model-listing endpoints through a local Node.js wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingfan0828](https://clawhub.ai/user/xingfan0828) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to list OneABC models or send prompts to chat, image, video, and music model endpoints from a local command-line wrapper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and an API key are sent to the configured OneABC-compatible endpoint. <br>
Mitigation: Install only when the publisher and configured ONEABC_BASE_URL are trusted, and verify the endpoint before running commands. <br>
Risk: Using OPENAI_API_KEY as a fallback can unintentionally send an unrelated key to the configured endpoint. <br>
Mitigation: Prefer a dedicated ONEABC_API_KEY and avoid relying on OPENAI_API_KEY for this wrapper. <br>


## Reference(s): <br>
- [ClawHub OneABC listing](https://clawhub.ai/xingfan0828/oneabc) <br>
- [Default OneABC API endpoint](https://api.oneabc.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text command output with Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and ONEABC_API_KEY or OPENAI_API_KEY; sends prompts to the configured ONEABC_BASE_URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
