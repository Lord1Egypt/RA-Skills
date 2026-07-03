## Description: <br>
Extracts visible Google Search results page data, including organic results, ads, related searches, People Also Ask questions, AI Overview text, and total result counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO analysts, and market researchers use this skill to collect structured SERP data from Google Search pages they can access normally in a browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the skill includes guidance for continuing collection through Google anti-bot blocks using stealth sessions, rotating proxies, CAPTCHA handling, and parallel sessions. <br>
Mitigation: Use only pages you can access normally, avoid proxy or stealth retry workflows, and stop when CAPTCHA or blocking appears unless you have clear authorization and policy compliance. <br>
Risk: Google SERP content can vary by session, locale, page state, and whether Google serves AI Overview or asynchronous related-query sections. <br>
Mitigation: Record query parameters and session context with results, wait for page stability, and treat missing AI Overview or related queries as availability limits rather than definitive absence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/google-search-serp) <br>
- [Publisher profile](https://clawhub.ai/user/browseract-cli) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON data with Markdown instructions and inline shell command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SERP fields include searchQuery, resultsTotal, organicResults, paidResults, relatedQueries, peopleAlsoAsk, and aiOverview.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
