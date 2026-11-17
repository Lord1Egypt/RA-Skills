## Description:

Guides agents using Guandata BI through official CLI workflows and specialist playbooks for governed ETL, restricted data extraction, dashboard verification, custom charts, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maojiebc](https://clawhub.ai/user/maojiebc)

### License/Terms of Use:

MIT

## Use Case:

BI developers, analysts, and operators use this skill to work with Guandata BI through its official command-line tools and to troubleshoot ETL, dashboards, data extraction, and publishing workflows. It also guides agents in producing SQL, code, dashboard assets, and evidence reports while checking data scope and business definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security scan flags an unpinned installer and a confirmed uninstall backup risk; its analysis is partial.

Mitigation: Review the installer and verify the package source and version before installation. Use the installer's dry-run and target-specific options, and preserve any existing configuration and backup files before uninstalling.

## Reference(s):

- [Restricted query playbook](references/restricted-query-playbook.md)
- [Bounded extraction guide](references/bounded-extraction.md)
- [Dashboard evidence guide](references/dashboard-evidence.md)
- [ETL governance and write guide](references/part-b-governance.md)
- [HTML dashboard playbook](references/part-c-html-dashboard.md)
- [V7 page and card publishing pipeline](references/v7-page-card-publish-pipeline.md)
- [Official CLI compatibility notes](references/official-cli-compatibility.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, SQL, Code, Configuration, Analysis]

**Output Format:** [Markdown guidance with shell commands, SQL, code, configuration examples, and structured JSON evidence when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or revise dashboard assets, extraction reports, and validation evidence according to the selected workflow.]

## Skill Version(s):

3.5.2 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
