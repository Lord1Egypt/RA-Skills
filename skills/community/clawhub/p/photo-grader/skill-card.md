## Description: <br>
Apply professional-grade color grading to camera RAW, JPG, and HEIC photos through RawTherapee CLI using Lightroom-style JSON parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[konanok](https://clawhub.ai/user/konanok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to batch grade RAW, JPG, or HEIC photo sets, generate RawTherapee PP3 sidecars, and export graded images from AI-recommended or manually supplied Lightroom-style parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local photo directories and JSON parameter files and writes graded outputs or PP3 sidecars. <br>
Mitigation: Run it only against intended project directories, review output paths before execution, and use dry-run or PP3-only mode when validating a new batch. <br>
Risk: The skill invokes RawTherapee CLI as a local external processor. <br>
Mitigation: Install RawTherapee from a trusted source, verify rawtherapee-cli before use, and keep the executable path under user control through PATH or config.toml. <br>
Risk: setup_deps.sh may install Python dependencies outside the desired environment on systems where tomli is missing. <br>
Mitigation: Use a project virtual environment before running setup_deps.sh, or install tomli manually in the intended Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/konanok/photo-grader) <br>
- [Publisher profile](https://clawhub.ai/user/konanok) <br>
- [Project homepage](https://github.com/konanok/photo-skills) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON parameter input, TOML configuration, PP3 sidecar files, and graded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local photo files and RawTherapee CLI; can run dry-run, PP3-only, uniform batch, and image export modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, VERSION, changelog released 2026-05-20, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
