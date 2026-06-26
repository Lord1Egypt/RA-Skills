## Description: <br>
用 ISBN 查图书详情，或按书名关键字搜书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up book metadata by ISBN or search book records by title keyword through the JisuAPI ISBN service. It is useful when an agent needs structured book details such as title, author, publisher, publication date, price, summary, cover image, or ISBN values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags suspicious behavior involving broad full-access review execution and possible transmission of code diffs to external reviewer CLIs. <br>
Mitigation: Review the skill before installing it in sensitive repositories; use `--no-yolo` and `--fallback-reviewer none` when sandbox prompts and no automatic third-party model fallback are required. <br>
Risk: The skill requires a JisuAPI key and sends ISBN or title-search requests to external JisuAPI endpoints. <br>
Mitigation: Store the API key in `JISU_API_KEY`, limit key permissions or quota where possible, and avoid submitting sensitive search terms if external API handling is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/isbn) <br>
- [JisuAPI ISBN API documentation](https://www.jisuapi.com/api/isbn/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON responses with agent-facing guidance for summarizing book results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; calls JisuAPI ISBN query and search endpoints.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
