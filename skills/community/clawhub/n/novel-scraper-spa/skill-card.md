## Description: <br>
Novel Scraper SPA helps an agent scrape novel text from static or JavaScript-rendered web pages by using requests for static pages and Playwright for SPA pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch a specified public novel chapter URL, extract article or content text, and save it as a local text file. It is suited for pages that require browser rendering as well as simpler static pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches arbitrary user-provided URLs and renders pages in a headless browser when SPA behavior is detected or forced. <br>
Mitigation: Use it only on public pages that the user is allowed to access, and avoid private or authenticated URLs. <br>
Risk: Custom output paths or generated book and chapter filenames can overwrite existing local files. <br>
Mitigation: Choose book names, chapter labels, and output paths carefully, and review the destination before running the scraper. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuzhihui886/novel-scraper-spa) <br>
- [Publisher Profile](https://clawhub.ai/user/yuzhihui886) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text files with CLI status messages and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves scraped text locally, by default under ~/.openclaw/workspace/novels/ unless a custom output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
