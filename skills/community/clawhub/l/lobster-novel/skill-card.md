## Description:

Lobster Novel helps OpenClaw agents plan, write, review, and export long-form Chinese fiction with continuity tracking, foreshadowing management, character voices, and token cost controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awoo129](https://clawhub.ai/user/awoo129)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and writers use this skill to manage long-form Chinese fiction projects, generate chapter context or drafts, review quality and continuity, and export manuscript outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe project cache loading can execute code when opening an untrusted novel project.

Mitigation: Use the skill only with trusted project directories until the pickle RAG cache is replaced with a safe format or disabled.

Risk: API-backed writing can disclose unpublished or sensitive manuscript content to the configured provider.

Mitigation: Review provider privacy terms and avoid API-backed writing for sensitive manuscripts unless disclosure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awoo129/skills/lobster-novel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, plain text, HTML, JSON-like status and review data, and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are project-directory based and may use SenseNova API-backed writing when SENSENOVA_API_KEY is configured.]

## Skill Version(s):

1.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
