## Description: <br>
Scan websites and content to identify SEO gaps, analyze meta tags, technical factors, keyword use, and provide competitor comparison insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattvalenta](https://clawhub.ai/user/mattvalenta) <br>

### License/Terms of Use: <br>


## Use Case: <br>
SEO practitioners, marketers, developers, and site owners use this skill to audit pages for on-page SEO, technical SEO, structured data, content quality, and competitor comparison gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit commands and API calls can test websites or URLs that the user is not authorized to assess. <br>
Mitigation: Confirm authorization for each target URL before running web, Lighthouse, PageSpeed, or Search Console checks. <br>
Risk: Private or staging URLs could be sent to Google APIs during PageSpeed, mobile-friendly, or rich-results checks. <br>
Mitigation: Use approved public URLs or obtain approval before sending non-public URLs to third-party APIs. <br>
Risk: API keys and bearer tokens may be exposed when using the example Google API commands. <br>
Mitigation: Keep credentials out of chats and source files, use environment variables or secret stores, and rotate any exposed tokens. <br>
Risk: Running Lighthouse through npx can execute packages from the package registry. <br>
Mitigation: Use trusted or pinned package versions when running Lighthouse locally. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mattvalenta/pls-seo-audit) <br>
- [PageSpeed Insights API endpoint](https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile) <br>
- [Google Search Console Mobile-Friendly Test endpoint](https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?key=YOUR_API_KEY) <br>
- [Google Rich Results Test endpoint](https://searchconsole.googleapis.com/v1/urlTestingTools/richResultsTest:run) <br>
- [Schema.org](https://schema.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, shell commands, code snippets, JSON examples, and an SEO audit report template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external web and Google API calls; users should provide authorized target URLs and protect credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
