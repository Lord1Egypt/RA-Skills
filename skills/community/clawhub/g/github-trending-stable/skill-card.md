## Description: <br>
Fetches GitHub Trending repositories by day, week, or month via web scraping, with optional language filters and text or JSON output without a GitHub API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[callmegod66](https://clawhub.ai/user/callmegod66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to answer questions about current GitHub trending repositories, hot projects, and language-specific trends. It can return a readable ranked list or JSON for downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires outbound requests to GitHub Trending pages. <br>
Mitigation: Use it only in environments where outbound access to GitHub is permitted. <br>
Risk: Results depend on GitHub's public page structure and may become empty or inaccurate if GitHub changes the page markup. <br>
Mitigation: Review outputs for plausibility and update the parser when GitHub Trending markup changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/callmegod66/github-trending-stable) <br>
- [GitHub Trending](https://github.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text ranking or JSON object with period, updated_at, and repository data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports daily, weekly, or monthly periods, optional language filtering, and configurable result limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
