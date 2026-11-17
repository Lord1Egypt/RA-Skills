## Description:

Find the cheapest available rate for one hotel via the Google Hotels backbone by using StayingAPI offers plus computed minimum and median rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to compare available booking rates for a single hotel through StayingAPI's Google Hotels-backed price comparison endpoint and report the cheapest available offer with coverage caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent needs access to a StayingAPI key and sends hotel lookup parameters to StayingAPI.

Mitigation: Use a sandbox stay_test_ key for evaluation and store any live key only in a trusted environment variable or runtime secret store.

Risk: Some properties return only a single aggregated-lowest offer, which can make a result look broader than the available coverage supports.

Mitigation: Check offers.length and explain when the result is a single-rate or limited-coverage comparison before presenting it as cross-OTA.

Risk: Async scrape jobs can fail, return empty results, or be rate limited if polling is too aggressive.

Mitigation: Honor Retry-After, back off polling attempts, cap retries, and inspect data.status plus meta.warnings or data.error before reporting a result.

## Reference(s):

- [StayingAPI auth setup](references/auth-setup.md)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI docs](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI pricing](https://stayingapi.com/pricing)
- [ClawHub skill page](https://clawhub.ai/stayingapi/skills/google-hotels-compare)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with REST request details and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and internet access to api.stayingapi.com; live requests may return async jobs that require polling.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
