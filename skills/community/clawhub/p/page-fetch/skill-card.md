## Description: <br>
Extract readable content from webpages with a stable, low-dependency workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylkangpeter](https://clawhub.ai/user/ylkangpeter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch public webpage content, inspect metadata and embedded page data, and report readable text, summaries, quotes, extraction method, and access limitations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch URLs that may require cookies or may point to private or internal resources. <br>
Mitigation: Avoid passing login cookies unless necessary and trusted, and only use the skill against internal or private network URLs when that access is intentional. <br>
Risk: Saved extraction output can persist page content to disk when explicit save options are used. <br>
Mitigation: Use explicit output paths when enabling JSON persistence and avoid saving sensitive page contents unnecessarily. <br>
Risk: Blocked pages, CAPTCHA, login walls, region restrictions, or browser runtime gaps can produce incomplete extraction. <br>
Mitigation: Report the extraction method and access limitation clearly, and do not imply full page access when only metadata or fragments were recovered. <br>


## Reference(s): <br>
- [Page Fetch Strategy](references/strategy.md) <br>
- [Browser Runtime Notes](references/browser-runtime.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with optional JSON extraction output from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports extraction method, missing content, uncertainty, and access limitations when relevant.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
