## Description:

AI-powered Investor Relations Manager - automated video generation for earnings reports, financial updates, and stakeholder communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

External communications and investor relations teams use this skill to turn verified financial updates, earnings report content, and stakeholder announcements into professional video presentations. Agents use it to guide setup, configuration, and local command execution for the IR video workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation asks users to run mutable external repository code, npm dependencies, and shell scripts.

Mitigation: Install only if the publisher is trusted, review or pin a specific commit before running commands, and inspect scripts before execution.

Risk: The workflow uses local credentials and may process sensitive or material nonpublic financial information.

Mitigation: Use a narrowly scoped, revocable OpenAI API key and avoid submitting sensitive financial information unless OpenAI processing and local disk storage are approved.

Risk: Generated investor communications can be misleading if source financial data is incorrect or disclosure language is not reviewed.

Mitigation: Verify all financial data and require legal or compliance review before distributing generated videos.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/investor-relations-manager)
- [GitHub repository](https://github.com/ZhenRobotics/openclaw-investor-relations-manager)
- [Quick Start Guide](https://github.com/ZhenRobotics/openclaw-investor-relations-manager/blob/main/QUICKSTART.md)
- [Transformation Summary](https://github.com/ZhenRobotics/openclaw-investor-relations-manager/blob/main/IR_TRANSFORMATION_SUMMARY.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance targets a local Node.js video-generation project and may lead the agent to produce MP4 video files through shell commands.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
