## Description: <br>
Generate images on Jimeng using an OpenClaw-managed browser, including prompt entry, ratio selection, result inspection, and local downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haohao-ui](https://clawhub.ai/user/haohao-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Jimeng image generation tasks, including setting prompts, choosing requested image options, handling visible service gates, and downloading completed outputs locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Jimeng browser profile and may encounter login, payment, membership, or credit prompts. <br>
Mitigation: Use a dedicated browser profile when possible and require the user to review login, payment, membership, or credit prompts before continuing. <br>
Risk: Generated outputs are saved to local files. <br>
Mitigation: Confirm the downloaded file exists and report the exact local path so the user can inspect the result. <br>


## Reference(s): <br>
- [Jimeng image generation entry page](https://jimeng.jianying.com/ai-tool/home/?workspace=0&type=image) <br>
- [ClawHub skill page](https://clawhub.ai/haohao-ui/jimeng-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded image file paths after browser-based generation completes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
