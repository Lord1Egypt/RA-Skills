## Description:

A PM interview coaching skill that uses a candidate resume, target company and role, optional JD, Xiaohongshu interview reports, and image understanding to run mock interviews and produce detailed feedback and model answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisdontknowcoding](https://clawhub.ai/user/krisdontknowcoding)

### License/Terms of Use:

MIT-0

## Use Case:

External users and interview candidates use this skill to practice product manager interviews for a target company and role. It guides the agent through resume review, recent interview-report lookup, structured mock interview questions, answer coaching, performance feedback, and supplemental practice questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Xiaohongshu and an external vision model as part of the coaching workflow, while that external-service behavior is under-disclosed in the skill text.

Mitigation: Use only approved external services, redact resume contact details and sensitive personal data before use, and disclose the Xiaohongshu and vision-model dependency to users before running those steps.

Risk: The image-fetching helper handles tokens and downloaded images unsafely, including command-line token handling and downloads without URL validation, size limits, safe filenames, or explicit cleanup.

Mitigation: Avoid passing real tokens on the command line, run the helper in an isolated Python virtual environment and workspace, and update it with URL validation, file-size limits, safe filename handling, and cleanup before production use.

Risk: The authoritative security verdict is suspicious because of the under-disclosed external workflow and unsafe helper-script behavior.

Mitigation: Review the skill and helper script before deployment, restrict execution to trusted local environments, and treat generated coaching content as practice guidance that requires user judgment.

## Reference(s):

- [PM Behavioral Question Bank](references/behavioral-questions.md)
- [Business Analysis Framework](references/business-framework.md)
- [ClawHub Skill Page](https://clawhub.ai/krisdontknowcoding/skills/pm-interview-coach)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown interview prompts, feedback tables, reference answers, supplemental questions, and optional bash command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are usually Chinese-language coaching content with structured sections, scoring dimensions, answer-quality gates, and optional local image paths from the helper script.]

## Skill Version(s):

1.4.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
