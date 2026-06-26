## Description: <br>
Sync memories across multiple agents using a shared TiDB Zero database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilyjazz](https://clawhub.ai/user/lilyjazz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Hive Mind to store and retrieve small preference key-value pairs across agent sessions and devices through a shared TiDB-backed memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores preferences in remote persistent memory, so sensitive values could be exposed if users save secrets, private personal data, or policy instructions. <br>
Mitigation: Use it only for low-sensitivity preferences and avoid storing passwords, secrets, private personal data, or policy instructions. <br>
Risk: Shared TiDB credentials or the cached local DSN can provide access to stored preferences if exposed. <br>
Mitigation: Use least-privilege TiDB credentials and protect the ~/.openclaw_hive_mind_dsn file with appropriate local filesystem permissions. <br>
Risk: Broad memory protocols can cause an agent to save unintended facts as persistent preferences. <br>
Mitigation: Configure the agent to save facts only when the user explicitly asks to remember them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilyjazz/hive-mind) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON responses from the CLI with Markdown usage and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports set, get, and list operations for preference keys; requires python3, curl, pymysql, and TiDB connection settings or auto-provisioning.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
