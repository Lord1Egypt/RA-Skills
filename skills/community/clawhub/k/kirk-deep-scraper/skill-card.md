## Description: <br>
A Docker-based scraping skill that uses Crawlee and Playwright to extract transcripts, descriptions, or visible text from public web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need browser-backed extraction from public or explicitly authorized URLs, including YouTube transcript or description capture and generic dynamic page text scraping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scrape broad web content through browser automation, including text that may be sensitive if used on private or unauthorized pages. <br>
Mitigation: Use it only on public or explicitly authorized URLs, and avoid logged-in, private, internal, or sensitive pages. <br>
Risk: Scraped text is printed to stdout and may appear in terminal output or agent logs. <br>
Mitigation: Review the target URL and output handling before running the skill, and avoid sending sensitive content through the scraper. <br>
Risk: The skill runs Docker and Playwright automation locally. <br>
Mitigation: Install only when browser-based scraping is needed and the operator is comfortable running Docker/browser automation from the local machine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-deep-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON printed to stdout with status, content type, and extracted text fields; setup and invocation guidance is Markdown with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker and a locally built skillboss-crawlee image; extracted page text is capped in the handlers before output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
