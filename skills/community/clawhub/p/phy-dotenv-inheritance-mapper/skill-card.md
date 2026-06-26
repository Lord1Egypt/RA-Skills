## Description: <br>
Maps a project's dotenv inheritance chain into a resolved report that shows override sources, environment conflicts, missing example variables, and code-referenced variables without external API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to inspect dotenv file load order, understand which environment values win, identify missing or conflicting variables, and improve local and deployment configuration hygiene. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dotenv reports may expose secrets or sensitive configuration values from local .env files. <br>
Mitigation: Treat reports as sensitive and redact secret values by default before sharing or committing them. <br>
Risk: Suggested git and .gitignore commands may alter repository tracking for environment files. <br>
Mitigation: Review each suggested command before running it, especially commands that remove files from git tracking or change ignore rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-dotenv-inheritance-mapper) <br>
- [Canlah AI](https://canlah.ai) <br>
- [The Twelve-Factor App: Config](https://12factor.net/config) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown report with tables, summaries, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include resolved environment-variable maps, conflict summaries, missing-variable findings, generated .env.example suggestions, and gitignore recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
