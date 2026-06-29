## Description: <br>
Keyword.com lets agents read Keyword.com projects, groups, keywords, rankings, regions, and current-user data through the OOMOL keyword connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve Keyword.com account, project, region, keyword, and ranking data from a connected OOMOL account without direct API token handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Keyword.com/OOMOL account and may access account-specific keyword and ranking data. <br>
Mitigation: Grant only the expected Keyword.com permissions and keep credentials managed through OOMOL; do not expose raw tokens to the agent. <br>
Risk: Connector schemas and account access can change or expire, causing failed commands or incorrect payload assumptions. <br>
Mitigation: Fetch the live connector schema before each action and retry setup only after authentication, scope, credential, or billing errors. <br>
Risk: CLI installation or authentication setup changes the local environment. <br>
Mitigation: Run setup steps only when the CLI or connection is missing and review install or auth commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-keyword) <br>
- [Keyword.com homepage](https://keyword.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run read-only Keyword.com connector actions that return JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
