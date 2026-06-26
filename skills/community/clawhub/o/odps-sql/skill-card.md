## Description: <br>
Use this skill when the user wants to query, analyze, or explore data in Alibaba Cloud ODPS (MaxCompute) by listing tables, inspecting schemas, and running SQL through the bundled command-line helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guilongzh](https://clawhub.ai/user/guilongzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data engineers use this skill to explore Alibaba Cloud ODPS/MaxCompute projects, discover tables, inspect schemas, construct ODPS-compatible SQL, and summarize query results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can execute unrestricted SQL against an Alibaba Cloud ODPS/MaxCompute project using configured cloud credentials. <br>
Mitigation: Use least-privilege credentials, preferably read-only RAM credentials, and review generated SQL before execution. <br>
Risk: Credential scoping is weak because the helper may load a .env file from the current working directory. <br>
Mitigation: Run the helper from the intended skill directory and avoid running it from directories that contain unrelated .env files. <br>
Risk: Production access keys may be exposed or misused if stored or shared unnecessarily. <br>
Mitigation: Do not store production access keys unnecessarily, keep .env files local, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ODPS SQL Reference Guide](references/odps_sql_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/guilongzh/odps-sql) <br>
- [Publisher Profile](https://clawhub.ai/user/guilongzh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL snippets, shell commands, and summarized command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute ODPS SQL through a Python helper when configured with Alibaba Cloud credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
