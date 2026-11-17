## Description:

Query TikTok Shop e-commerce analytics via the bundled kalo CLI for product, shop, creator, video, livestream, and category rankings, details, and revenue trends from KaloData.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maosen-sgy](https://clawhub.ai/user/maosen-sgy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query KaloData-backed TikTok Shop analytics and build structured research workflows for products, shops, creators, videos, livestreams, and categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store a KaloData API key locally or read it from the environment.

Mitigation: Prefer environment-based secrets where possible, keep local config files private, and avoid sharing command transcripts that may include credentials.

Risk: A user-configurable API base URL could receive the KaloData API key if changed to an untrusted destination.

Mitigation: Keep the API base URL at the production KaloData endpoint and set KALODATA_BASE_URL only for destinations you fully trust.

Risk: Broad analysis workflows can fan out into multiple KaloData API calls and consume credits.

Mitigation: Check remaining credits before large analyses, use bounded page and limit options, and tell users when a workflow is likely to make multiple paid API calls.

## Reference(s):

- [Analysis playbooks](references/playbooks.md)
- [ClawHub skill page](https://clawhub.ai/maosen-sgy/skills/kalodata)
- [KaloData Open Center](https://www.kalodata.com/open-center/home)
- [KaloData pricing](https://www.kalodata.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; bundled CLI responses are TOON text or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a KaloData API key and consumes KaloData credits for API-backed queries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
