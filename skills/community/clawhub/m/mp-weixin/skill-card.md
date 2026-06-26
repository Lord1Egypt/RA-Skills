## Description: <br>
Uses Python to extract metadata and article body content from WeChat Official Account article URLs, including title, author, body HTML, publish time, and cover image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bozoyan](https://clawhub.ai/user/bozoyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch public mp.weixin.qq.com article pages and convert WeChat article metadata and content into structured data for archiving, analysis, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill could be misused to scrape restricted WeChat content, bypass verification, or use logged-in cookies without authorization. <br>
Mitigation: Use it only with intended public mp.weixin.qq.com URLs, respect access controls and rate limits, and do not use it for CAPTCHA bypass or unauthorized logged-in sessions. <br>
Risk: Extracted article HTML and saved JSON may contain third-party content, links, or sensitive data from the source page. <br>
Mitigation: Review extracted output paths and JSON contents before automated use, and handle copied article content according to applicable privacy, copyright, and organizational requirements. <br>


## Reference(s): <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) <br>
- [Requests Documentation](https://docs.python-requests.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, guidance] <br>
**Output Format:** [CLI text summaries and structured JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful extraction returns article metadata, body HTML, account metadata when available, source URL parameters, and copyright status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
