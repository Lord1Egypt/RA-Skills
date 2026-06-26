## Description: <br>
查询并整理今天或指定日期的日本动画新番播出和官方配信信息，并以中文表格列出作品、平台、时间和集数。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noitalihinna](https://clawhub.ai/user/noitalihinna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and anime viewers use this skill to ask an agent for a current Japanese anime airing or streaming schedule for today or a specific date, with results returned in Chinese. The skill emphasizes current web verification, JST timing, platform names, and episode numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anime schedule details can be time-sensitive, incomplete, or conflicting across public sources. <br>
Mitigation: Browse current sources, prefer official anime, broadcaster, or streaming pages, cross-check episode numbers, and mark unresolved entries as pending confirmation. <br>
Risk: The skill may activate automatically for matching anime schedule requests and uses public web lookups. <br>
Mitigation: Install it only for agents expected to answer anime schedule questions from public sources, and review the returned source links before relying on the schedule. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noitalihinna/japan-anime-today) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown table with concise notes and source links when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Rows are sorted by JST airtime and should mark unverified results as pending confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
