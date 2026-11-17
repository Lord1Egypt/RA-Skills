## Description:

A skill that converts videos into text and structured copy, then uses custom prompts to create summaries, rewrites, quote collections, shot breakdowns, or translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, editors, and teams use the skill to transcribe local videos or supported video links, extract key information, and turn recordings into summaries, scripts, meeting notes, or translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A previously downloaded video may be uploaded instead of the newly requested video when different URLs share a filename.

Mitigation: Clear prior downloaded media when switching URLs with identical filenames, and verify the selected video before processing.

Risk: The stated network limits are not enforced, and processing requires cloud upload through a paid service token.

Mitigation: Do not use confidential recordings until the publisher clarifies permitted upload hosts and retention terms.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/guaikei-viral-copy-mimic)
- [GuaiKei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or structured Markdown, according to the requested task]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcriptions and prompt-directed summaries, rewrites, quotes, shot breakdowns, notes, or translations.]

## Skill Version(s):

1.0.0 (source: server release, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
