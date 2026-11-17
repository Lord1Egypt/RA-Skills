## Description:

Fetches the Solo Scope RSS feed, groups entries into 3-6 concise topics, writes short core-value summaries, and returns a Markdown briefing with original titles and URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadowcz007](https://clawhub.ai/user/shadowcz007)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to turn the MIXDAO Solo Scope RSS feed into a concise daily briefing organized for solo founders and small teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad RSS-summary prompts could route to this skill when the user did not intend a Solo Scope briefing.

Mitigation: Use strict skill routing or explicit trigger phrases such as Solo Scope, MIXLAB Solo Scope, mixdao feed, or RSS category briefing.

Risk: Generated briefings may include the MIXLAB branding line from the template.

Mitigation: Review the final Markdown before sharing externally and remove branding that is not appropriate for the use case.

Risk: The briefing depends on one live RSS feed, so output quality depends on feed availability and feed item content.

Mitigation: Confirm the source feed is reachable and check that retained titles and URLs match the RSS entries before relying on the summary.

## Reference(s):

- [Solo Scope RSS feed](https://www.mixdao.world/feed)
- [ClawHub skill page](https://clawhub.ai/shadowcz007/skills/mixlab-solo-scope)
- [Publisher profile](https://clawhub.ai/user/shadowcz007)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with grouped source links and short category summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each category summary is limited to 140 Chinese characters; entries retain original RSS titles and URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
