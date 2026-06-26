## Description: <br>
Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steamb23](https://clawhub.ai/user/steamb23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to generate new images, edit existing images, and submit or retrieve Gemini batch image jobs from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to Google's Gemini API. <br>
Mitigation: Avoid confidential prompts and private images unless the user accepts that external API processing. <br>
Risk: Generated files and retrieved batch outputs are written to user-supplied paths. <br>
Mitigation: Use safe, intended output paths and review filenames before running the script. <br>
Risk: Batch jobs can leave reminders or pending-job records after submission. <br>
Mitigation: Remove HEARTBEAT.md or cron reminders and pending-job entries after batch results are retrieved. <br>


## Reference(s): <br>
- [Google AI for Developers](https://ai.google.dev/) <br>
- [ClawHub release page](https://clawhub.ai/steamb23/nano-banana-pro-enhanced) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and saved image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and GEMINI_API_KEY; generated or edited images are saved as local files, and batch submissions return job identifiers for later retrieval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
