## Description:

Periodic Reflection generates structured self-evolution reflection reports for EvoMap publishing, agent evolution, DevOps operations, and other workflows that need metric-based retrospectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent maintainers use this skill to generate recurring Markdown reflection reports that compare metrics, track versions and changelog entries, record findings, and plan next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic mode can repeatedly generate reports that appear data-backed and healthy without real metric collection or unknown/unhealthy states.

Mitigation: Review and correct the report generator before using --auto for monitoring or compliance decisions.

Risk: Cron-based automation can create repeated local report and log output without retention or duplicate-run safeguards.

Mitigation: Enable cron only after adding clear removal, private log paths, retention, and duplicate-run safeguards.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jpengcheng523-netizen/skills/periodic-reflection)
- [Best Practices](references/best-practices.md)
- [Reflection Report Template](templates/reflection-template.md)
- [Complete Documentation](https://www.feishu.cn/docx/ZEeYdNWKtoFWI7xf6MCcXottnYg)
- [Introduction Documentation](https://www.feishu.cn/docx/BuMrdiWCmov6yvxRE1PcFGTLnWH)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown report files with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local reports under reports/ or a user-specified output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
