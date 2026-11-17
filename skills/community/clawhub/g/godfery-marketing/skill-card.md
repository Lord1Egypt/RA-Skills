## Description:

Generate Instagram marketing content from product URLs, including image suggestions, captions, calls to action, hashtag strategy, and story or reel content ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, creators, and e-commerce operators use this skill to turn product URLs into ready-to-post Instagram content packages. It helps plan feed posts, carousels, stories, reels, captions, hashtags, posting strategy, and engagement preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The extraction script sends product URLs, scraped page content, and SKILLBOSS_API_KEY-bearing requests to an external API service.

Mitigation: Use only public product URLs, avoid private or signed URLs, and confirm the external API provider is trusted before use.

Risk: The evidence reports a mismatch between the API endpoint documented by the skill and the endpoint used by the script.

Mitigation: Confirm whether api.skillbossai.com and api.heybossai.com are the same trusted provider endpoint before running automated extraction.

Risk: Extracted product claims may be incomplete or inaccurate.

Mitigation: Review product facts, pricing, claims, and generated marketing copy against the source product page before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/godfery-marketing)
- [Instagram Hashtag Strategy](artifact/references/HASHTAG_STRATEGY.md)
- [Instagram Content Package Output Template](artifact/templates/OUTPUT_TEMPLATE.md)
- [SkillBoss API Hub endpoint from skill documentation](https://api.skillbossai.com/v1/pilot)
- [SkillBoss API endpoint used by extraction script](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown content package with optional JSON product extraction output and inline shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for automated product extraction; manual extraction fallback is documented.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
