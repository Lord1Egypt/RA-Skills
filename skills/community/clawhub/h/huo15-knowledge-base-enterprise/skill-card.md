## Description: <br>
Huo15 Knowledge Base Enterprise helps agents ingest source materials, compile them into Markdown wiki entries, search and lint the knowledge base, and sync selected wiki articles to Odoo Knowledge with visibility controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and enterprise knowledge administrators use this skill to maintain a human-readable Markdown knowledge base and publish curated wiki articles into Odoo Knowledge with workspace, private, or department-level visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can synchronize local wiki content into a configured Odoo Knowledge instance, which may expose enterprise content if configuration or visibility settings are wrong. <br>
Mitigation: Review the target Odoo URL, database, user ID, and visibility rules before export; run the Odoo export with dry-run first. <br>
Risk: The bundled enterprise configuration contains credential-like fields and the skill documentation discusses storing credentials in Odoo Knowledge. <br>
Mitigation: Replace bundled configuration before use, use a least-privilege Odoo account, and do not store passwords or API tokens in Odoo Knowledge unless the organization has approved that system for secrets. <br>
Risk: The install-all-agents script initializes knowledge-base directories across every local OpenClaw agent. <br>
Mitigation: Avoid running install-all-agents.sh unless broad local agent modification is intentional and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/huo15-knowledge-base-enterprise) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jobzhao15) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON configuration, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local knowledge-base files and synchronize wiki content to a configured Odoo Knowledge instance.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
