## Description:

MarriottAI helps agents search and present Marriott hotels, hotel packages, attractions, and train tickets using the FlyAI travel platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[birkhoff-china](https://clawhub.ai/user/birkhoff-china)

### License/Terms of Use:

MIT-0

## Use Case:

Travel-focused agents use this skill to answer external user requests for Marriott stays, hotel packages, local attractions, and train options, including comparison, itinerary planning, and booking-link presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned global third-party FlyAI CLI whose executable code is outside the reviewed artifact.

Mitigation: Install only after trusting the FlyAI CLI publisher; prefer a pinned, locally scoped, or sandboxed installation before using it for travel decisions.

Risk: Optional FLYAI_API_KEY configuration may expose credentials to the third-party CLI.

Mitigation: Configure FLYAI_API_KEY only if you trust how the CLI stores and uses the key, and prefer scoped or disposable credentials where possible.

Risk: Returned prices, availability, and booking links may change and may reflect Marriott/Fliggy-focused inventory with China-oriented locale defaults.

Mitigation: Treat results as booking guidance and confirm final prices, policies, and availability on the linked provider pages before purchase.

## Reference(s):

- [MarriottAI ClawHub Skill Page](https://clawhub.ai/birkhoff-china/skills/marriott-ai)
- [birkhoff-china Publisher Profile](https://clawhub.ai/user/birkhoff-china)
- [FlyAI Homepage](https://open.fly.ai/)
- [search-marriott-hotel reference](artifact/references/search-marriott-hotel.md)
- [search-marriott-package reference](artifact/references/search-marriott-package.md)
- [search-poi reference](artifact/references/search-poi.md)
- [search-train reference](artifact/references/search-train.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Single-line JSON from FlyAI CLI commands, followed by Markdown travel summaries with images and booking links when data is available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results may include real-time prices, images, booking URLs, itinerary details, and optional API-key configuration.]

## Skill Version(s):

1.0.6 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
