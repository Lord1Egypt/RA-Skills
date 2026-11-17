## Description:

Polish and improve literature review for students and researchers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeoyee](https://clawhub.ai/user/jeoyee)

### License/Terms of Use:

MIT-0

## Use Case:

Students and researchers use this skill to analyze literature review structure, citation density, and critical thinking, then polish draft text with Kimi AI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user drafts to Moonshot/Kimi for polishing, which may expose confidential, unpublished, regulated, or student-identifying text.

Mitigation: Use only with drafts appropriate for Moonshot/Kimi processing, and avoid confidential or regulated content unless external processing is approved.

Risk: The release embeds a real-looking API key in both scripts.

Mitigation: Revoke the exposed key, remove it from the scripts, and require users to provide their own key through environment configuration before use.

Risk: The script can save polished output files locally.

Mitigation: Warn users before writing files and review saved outputs for sensitive content handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeoyee/skills/literature-review-polisher)
- [Moonshot API endpoint](https://api.moonshot.cn/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Interactive console text and saved polished text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save polished output to a timestamped local text file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
