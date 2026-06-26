## Description: <br>
Musify MooreThreads helps agents guide CUDA-to-MUSA code conversion with the musify tool, including batch conversion commands, mapping options, exclusion markers, and review steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongyang-mt](https://clawhub.ai/user/dongyang-mt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers migrating CUDA codebases to Moore Threads MUSA use this skill to plan and run musify-based conversions, then review, build, and test the converted code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: In-place conversion commands can modify project files and text-based API mapping may require manual fixes. <br>
Mitigation: Run conversions on a version-controlled or backed-up project, review diffs, compile with the MUSA compiler, and test on a MUSA device before relying on the result. <br>
Risk: The workflow depends on external toolkit and package sources for musify-text and Python dependencies. <br>
Mitigation: Install only from trusted package and toolkit sources, and use an isolated environment where practical. <br>


## Reference(s): <br>
- [Musify Blog Post](https://blog.mthreads.com/blog/musa/2024-05-28-使用musify对代码进行平台迁移/) <br>
- [MUSA Documentation](https://docs.mthreads.com/) <br>
- [Tutorial on MUSA](https://github.com/MooreThreads/tutorial_on_musa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include in-place file modification commands; users should review diffs before building or committing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
