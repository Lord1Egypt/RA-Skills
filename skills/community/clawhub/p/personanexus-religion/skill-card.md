## Description:

Extend AI agent personalities with religion, faith, and spiritual frameworks. Define principles, sacred texts, moral frameworks, traditions, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcrowan3](https://clawhub.ai/user/jcrowan3)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to define, validate, and compile religion, faith, and spiritual-framework settings for PersonaNexus-style agent identities. It supports local generation of system prompts and agent identity files from YAML configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated religion and personality identity files can become persistent agent instructions and may encode unintended beliefs, scope, or behavioral commitments.

Mitigation: Review generated system prompts, SOUL.md, STYLE.md, and personality.json before attaching them to an operational agent.

Risk: Bundled generic templates may contain broad or unrelated fields that are not appropriate for a specific deployment.

Mitigation: Remove unrelated database, memory, or broad-scope fields before using templates as operational agent policies.

Risk: Unpinned Python dependencies can change behavior across installations.

Mitigation: Install in an isolated Python environment and prefer pinned or locked dependency versions.

## Reference(s):

- [PersonaNexus framework](https://github.com/PersonaNexus/personanexus)
- [ClawHub skill page](https://clawhub.ai/jcrowan3/skills/personanexus-religion)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, Python, and shell command examples; runtime outputs may include plain text prompts, JSON, Markdown, SOUL.md, STYLE.md, and OpenClaw personality.json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [All processing is local; generated system prompt, SOUL.md, STYLE.md, and personality.json outputs should be reviewed before use as persistent agent instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
