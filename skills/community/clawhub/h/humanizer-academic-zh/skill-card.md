## Description:

Humanizer 中文学术版 helps an agent revise Chinese academic writing to reduce formulaic AI-writing patterns while preserving the user's meaning and academic tone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cangtianhuang](https://clawhub.ai/user/cangtianhuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent in polishing Chinese academic text, removing common AI-generated writing patterns, and producing a more natural revised passage without changing the core meaning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to reduce AI-detection signals in academic writing, which may conflict with school, journal, employer, or disclosure rules.

Mitigation: Use only when policy permits this editing posture, and require the user to retain responsibility for disclosure, authorship, citation, and academic integrity obligations.

Risk: Users may paste confidential or unpublished research into an unapproved AI service while using the prompt.

Mitigation: Review data-handling rules before use and avoid submitting confidential, sensitive, or unpublished material to services that are not approved for that content.

Risk: Broad prompt activation could affect writing outside intentional academic editing sessions.

Mitigation: Enable the skill only for explicit Chinese academic polishing tasks and disable the system prompt when that editing session is complete.

Risk: Unpinned package-manager installation commands can install changed upstream content.

Mitigation: Prefer manual review and installation of the artifact files or pin the package source before deployment.

## Reference(s):

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [blader/humanizer](https://github.com/blader/humanizer)
- [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)
- [redbaronyyyyy-eng/humanizer-zh-academic](https://github.com/redbaronyyyyy-eng/humanizer-zh-academic)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese academic prose or Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces revised user-provided text; no tool calls, API keys, or generated files are required by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
