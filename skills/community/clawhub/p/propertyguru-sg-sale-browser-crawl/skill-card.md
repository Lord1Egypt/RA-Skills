## Description:

Collects about 50 Singapore PropertyGuru sale listings from a search results URL using a real browser session and Next.js page data after Cloudflare verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snailb1007](https://clawhub.ai/user/snailb1007)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and data analysts use this skill to collect a bounded sample of PropertyGuru Singapore sale listing data from filtered search URLs for review or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect public listing details such as price, address fields, agent, and agency.

Mitigation: Use it only for searches you are allowed to access and keep collection bounded to the data needed for the task.

Risk: PropertyGuru's Cloudflare verification, page structure, or Next.js payload path may change and block or alter extraction.

Mitigation: Use a real browser session, verify that the results page loaded before extraction, and report verification blocks or missing page data explicitly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snailb1007/skills/propertyguru-sg-sale-browser-crawl)
- [PropertyGuru Default Search URL](https://www.propertyguru.com.sg/property-for-sale?listingType=sale&page=1&isCommercial=false&maxPrice=1400000)
- [Source Notes](references/source-notes.md)

## Skill Output:

**Output Type(s):** [JSON, Data, Guidance]

**Output Format:** [JSON records or Markdown summary with preserved listing payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records should preserve source URL, page number, collection timestamp, listing ID, and raw listingData when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
