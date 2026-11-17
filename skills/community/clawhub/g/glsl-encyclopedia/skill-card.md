## Description:

GLSL language/specification workflow for GLSL-specific questions, shader authoring and review, exact syntax and semantic lookup, built-in and qualifier reference, interface/layout reasoning, stage-specific behavior checks, version/extension rules, and compiler-error triage when the actual language layer is GLSL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklouzal](https://clawhub.ai/user/kklouzal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to answer, author, review, and troubleshoot GLSL shader-language work with a docs-first workflow. It is intended for GLSL syntax, qualifiers, built-ins, interfaces, stage behavior, version or extension rules, and compiler-error triage, not for unrelated shader languages or generic Vulkan API debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a .GLSL-Encyclopedia directory in the active workspace containing cached documentation and local shader notes that may be shared or committed with the workspace.

Mitigation: Review the cache and notes before sharing or committing workspace files, and avoid storing plaintext credentials, private URLs, tokens, recovery codes, or other secrets there.

Risk: Cached GLSL documentation and local observations can become stale or be mistaken for authoritative project-independent language behavior.

Mitigation: Refresh or re-check official GLSL docs for exact syntax, layout/interface rules, built-ins, stage behavior, compiler errors, and version-sensitive decisions, and keep local observations clearly labeled.

## Reference(s):

- [Official GLSL Documentation](https://docs.vulkan.org/glsl/latest/index.html)
- [GLSL Variables Documentation](https://docs.vulkan.org/glsl/latest/chapters/variables.html)
- [Workflow](references/workflow.md)
- [Cache Layout](references/cache-layout.md)
- [Topic Map](references/topic-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workspace-local .GLSL-Encyclopedia cache, notes, and inventory files when the agent applies the skill workflow.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
