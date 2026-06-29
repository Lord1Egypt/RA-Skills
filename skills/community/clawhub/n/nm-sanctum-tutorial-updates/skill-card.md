## Description: <br>
Generates or updates tutorials from VHS tapes and Playwright specs with dual-tone markdown and GIF recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to refresh user-facing tutorials, recordings, GIF assets, README demo sections, and docs or book markdown from VHS tapes, Playwright specs, and tutorial manifests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run project-provided tape, manifest, build, and local service commands while generating tutorial assets. <br>
Mitigation: Use it only in trusted repositories, review tape files and manifest requires entries before execution, and avoid skip-validation options unless the inputs are already trusted. <br>
Risk: The skill can rebuild or install local binaries and modify documentation, README, book summary, and generated media files. <br>
Mitigation: Review generated diffs and asset changes before relying on or publishing them, and confirm rebuild commands are appropriate for the project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-tutorial-updates) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated documentation or asset paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update tutorial markdown, README demo sections, book summaries, and GIF assets in the target repository.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
