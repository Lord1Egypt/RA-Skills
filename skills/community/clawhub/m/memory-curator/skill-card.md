## Description:

Distills verbose daily logs into compact, indexed digests for managing agent memory files, compressing logs, summarizing past activity, and building index-first memory architectures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[77darius77](https://clawhub.ai/user/77darius77)

### License/Terms of Use:


## Use Case:

Developers and agents use Memory Curator to turn verbose daily memory logs into compact digest skeletons that preserve summaries, stats, key events, learnings, connections, open questions, and next-day priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The digest script accepts an unchecked date argument that can escape the intended memory folder and read or overwrite other accessible Markdown files.

Mitigation: Run it only with trusted YYYY-MM-DD date arguments, avoid unreviewed cron automation, and confirm destination digest paths before relying on generated files.

## Reference(s):

- [Memory Curator on ClawHub](https://clawhub.ai/77darius77/skills/memory-curator)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown digest skeletons with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes digest files under the user's local Clawd memory directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
