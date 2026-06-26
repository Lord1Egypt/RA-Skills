## Description: <br>
Install, configure, validate, and run the news-fetcher Python CLI for aggregating RSS/Atom and HTML news sources with deduplication, clustering, ranking, source diversity, summaries, and GitHub project discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miniade](https://clawhub.ai/user/miniade) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and operate the news-fetcher CLI, create or validate source configuration, troubleshoot command usage, and produce aggregated news or GitHub project discovery outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to install a Python package from a GitHub tag. <br>
Mitigation: Review and trust the referenced repository and tag before installation, use a virtual environment, and avoid installing as root. <br>
Risk: The CLI fetches public RSS, Atom, HTML, and GitHub sources and can write local output files. <br>
Mitigation: Use trusted source URLs, validate configuration before running, and choose output paths deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miniade/news-fetcher) <br>
- [news-fetcher source](https://github.com/miniade/news-fetcher) <br>
- [news-fetcher PyPI project](https://pypi.org/project/news-fetcher/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, code] <br>
**Output Format:** [Markdown with inline bash and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to produce JSON, Markdown, CSV, RSS, or local output files through the news-fetcher CLI.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence and skill release marker) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
