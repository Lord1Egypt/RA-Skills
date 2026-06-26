## Description: <br>
Fetches current international, technology, gaming, science, and framework-update headlines from public RSS feeds and presents them as a concise morning briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amadeus9169](https://clawhub.ai/user/amadeus9169) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks for a morning brief, daily briefing, or quick snapshot of world events. It fetches selected public RSS and Atom feeds, preserves source links, and helps present a concise Chinese news briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to public news and release feeds and preserves clickable third-party links. <br>
Mitigation: Run it only when live feed access is expected, review the configured feed URLs, and treat clicked source links as external content. <br>
Risk: The artifact documentation lists different Python packages than the script imports. <br>
Mitigation: Install and verify the packages used by the script, including httpx and feedparser, before relying on the command-line workflow. <br>


## Reference(s): <br>
- [Morning Brief on ClawHub](https://clawhub.ai/amadeus9169/morning-brief-v1) <br>
- [BBC World RSS Feed](https://feeds.bbci.co.uk/news/world/rss.xml) <br>
- [Solidot RSS Feed](https://www.solidot.org/index.rss) <br>
- [Polygon RSS Feed](https://www.polygon.com/rss/index.xml) <br>
- [ScienceDaily Science RSS Feed](https://www.sciencedaily.com/rss/top/science.xml) <br>
- [OpenClaw Releases Feed](https://github.com/joargp/openclaw/releases.atom) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown headings and bullet links, with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public RSS or Atom feeds over the network and supports an optional headline limit in the script.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
