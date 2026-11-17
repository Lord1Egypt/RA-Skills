## Description:

Generate Instagram marketing content from product URLs, including product details, image suggestions, captions, calls to action, hashtag strategy, and Story or Reel content suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, creators, and commerce teams use this skill to turn product URLs into ready-to-post Instagram content packages. It supports product extraction, content format selection, visual briefs, captions, hashtag sets, posting guidance, and engagement preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated product extraction sends the API key and product page data to an API hostname that differs from the main documentation.

Mitigation: Confirm whether api.heybossai.com is an authorized SkillBoss endpoint before use, and only use a narrowly scoped SKILLBOSS_API_KEY.

Risk: Product URLs and scraped page content may include private, sensitive, or embargoed product information.

Mitigation: Use only public product URLs or approved internal URLs, and avoid submitting sensitive product pages to the extraction script.

Risk: Extracted product claims may be incomplete or inaccurate.

Mitigation: Check generated claims, prices, benefits, and audience assumptions against the source product page before publishing marketing content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/godfery-mkt)
- [Publisher profile](https://clawhub.ai/user/tobeyrebecca)
- [Instagram Hashtag Strategy](references/HASHTAG_STRATEGY.md)
- [Output Template](templates/OUTPUT_TEMPLATE.md)
- [SkillBoss API endpoint used by artifact](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown content package with optional JSON product extraction output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for automated product extraction; manual extraction fallback is documented.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
