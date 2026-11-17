## Description:

Memphis Cognitive is a documentation-only meta-package that guides agents through installing and using the separate Memphis CLI for decision capture, memory recall, reflection, prediction, knowledge graph, and multi-agent sync workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elathoxu-crypto](https://clawhub.ai/user/elathoxu-crypto)

### License/Terms of Use:

MIT

## Use Case:

Developers, technical operators, and OpenClaw users use this skill as guidance for adding decision-oriented memory workflows to an agent through the separately installed Memphis CLI. The skill helps users record decisions, query memory, infer decisions from git history, generate reflections, build knowledge graphs, and coordinate memory sharing across agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup documentation recommends remote installer patterns such as curl piped to a shell, including a NodeSource command piped through sudo.

Mitigation: Prefer a pinned release or package version, verify checksums or signatures, and inspect installer scripts before execution.

Risk: Trade and share-sync workflows may move memory records that contain private or proprietary data.

Mitigation: Review memory contents and recipient configuration before using trade or sync commands, and avoid sharing sensitive records unless the receiving environment is trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elathoxu-crypto/skills/memphis-cognitive)
- [Memphis Repository](https://github.com/elathoxu-crypto/memphis)
- [Memphis Documentation](https://github.com/elathoxu-crypto/memphis/tree/master/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only meta-package; Memphis CLI must be installed separately.]

## Skill Version(s):

3.7.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
