## Description: <br>
Fetch and analyze OpenRank and other statistical metrics for an open source repository or developer using OpenDigger data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunny0826](https://clawhub.ai/user/sunny0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and open source program teams use this skill to query OpenDigger metrics for GitHub or Gitee repositories and developers, summarize current health signals, and produce period-specific metric tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public JSON metric files from oss.open-digger.cn, and requests for all metrics may trigger many outbound fetches. <br>
Mitigation: Install and use the skill only where outbound requests to oss.open-digger.cn are acceptable. <br>


## Reference(s): <br>
- [ClawHub OpenRank release](https://clawhub.ai/sunny0826/openrank) <br>
- [OpenDigger public metric storage](https://oss.open-digger.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and tables with fetched public metric values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the language of the user's prompt when presenting results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
