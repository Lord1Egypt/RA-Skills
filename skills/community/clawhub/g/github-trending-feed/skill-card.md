## Description: <br>
Fetches GitHub Trending repositories, optionally filtered by language, and returns structured JSON for an agent to format for chat or console output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humor200](https://clawhub.ai/user/humor200) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical community managers, and agents use this skill to retrieve public GitHub Trending repository data and turn it into daily feed updates for chat platforms or the console. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes unauthenticated requests to GitHub, so rate limits or network failures can prevent fresh results. <br>
Mitigation: Use reasonable request frequency, add caching for high-volume use, and treat unavailable results as a temporary data-fetch issue. <br>
Risk: If scraping or API lookup fails, the script may return fallback repositories or per-repository error fields instead of current trending data. <br>
Mitigation: Check the returned JSON for error fields and freshness before publishing the feed. <br>


## Reference(s): <br>
- [GitHub Trending](https://github.com/trending) <br>
- [GitHub REST API repository endpoint](https://api.github.com/repos/{owner}/{repo}) <br>
- [ClawHub skill page](https://clawhub.ai/humor200/github-trending-feed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [JSON data that the agent formats as Markdown, chat messages, or console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns repository name, description, language, star count, URL, and optional error fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
