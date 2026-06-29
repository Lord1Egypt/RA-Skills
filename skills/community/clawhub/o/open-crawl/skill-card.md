## Description: <br>
open-crawl helps agents look up live Amazon product or search-result data, or a named public web page, through Claw School's hosted data API and return structured JSON or raw HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claw-school](https://clawhub.ai/user/claw-school) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they explicitly need current Amazon product, search-result, or named public-page data returned in a structured form. It is not intended for background crawling or for private, logged-in, internal, tokenized, or sensitive pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested public URLs and returned page content are sent to Claw School's hosted API and its upstream scraping provider. <br>
Mitigation: Use only user-requested public URLs, and do not submit private, logged-in, internal, tokenized, or sensitive pages. <br>
Risk: The CLAW_KEY authenticates access to the hosted API. <br>
Mitigation: Keep the CLAW_KEY confidential and send it only to the Claw School API as an Authorization: Bearer credential. <br>


## Reference(s): <br>
- [open-crawl ClawHub skill page](https://clawhub.ai/claw-school/skills/open-crawl) <br>
- [Claw School access page](https://claw-school.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [Structured JSON responses with optional raw HTML fallback and concise user-facing error guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses HTTPS POST requests with a CLAW_KEY; public, user-requested URLs only.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
