## Description: <br>
AI-powered Investor Relations Manager - automated video generation for earnings reports, financial updates, and stakeholder communications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Investor relations and corporate communications teams use this skill to turn financial updates, earnings highlights, shareholder updates, and investor-focused product announcements into professional presentation videos. Agents use it to guide setup, run the provided video-generation commands, and remind users to review financial accuracy and compliance before distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs an external npm project and its dependencies. <br>
Mitigation: Review the external repository and dependency tree before installation, and run it in a controlled project directory. <br>
Risk: Investor-relations content can include confidential, material, or unapproved financial disclosures processed through OpenAI APIs. <br>
Mitigation: Use only data approved by the organization's disclosure policy, use a dedicated OpenAI API key with appropriate limits, and avoid entering confidential information unless policy permits it. <br>
Risk: Generated videos may contain incorrect financial statements or presentation choices that are unsuitable for regulated investor communications. <br>
Mitigation: Review all generated videos for data accuracy, legal compliance, and stakeholder-communication requirements before distribution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZhenStaff/investor-relations-manager) <br>
- [Project repository](https://github.com/ZhenRobotics/openclaw-investor-relations-manager) <br>
- [Quick Start Guide](https://github.com/ZhenRobotics/openclaw-investor-relations-manager/blob/main/QUICKSTART.md) <br>
- [Transformation Summary](https://github.com/ZhenRobotics/openclaw-investor-relations-manager/blob/main/IR_TRANSFORMATION_SUMMARY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to generate MP4 investor-relations videos through an external local project; the generated media is saved by that project, not by the skill card itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
