## Description: <br>
Scrape GitHub Trending repositories into structured JSON with optional language, time range, result count, and output-file controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yes999zc](https://clawhub.ai/user/yes999zc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to collect current GitHub Trending repository data for analysis, cards, visualizations, or other downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound HTTPS requests to GitHub Trending. <br>
Mitigation: Use it only in environments where network access to GitHub is acceptable. <br>
Risk: The optional --output flag can overwrite a user-selected file path. <br>
Mitigation: Write output to a temporary or workspace path intended for replacement, not to important files. <br>
Risk: Scraped GitHub Trending HTML may change or omit repository metrics. <br>
Mitigation: Review downstream use of stars, forks, and period-star fields, especially when values are zero or missing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yes999zc/github-trending-scraper) <br>
- [GitHub Trending](https://github.com/trending) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON written to stdout or an optional user-specified file, with Markdown usage guidance for agent responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports language filters, daily/weekly/monthly ranges, top-N limiting, and compact JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
