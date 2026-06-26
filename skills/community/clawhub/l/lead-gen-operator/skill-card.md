## Description: <br>
Automated lead generation assistant - finds companies, scores them, writes personalized outreach emails, and tracks pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Clawdquip](https://clawhub.ai/user/Clawdquip) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales and growth users use this skill in OpenClaw to discover and track prospective companies, score leads, draft personalized outreach, export pipeline data, and manage follow-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retains prospect, contact, outreach, and pipeline data locally. <br>
Mitigation: Review the local storage location, restrict access to the workspace, and keep backups before overwriting JSON lead data. <br>
Risk: The skill can send Gmail outreach and may act with too little confirmation or scoping. <br>
Mitigation: Require preview-and-confirm behavior for every outbound email and review outreach practices for compliance before use. <br>
Risk: The skill can support unsolicited or high-volume outreach workflows. <br>
Mitigation: Use only with approved prospecting policies, appropriate consent or lawful basis, and rate limits suited to the user's organization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Clawdquip/lead-gen-operator) <br>
- [README](README.md) <br>
- [Setup Guide](SETUP-GUIDE.md) <br>
- [Agent Persona](SOUL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, CSV, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, local JSON lead records, CSV exports, and generated email draft text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OpenClaw workspace files for lead storage and may optionally support Gmail outreach through a separate connected skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
