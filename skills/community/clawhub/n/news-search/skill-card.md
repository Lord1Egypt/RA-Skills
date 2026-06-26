## Description: <br>
Searches Baidu News, Toutiao, Bing News, Google News, and Sina News, aggregates matching news results, and removes duplicate links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlutwuwei](https://clawhub.ai/user/dlutwuwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to run browser-based news searches for a keyword across multiple public news/search providers and return deduplicated result summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords are sent to the selected third-party news and search providers. <br>
Mitigation: Avoid submitting confidential or sensitive terms unless sharing them with those providers is acceptable. <br>
Risk: The skill uses automated browser access with a stealth plugin and launches Chromium with no-sandbox flags. <br>
Mitigation: Run it in a constrained environment and confirm the selected providers' terms of service and isolation requirements before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlutwuwei/news-search) <br>
- [Publisher profile](https://clawhub.ai/user/dlutwuwei) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON news result summaries with titles, links, sources, channels, and available times.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on third-party page structure, availability, regional access, and the selected engine and result limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
