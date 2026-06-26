## Description: <br>
Auto Researcher helps an agent research topics across X/Twitter, Reddit, YouTube, GitHub, Hacker News, Product Hunt, and news sites, then produce structured research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yofoan](https://clawhub.ai/user/yofoan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and product teams can use this skill to gather public signals about a topic, market, competitor, technology choice, or user feedback theme and turn the results into Markdown, JSON, or presentation-style research outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the included shell scripts can run unintended local code from a crafted research topic. <br>
Mitigation: Review and patch heredoc input handling before running the shell scripts, and avoid using pasted or untrusted topics until that handling is fixed. <br>
Risk: The security summary says research queries are sent to several outside services. <br>
Mitigation: Do not use confidential topics unless sharing those queries with the listed services and any configured CLI accounts is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yofoan/multi-platform-parallel-research) <br>
- [Publisher profile](https://clawhub.ai/user/yofoan) <br>
- [Hacker News Algolia Search API](https://hn.algolia.com/api/v1/search) <br>
- [Jina AI Reader](https://r.jina.ai/) <br>
- [GitHub repository search](https://github.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated Markdown reports, JSON data files, and presentation outlines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Research results may be written to temporary local files and may depend on external services and locally configured CLI tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
