## Description: <br>
jike-data-service helps agents query Douyin content marketing data for Honor phone teams, including competitor accounts, keyword rankings, hot videos, trending hashtags, and benchmark video discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzoob](https://clawhub.ai/user/mzoob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content marketing analysts and agent operators use this skill to find Douyin accounts, keywords, hot videos, hashtags, and benchmark content for Honor and competitor phone marketing analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a remote Douyin marketing-data API and requires an authorized API key. <br>
Mitigation: Install only if you trust the ry-api.dso100.com service and are authorized to use its API key; keep the base URL pointed at the intended HTTPS service. <br>
Risk: API-key handling may expose credentials through local configuration or diagnostic output. <br>
Mitigation: Prefer the RY_DATA_SECRET_KEY environment variable, avoid committing config files with secrets, and do not share check-command output. <br>
Risk: Keyword add and delete commands can change remote monitoring state. <br>
Mitigation: Confirm any keyword add or delete request with the user before allowing the agent to run it. <br>


## Reference(s): <br>
- [jike-data-service on ClawHub](https://clawhub.ai/mzoob/jike-data-service) <br>
- [Service homepage](https://ry-api.dso100.com) <br>
- [CLI reference](references/cli-reference.md) <br>
- [Workflow guide](references/workflow-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese prose with CLI command snippets and optional JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paginated results; default page size is 20 and requests should stay within the documented maximum of 100.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
