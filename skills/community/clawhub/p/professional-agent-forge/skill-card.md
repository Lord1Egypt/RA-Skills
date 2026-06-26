## Description: <br>
Builds complete OpenClaw agent packages for real professions or job roles, centered on core role files and a supporting-skill recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliciawque](https://clawhub.ai/user/aliciawque) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate role-ready OpenClaw agent packages for professions such as product manager, software engineer, lawyer, data analyst, designer, and marketer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated packages can recommend MCP servers, account integrations, filesystem access, database access, or long-term memory. <br>
Mitigation: Review and explicitly approve each generated integration or access recommendation before enabling it. <br>
Risk: Profession-specific packages may be applied to legal, client, business, or production data. <br>
Mitigation: Have a qualified human review generated agent behavior and boundaries before using the package in sensitive workflows. <br>


## Reference(s): <br>
- [Data Analyst Full Agent Reference](references/data-analyst.md) <br>
- [UI/UX Designer Full Agent Reference](references/designer.md) <br>
- [Lawyer Full Agent Reference](references/lawyer.md) <br>
- [Marketer Full Agent Reference](references/marketer.md) <br>
- [Product Manager Full Agent Reference](references/product-manager.md) <br>
- [Software Engineer Full Agent Reference](references/software-engineer.md) <br>
- [Apache Superset](https://github.com/apache/superset) <br>
- [Evidence](https://github.com/evidence-dev/evidence) <br>
- [Great Expectations](https://github.com/great-expectations/great_expectations) <br>
- [dbt Core](https://github.com/dbt-labs/dbt-core) <br>
- [Backstage](https://github.com/backstage/backstage) <br>
- [NocoDB](https://github.com/nocodb/nocodb) <br>
- [Appsmith](https://github.com/appsmithorg/appsmith) <br>
- [PostHog](https://github.com/PostHog/posthog) <br>
- [Visual Studio Code](https://github.com/microsoft/vscode) <br>
- [Neovim](https://github.com/neovim/neovim) <br>
- [lazygit](https://github.com/jesseduffield/lazygit) <br>
- [bat](https://github.com/sharkdp/bat) <br>
- [ripgrep](https://github.com/BurntSushi/ripgrep) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown package with sections for soul.md, identity.md, memory.md, agents.md, tools.md, and skills-recommendation.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific agent package content and recommends supporting skills and tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
