## Description: <br>
Pinkr CRM lets an agent authenticate to the Pinkr CRM admin API and call member list and member detail endpoints through a Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[double-jin](https://clawhub.ai/user/double-jin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to connect to Pinkr CRM with admin credentials, retrieve member lists, and fetch member detail records. It is intended for CRM workflows where the agent is allowed to access Pinkr customer data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authenticated access to Pinkr CRM through admin credentials. <br>
Mitigation: Install only when the agent is trusted with Pinkr CRM admin access and use least-privilege CRM credentials where possible. <br>
Risk: CRM bearer tokens or customer data could be exposed outside the intended service boundary. <br>
Mitigation: Keep unrelated secrets out of readable environment files, avoid logging login output, and review returned CRM data before sharing it. <br>
Risk: The API command accepts endpoint input, which can increase impact if an autonomous agent calls unintended URLs or paths. <br>
Mitigation: Limit use to expected Pinkr CRM endpoints and require review before allowing autonomous endpoint or payload selection. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/double-jin/pinkr-admin-api) <br>
- [Publisher profile](https://clawhub.ai/user/double-jin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Pinkr CRM credentials in environment variables and returns formatted JSON from CRM API calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
