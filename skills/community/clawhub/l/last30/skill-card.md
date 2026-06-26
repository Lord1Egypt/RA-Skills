## Description: <br>
Researches a topic across Reddit, X/Twitter, Hacker News, YouTube, Polymarket, and web search from the last 30 days, then synthesizes a grounded, cited briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ralph-oei](https://clawhub.ai/user/ralph-oei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to research recent trends, news, recommendations, and product comparisons across multiple public sources and produce a concise cited briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics are sent to external services including Brave Search, Reddit, Hacker News, YouTube search, Polymarket, and optionally X/Twitter. <br>
Mitigation: Avoid submitting confidential topics, and use the skill only when the listed services are acceptable for the research context. <br>
Risk: Optional X/Twitter credentials are passed to the local `bird` executable when AUTH_TOKEN and CT0 are set. <br>
Mitigation: Leave AUTH_TOKEN and CT0 unset unless X/Twitter search is required, and verify the `bird` executable on PATH before providing session credentials. <br>
Risk: Briefings are saved to ~/Documents/Last30Days/ by default. <br>
Mitigation: Use a controlled save directory when needed and review or remove saved reports that contain sensitive research topics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ralph-oei/last30) <br>
- [Publisher profile: ralph-oei](https://clawhub.ai/user/ralph-oei) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown briefing by default, with optional compact text or JSON output from script emit modes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved to ~/Documents/Last30Days/ by default and support quick, balanced, and deep result limits.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and artifact _meta.json; SKILL.md frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
