## Description:

Openclaw Boss generates blunt, humorous self-reflection and user-profile reports from OpenClaw memories, user information, session history, and prior reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winston-wwzhen](https://clawhub.ai/user/winston-wwzhen)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use this skill to generate daily, weekly, or monthly self-reflection reports that summarize personality traits, technical capability, security awareness, efficiency, historical score changes, and growth suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads long-term memory, user profile files, memory files, session metadata, prior reports, and memory database content.

Mitigation: Install only in a trusted workspace, review the configured data access before use, and test in a sandbox when handling sensitive personal or work data.

Risk: Scheduled report generation can create persistent weekly and monthly jobs that run with root-level cron configuration.

Mitigation: Verify or remove the missing .onload hook before installation, disable root cron scheduling when it is not needed, and prefer manual report generation for tighter control.

Risk: Generated reports may include personal information or secrets and the skill behavior asks the agent to forward full reports into chat.

Mitigation: Review and redact generated reports before forwarding or sharing them, and avoid sending full unredacted reports into chat when sensitive data may be present.

## Reference(s):

- [Analysis Dimensions](references/analysis-dimensions.md)
- [Openclaw Boss on ClawHub](https://clawhub.ai/winston-wwzhen/skills/openclaw-boss)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional ASCII score cards and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local daily, weekly, or monthly report files and print the generated report to stdout.]

## Skill Version(s):

5.2.0 (source: server release metadata and SKILL.md frontmatter; package.json reports 5.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
