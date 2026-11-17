## Description:

Provides EEG and neuroscience answers by retrieving from a local SQLite Wikipedia-derived knowledge base and presenting concise, sourced explanations in an Elon Musk-inspired first-principles voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhongm](https://clawhub.ai/user/yhongm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer EEG, brain-wave, sleep, epilepsy, BCI, and neuroscience questions with cited knowledge-base snippets and persona-styled explanatory guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external neuroscience database that was not included in the server review.

Mitigation: Only install the database from a trusted release source and review it before deployment.

Risk: The skill covers medical-adjacent and mental-health-adjacent topics.

Mitigation: Treat outputs as educational summaries and require qualified professional review for diagnosis, treatment, or care decisions.

Risk: The fixed forceful persona can make uncertain neuroscience claims sound more confident than they are.

Mitigation: Require explicit uncertainty language and source labels for substantive claims, especially on clinical or emerging-science topics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yhongm/skills/musk-eeg)
- [Musk-EEG homepage metadata](https://github.com/yhongm/Musk-EEG)
- [Electroencephalography reference](https://en.wikipedia.org/wiki/Electroencephalography)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with cited source labels and occasional inline shell commands for database search workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are intended as educational summaries, not medical or mental-health advice.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
