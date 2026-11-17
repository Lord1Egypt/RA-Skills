## Description:

Graphify Source helps agents build and query local knowledge graphs from code repositories, documents, images, video, and audio using a local llama.cpp model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peing111](https://clawhub.ai/user/peing111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert local project sources and related media into searchable knowledge graphs, then query architecture, paths, and component behavior through natural language commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags this skill as a review concern because it asks users to run an unreviewed local program over whole projects.

Mitigation: Install and run only a verified graphify.py from a trusted source, and test on non-sensitive projects before broader use.

Risk: The security evidence notes inconsistent local-only assurances and optional Anthropic/OpenAI API key use for semantic extraction.

Mitigation: Avoid running the skill over repositories containing secrets or private data, and do not set external API keys unless extracted content may leave the machine.

## Reference(s):

- [Graphify homepage](https://clawhub.ai/fantox/graphify)
- [Graphify Source ClawHub skill page](https://clawhub.ai/peing111/skills/graphify-source)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; generated graph artifacts include Markdown, HTML, and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts are described as being written under graphify-out/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
