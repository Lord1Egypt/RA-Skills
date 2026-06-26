## Description: <br>
读书每日推荐从微信读书飙升榜抓取热门书籍数据，并生成每日读书推荐卡片的 HTML 或 PNG 输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lwter](https://clawhub.ai/user/lwter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, content creators, and automation builders use this skill to fetch WeRead rising-list book data, select a daily recommendation, and render a shareable reading card. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external WeRead pages and rendered cards may load external cover images or fonts. <br>
Mitigation: Run it only in environments where those external requests are acceptable, and review generated HTML before sharing or publishing it. <br>
Risk: The skill writes local JSON, HTML, and optional PNG files, and may reuse cached ranking data. <br>
Mitigation: Use an explicit output directory, review generated files, and force a refresh when current ranking data is required. <br>
Risk: Recurring daily pushes can run repeatedly if enabled from a broad book-recommendation request. <br>
Mitigation: Ask before creating any recurring automation and confirm the schedule, destination, and generated card workflow. <br>


## Reference(s): <br>
- [WeRead Rising Ranking](https://weread.qq.com/web/category/rising) <br>
- [ClawHub skill page](https://clawhub.ai/lwter/nexus-reader) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, HTML, PNG image, Shell commands, Guidance] <br>
**Output Format:** [Local JSON data files plus generated HTML and optional PNG card files, with brief Markdown guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated files under the configured output directory and can cache fetched ranking data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
