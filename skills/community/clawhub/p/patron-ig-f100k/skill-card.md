## Description:

Analyzes a user's Instagram videos from the last seven days, optionally transcribes reels with Supadata, classifies performance against weekly medians, extracts viral and negative patterns, and updates a persistent Instagram patterns memory file for future scriptwriting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and agents use this skill to review weekly Instagram reel performance, identify content patterns that worked or underperformed, and update reusable memory for future scriptwriting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram reel URLs may be sent to Supadata for transcription.

Mitigation: Use the skill only when sharing those reel URLs with Supadata is acceptable, and skip transcription when that data sharing is not approved.

Risk: The skill may use Apify for Instagram scraping.

Mitigation: Confirm the Apify account, actor configuration, and Instagram data collection terms before scheduled or repeated use.

Risk: The skill can update a persistent patterns memory file that may influence later scriptwriting.

Mitigation: Review the generated patterns file before relying on it for future content decisions.

Risk: The artifact sources a local secrets file when SUPADATA_API_KEY is missing.

Mitigation: Provide SUPADATA_API_KEY through a scoped secret mechanism instead of allowing broad environment loading from a secrets file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/patron-ig-f100k)
- [Supadata transcript API endpoint](https://api.supadata.ai/v1/transcript)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown memory file with weekly analysis tables, pattern summaries, and terminal confirmation text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Instagram reel URLs, captions, weekly engagement medians, performance classifications, and transcription availability notes.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
