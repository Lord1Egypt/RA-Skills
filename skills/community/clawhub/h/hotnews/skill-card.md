## Description: <br>
hotnews is a CLI skill that fetches trending news and hot topics from Chinese platforms and GitHub and returns structured items with titles, URLs, ranks, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengzhuangpro](https://clawhub.ai/user/zhengzhuangpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other users use this skill to list available hot-news sources and fetch recent trending topics as readable text or JSON for monitoring and downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run the external hotnews npm CLI, which was not included in the reviewed artifact. <br>
Mitigation: Confirm the package name and provenance before first use, install it from a trusted source, and keep normal package-review controls in place. <br>
Risk: Fetched news and trending-topic content comes from public sources and should not be treated as trusted input. <br>
Mitigation: Review results before relying on them for decisions or passing them into downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhengzhuangpro/hotnews) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports source selection and a 1-50 item limit; JSON mode returns title, url, hot, and rank fields.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
