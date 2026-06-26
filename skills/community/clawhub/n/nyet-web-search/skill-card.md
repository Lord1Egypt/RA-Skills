## Description: <br>
Web Search (DDG) helps agents search DuckDuckGo for web pages, news, images, and videos and return clean results as text, Markdown, or JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyetnighy](https://clawhub.ai/user/nyetnighy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to gather current web, news, image, and video results for research, fact-checking, market scans, and URL collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to DuckDuckGo and may reveal sensitive terms. <br>
Mitigation: Avoid submitting secrets, private identifiers, or confidential business details as search queries. <br>
Risk: Saved search results are external web content and may overwrite files if an unsafe output path is chosen. <br>
Mitigation: Use a dedicated output folder, avoid important file paths, and treat saved results as untrusted content until reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nyetnighy/nyet-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Plain text, Markdown, or JSON search results, optionally saved to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include titles, URLs, descriptions, source metadata, publication dates, image links, thumbnails, dimensions, video publishers, and durations depending on the search type.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
