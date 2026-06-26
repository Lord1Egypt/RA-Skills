## Description: <br>
通过华银康集团 PathClaw 服务对 .svs 病理切片进行 AI 辅助诊断。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t-programmer](https://clawhub.ai/user/t-programmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and clinicians use this skill to submit authorized .svs pathology slide files to the PathClaw service for AI-assisted diagnostic analysis and result polling. The skill guides the user through supported pathology category selection, file validation, upload, and result reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive pathology slide files may be uploaded to an external PathClaw service without clear pre-upload consent or privacy disclosure. <br>
Mitigation: Require explicit user confirmation before upload and use the skill only when the organization has approved the vendor, privacy terms, retention policy, and clinical-use limits. <br>
Risk: Pathology slides may contain regulated or identifying health information. <br>
Mitigation: Prefer de-identified or non-regulated samples unless the user is authorized to send the files and the deployment has appropriate privacy controls. <br>
Risk: AI-assisted pathology output could be mistaken for a final clinical diagnosis. <br>
Mitigation: Present results as AI-assisted reference output and require review by qualified medical professionals before clinical use. <br>


## Reference(s): <br>
- [PathClaw skill page](https://clawhub.ai/t-programmer/skills/pathclaw) <br>
- [PathClaw login API](https://pathclaw.pathologyunion.com/api/user/login) <br>
- [PathClaw diagnosis submission API](https://pathclaw.pathologyunion.com/api/v1/diagnosis/run) <br>
- [PathClaw diagnosis result API](https://pathclaw.pathologyunion.com/api/v1/diagnosis/<slide_id>/result) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with status summaries, result text, links, and inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes supported pathology category mapping, .svs file validation guidance, polling status summaries, and token redaction expectations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
