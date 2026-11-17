## Description:

Convert CUDA code to MUSA (Moore Threads GPU) using the musify tool for CUDA-to-MUSA migration, kernel/API conversion, and batch conversion of .cu, .cuh, .cpp, and .h files with text-based API mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongyang-mt](https://clawhub.ai/user/dongyang-mt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to migrate CUDA codebases to Moore Threads MUSA by running musify-text conversions, applying optional exclusion markers, reviewing generated changes, and validating the result with the MUSA compiler and device tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ahocorapy dependency is shown without a pinned version.

Mitigation: Install it in a dedicated virtual environment and pin a reviewed version before use in managed workflows.

Risk: In-place conversion can modify source files directly.

Mitigation: Back up or commit the project before running in-place conversion, then review generated diffs before keeping the changes.

Risk: Text-based API mapping may produce conversions that need manual fixes.

Mitigation: Compile converted code with the MUSA compiler and test it on a MUSA device before relying on the result.

## Reference(s):

- [Musify Blog Post](https://blog.mthreads.com/blog/musa/2024-05-28-使用musify对代码进行平台迁移/)
- [MUSA Documentation](https://docs.mthreads.com/)
- [Tutorial on MUSA](https://github.com/MooreThreads/tutorial_on_musa)
- [ClawHub Skill Page](https://clawhub.ai/dongyang-mt/skills/musify)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on text-based CUDA-to-MUSA conversion workflows and expected manual review after conversion.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
