## Description: <br>
Fetch and generate structured reports on fastest-growing repositories, newly popular projects, and hot GitHub topic tags using the github-discover CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderyi](https://clawhub.ai/user/coderyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical analysts use this skill to run github-discover, combine real-time GitHub Search API data, and produce a concise Markdown report on repository growth, newly popular projects, and active topic tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party github-discover npm package. <br>
Mitigation: Install it only when the package is trusted, and pin or review the package version when supply-chain reproducibility matters. <br>
Risk: Generated reports contact GitHub and depend on GitHub Search API freshness and indexing behavior. <br>
Mitigation: Treat results as time-sensitive GitHub Search API output, and note that the growth score is estimated rather than official GitHub Trending data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/coderyi/github-trending-report) <br>
- [Publisher Profile](https://clawhub.ai/user/coderyi) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown report with repository lists, topic summaries, and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-derived repository metadata, links, star counts, primary languages, and short trend analysis.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
