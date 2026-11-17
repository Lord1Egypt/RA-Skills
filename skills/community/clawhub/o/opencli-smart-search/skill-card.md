## Description:

Routes search and research requests to suitable opencli sources, including AI, web, social, technical, shopping, travel, finance, jobs, and Chinese-language sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to choose appropriate opencli search sources, inspect live command help, run bounded searches, and report which sites and queries were used. It is especially useful for multilingual research workflows that need source routing across AI, social, technical, media, commerce, travel, finance, and job-search providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms may be sent to selected external providers, including social-media, shopping, travel, finance, or job-search sources.

Mitigation: Review the selected source before execution and avoid sensitive queries unless the provider is appropriate for that information.

Risk: Broad source routing can produce incomplete, stale, or provider-biased results.

Mitigation: Use the required live help checks, per-site call ledger, frequency limits, and final search summary to make source coverage and gaps visible.

## Reference(s):

- [AI Default Sources](references/sources-ai.md)
- [Information and Knowledge Sources](references/sources-info.md)
- [Media and Entertainment Sources](references/sources-media.md)
- [Other Vertical Sources](references/sources-other.md)
- [Shopping Sources](references/sources-shopping.md)
- [Social Media Sources](references/sources-social.md)
- [Technical and Academic Sources](references/sources-tech.md)
- [Travel Sources](references/sources-travel.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and a required search summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live opencli registry and help output to select sources; the skill itself does not generate persistent files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
