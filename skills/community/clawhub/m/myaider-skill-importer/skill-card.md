## Description: <br>
Import, create, and upgrade agent skills from a configured MyAider MCP server using the skill-creator workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hurungang](https://clawhub.ai/user/hurungang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to discover a configured MyAider MCP server, select remote skills to import or upgrade, and create local agent skill files through skill-creator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote MCP content can be used to create or overwrite local agent skills. <br>
Mitigation: Select individual skills when possible, review generated SKILL.md files before accepting imports or upgrades, and keep backups of existing skills. <br>
Risk: The importer depends on the trustworthiness of the configured MyAider MCP server and the skills it returns. <br>
Mitigation: Install and run it only with a trusted MyAider MCP server and review returned skill content before deployment. <br>


## Reference(s): <br>
- [MyAider MCP setup](https://www.myaider.ai/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/hurungang/myaider-skill-importer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and generated SKILL.md skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke MCP tools and skill-creator to create or overwrite local skill files after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
