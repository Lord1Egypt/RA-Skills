## Description: <br>
Helps agents search, browse, inspect, and install Huawei Cloud agent skills by using a remote GitCode-hosted skill index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to locate Huawei Cloud skills for services such as ECS, OBS, RDS, and VPC, review matching skill details, and prepare installation commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches remote catalog data before recommending skills. <br>
Mitigation: Review search results and fetched skill documentation before treating a result as authoritative. <br>
Risk: Installation commands can modify the local skill setup. <br>
Mitigation: Review the exact npx command and source before execution, and require explicit confirmation before installing a matched skill. <br>
Risk: The security verdict is suspicious because remote fetching and install guidance are broader than the disclosed controls justify. <br>
Mitigation: Use the skill in a constrained environment and avoid installing directly from a search result without human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huaweiclouddev/skills/huawei-cloud-find-skills) <br>
- [Search script](artifact/scripts/search-skills.py) <br>
- [GitCode skill index](https://gitcode.com/api/v5/repos/2501_91318609/skills-for-index/contents/skills-index/index.json?ref=main) <br>
- [GitCode Chinese-English keyword map](https://gitcode.com/api/v5/repos/2501_91318609/skills-for-index/contents/skills-index/cn-en-map.json?ref=main) <br>
- [Huawei Cloud skills repository](https://github.com/huaweicloud/huaweicloud-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples and search-result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.6+ and outbound HTTPS access to gitcode.com when executing the search script.] <br>

## Skill Version(s): <br>
0.0.8 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
