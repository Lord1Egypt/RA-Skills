## Description: <br>
Fetches articles from Karpathy curated RSS feeds and generates a Chinese tech daily newsletter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MESevenJourney](https://clawhub.ai/user/MESevenJourney) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill in Claude Code to collect recent posts from a curated RSS list, select high-value technology articles, read them in full, and produce a structured Chinese daily brief with editorial synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to a hosted OPML file, many public RSS feeds, and selected article pages. <br>
Mitigation: Install and run it only in environments where that network access is acceptable; review or pin the OPML source when a fixed, auditable feed list is required. <br>
Risk: The workflow writes a dated Markdown newsletter file in the current working directory. <br>
Mitigation: Run it from a directory where creating that output file is expected and review generated content before sharing. <br>
Risk: Python dependencies are resolved at runtime through uv for the feed-fetching script. <br>
Mitigation: Use normal dependency review or lock/pin dependencies before deployment in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MESevenJourney/karpathy-curated-rss-brief) <br>
- [Publisher profile](https://clawhub.ai/user/MESevenJourney) <br>
- [Karpathy curated RSS OPML](https://mesevenjourney.github.io/static/hn-popular-blogs-2025.opml) <br>
- [Karpathy RSS list announcement](https://x.com/karpathy/status/2018043254986703167) <br>
- [The web is bearable with RSS](https://pluralistic.net/2026/03/07/reader-mode/) <br>
- [Output template](references/output-template.md) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown newsletter saved as a dated .md file, with JSON returned by the feed-fetching helper during execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch helper caps RSS results at 20 recent articles; the workflow selects 8-10 articles for the final brief and validates UTF-8 output for replacement characters.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
