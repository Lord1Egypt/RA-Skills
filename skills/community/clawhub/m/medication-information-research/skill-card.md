## Description:

Retrieve source-attributed GoodRx medication and health information with author and review dates. Treat it as secondary material; safety-critical claims remain unverified without official source text. Not for personalized diagnosis, dosing, or treatment decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

People researching a medication, condition, or health topic can use this skill to prepare a concise brief from GoodRx pages with source links and available author, reviewer, and date details. It is not for personalized medical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawlora receives the API key and requested medication or health topics.

Mitigation: Keep personal health and prescription details out of requests, and protect the API key.

Risk: Safety-critical information from GoodRx may not be independently verified against an official source.

Mitigation: Verify safety-critical claims with official source text and a qualified clinician or pharmacist.

Risk: API use may consume account credits.

Mitigation: Bound requests to the user's question and consider API credit usage.

## Reference(s):

- [ClawHub release](https://clawhub.ai/crawlora-org/skills/medication-information-research)
- [GoodRx](https://www.goodrx.com)
- [Crawlora API endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise source-linked Markdown brief with available author, reviewer, and publication or review dates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secondary-source information; identify safety-critical claims that are not independently verified. No personalized diagnosis, dosing, or treatment decisions.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
