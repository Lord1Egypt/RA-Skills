## Description: <br>
Download manga chapters from MangaBat by guiding an agent to run a scraper with CDN download and optional Playwright browser fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jrrqd](https://clawhub.ai/user/jrrqd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help users download MangaBat chapters by locating and running a trusted scraper, choosing CDN or browser fallback options, and saving chapter images locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package tells agents to find and run a scraper script that is not included, making the script source uncertain. <br>
Mitigation: Only run a scraper whose exact source is trusted, and review the script before execution. <br>
Risk: Scraping can create outbound requests and local image downloads that may exceed rights, site permission, or acceptable-use expectations. <br>
Mitigation: Use the skill only for content the user has rights and permission to access, keep worker counts low, and avoid broad batch downloads without authorization. <br>
Risk: The optional Playwright fallback may install Chromium and launch a headless browser. <br>
Mitigation: Confirm the environment allows browser installation and outbound browsing before using the fallback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jrrqd/manga-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/jrrqd) <br>
- [MangaBat](https://www.mangabats.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local image output paths and optional browser fallback setup.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
