## Description: <br>
Gathers top public news from X.com and RSS sources, translates and summarizes it in Chinese, and generates daily visual news posters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, journalists, developers, and teams use this skill to create keyword-driven daily news digests, translated summaries, and shareable posters from public news sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill browses public news sites and stores keyword-specific summaries and posters locally. <br>
Mitigation: Use it only for intended public-news briefings and periodically review or delete saved data under ~/workspace/news-digest. <br>
Risk: Scheduled briefings can continue producing local files over time. <br>
Mitigation: Enable recurring jobs only when ongoing automatic generation is desired and review scheduled tasks and retained outputs regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/news-daily-digest-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON news data, HTML poster source, and rendered poster files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves keyword-specific data and posters under ~/workspace/news-digest with date-based archival.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
