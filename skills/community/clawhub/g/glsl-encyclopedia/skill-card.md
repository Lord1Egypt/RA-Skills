## Description: <br>
GLSL Encyclopedia guides agents through docs-first GLSL language and shader-source work, including syntax and semantic lookup, shader authoring and review, stage/interface/layout reasoning, version and extension checks, and compiler-error triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklouzal](https://clawhub.ai/user/kklouzal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to answer, author, review, and debug GLSL shader source using official GLSL docs, local cached excerpts, and clearly separated project observations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches official GLSL documentation and writes workspace-local cache and notes. <br>
Mitigation: Use the documented docs.vulkan.org GLSL workflow and review generated .GLSL-Encyclopedia files before relying on them. <br>
Risk: Workspace notes can accidentally capture secrets, private URLs, tokens, or sensitive access details. <br>
Mitigation: Do not store secrets or sensitive access details in the notes; redact or omit them when recording local observations. <br>


## Reference(s): <br>
- [Official GLSL Documentation](https://docs.vulkan.org/glsl/latest/index.html) <br>
- [GLSL Encyclopedia Workflow](references/workflow.md) <br>
- [GLSL Cache Layout](references/cache-layout.md) <br>
- [GLSL Topic Map](references/topic-map.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kklouzal/glsl-encyclopedia) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and workspace file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace-local .GLSL-Encyclopedia cache and note files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
