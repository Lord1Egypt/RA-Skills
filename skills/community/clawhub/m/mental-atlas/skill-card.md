## Description:

Apply a four-layer learning framework to pasted text, files, URLs, or domain names to extract representations, schemas, mental models, disputes, test questions, and a compressed conclusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bhackerj](https://clawhub.ai/user/bhackerj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, students, and knowledge workers use this skill to turn source material or a domain prompt into a compact learning map with core concepts, reusable patterns, mental models, major disputes, and application-focused test questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided local paths or URLs cause the agent to read or fetch that material.

Mitigation: Provide only material the agent is authorized to access, and review fetched or read content before relying on the resulting learning map.

Risk: Mixed-language inputs may produce Chinese output by default.

Mitigation: Specify the desired output language in the user request when a different language is required.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with tables, structured sections, bilingual headings when appropriate, and collapsible-style hints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output language follows the input language rules in the artifact; mixed-language inputs produce Chinese output by default.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
