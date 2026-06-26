## Description: <br>
导师 Mentor helps an agent collect public posts, speeches, and social or video content for a named public figure, analyze their thinking framework and communication style, and generate a local MENTOR.md for mentor-style advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophie-xin9](https://clawhub.ai/user/sophie-xin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to build a mentor profile from a public figure's public social posts, videos, speeches, and biographical references. The generated mentor file supports advice and analysis through that person's extracted decision patterns, values, communication style, domain expertise, and documented blind spots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bundles collectors that can scrape sensitive personal social-media data from the currently logged-in user. <br>
Mitigation: Run collectors only with explicit user approval, avoid using personal logged-in social accounts unless local collection is intended, and review collected files before reuse. <br>
Risk: Browser automation and local file access can expose data beyond the intended public-figure sources. <br>
Mitigation: Limit ManoBrowser access to the target public pages, keep generated data local, and require approval before browser automation, MCP credential use, authenticated scraping, GitHub downloads, or shell commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sophie-xin9/mentor) <br>
- [Publisher profile](https://clawhub.ai/user/sophie-xin9) <br>
- [README](README.md) <br>
- [Analysis guide](guides/ANALYSIS.md) <br>
- [Social media collection guide](guides/SOCIAL_MEDIA.md) <br>
- [Video subtitle guide](guides/VIDEO_SUBTITLE.md) <br>
- [Wiki and quotes guide](guides/WIKI_QUOTES.md) <br>
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, JSON data files, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primary generated artifacts are MENTOR.md, raw collected data JSON, and analysis notes stored locally.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
