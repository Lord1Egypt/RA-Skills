## Description: <br>
Extracts around 50 Singapore for-sale listings from a PropertyGuru search results URL using a real browser session after Cloudflare verification, with listings read from the page's hydrated Next.js data and deduplicated by listing id across sequential pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snailb1007](https://clawhub.ai/user/snailb1007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect a bounded sample of public PropertyGuru Singapore sale listings from a filtered search URL when direct HTTP access is blocked or unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a real browser session to collect public PropertyGuru listing data, which may be inappropriate if used outside the stated URL and listing-count scope. <br>
Mitigation: Keep crawls bounded to the requested search URL and target count, and review PropertyGuru access terms before repeated or expanded collection. <br>
Risk: Browser automation can expose the user to local environment or session risks if run in an untrusted setup. <br>
Mitigation: Use a trusted Playwright environment and review browser session behavior before running the crawl. <br>
Risk: Cloudflare verification or PropertyGuru page changes can prevent reliable extraction. <br>
Mitigation: Report verification blocks explicitly and re-check the documented Next.js data path before changing extraction logic. <br>


## Reference(s): <br>
- [Source Notes](references/source-notes.md) <br>
- [Default PropertyGuru SG Sale Search](https://www.propertyguru.com.sg/property-for-sale?listingType=sale&page=1&isCommercial=false&maxPrice=1400000) <br>
- [ClawHub Skill Release](https://clawhub.ai/snailb1007/propertyguru-sg-sale-browser-crawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code or shell command snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill usually guides an agent to collect about 50 unique listing records while preserving source URL, page number, collection time, listing id, and raw listing payload where possible.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
