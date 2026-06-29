## Description: <br>
This Agent Skill helps agents route standard Guandata BI work to the official Guandata CLI family and handle advanced ETL governance, custom chart debugging, v7 publishing, SuperApp workflows, AI-native ADS design, and restaurant BI formulas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maojiebc](https://clawhub.ai/user/maojiebc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, BI engineers, and analysts use this skill to help an agent work with Guandata BI environments, especially for ETL governance, BI engine troubleshooting, custom dashboards, SuperApp workflows, and business formula design. It is intended for users administering their own BI instance with appropriate account permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to ETLs, datasets, dashboards, forms, and pages in a Guandata BI instance. <br>
Mitigation: Review BI permissions before use and prefer a non-production or least-privilege BI account for testing. <br>
Risk: Deletion or overwrite tasks can affect BI assets. <br>
Mitigation: Keep deletion and overwrite workflows behind explicit human confirmation, and confirm backups or rebuild sources before proceeding. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maojiebc/skills/guanyuan-majia) <br>
- [README.en.md](README.en.md) <br>
- [SmartETL Full-Chain Rewrite](references/part-b17-fullchain-rewrite.md) <br>
- [HTML Dashboard Playbook](references/part-c-html-dashboard.md) <br>
- [SuperApp Pipeline](references/part-e-superapp-pipeline.md) <br>
- [AI-Native ADS Design](references/ai-native-ads-design.md) <br>
- [Restaurant BI Formula Library](references/restaurant-bi-formulas/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command snippets, JSON and SQL examples, and implementation playbooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing instructions for Guandata BI governance, ETL, custom charts, dashboards, SuperApp workflows, and formula design.] <br>

## Skill Version(s): <br>
3.1.4 (source: SKILL.md frontmatter metadata, package.json, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
