## Description:

English Visual Vocabulary helps learners memorize English words with visual cards, pronunciation, Chinese definitions, root analysis, personalized study plans, and Ebbinghaus review schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bxwzan](https://clawhub.ai/user/bxwzan)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and educators use this skill to create visual English vocabulary cards, study plans, root and affix explanations, and spaced review schedules for vocabulary learning and test preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A card-generation script can write files outside its intended output folder when given crafted word input.

Mitigation: Run scripts only with trusted word lists, or validate and sanitize word values before allowing scripts to create files.

Risk: Image search or generation may send vocabulary prompts to external services.

Mitigation: Confirm external image tools are acceptable for the use case and avoid submitting sensitive or proprietary vocabulary prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bxwzan/skills/learn-english-with-images)
- [Common English roots and affixes](artifact/references/common_roots.md)
- [Ebbinghaus review schedule](artifact/references/ebbinghaus_schedule.md)
- [Beginner vocabulary list](artifact/references/vocabulary_lists/beginner.json)
- [Intermediate vocabulary list](artifact/references/vocabulary_lists/intermediate.json)
- [Advanced vocabulary list](artifact/references/vocabulary_lists/advanced.json)
- [Oxford Learner's Dictionaries](https://www.oxfordlearnersdictionaries.com/)
- [Etymonline](https://www.etymonline.com/)
- [Anki](https://apps.ankiweb.net/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown vocabulary cards and plans, JSON study data and schedules, shell command examples, and plain-language study guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown and JSON files for cards, plans, review schedules, logs, and reports.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and README report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
