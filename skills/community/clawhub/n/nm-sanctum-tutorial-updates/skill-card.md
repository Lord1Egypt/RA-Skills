## Description: <br>
Generates or updates tutorials from VHS tapes and Playwright specs with dual-tone markdown and GIF recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to refresh user-facing tutorials, generate terminal and browser demo recordings, and create concise project docs plus deeper book-style tutorial content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local tutorial and demo commands from tape files. <br>
Mitigation: Install only in trusted repositories, review tape files before execution, and avoid skip-validation unless commands are already verified. <br>
Risk: Generated tutorial assets and documentation updates can modify README, SUMMARY, docs, and book content. <br>
Mitigation: Review proposed documentation changes, manifest outputs, and generated media paths before committing them. <br>
Risk: Manifest prerequisite commands and rebuild steps can start background services or rebuild local binaries. <br>
Mitigation: Review manifest requires entries and rebuild/install commands before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-sanctum-tutorial-updates) <br>
- [Project homepage from ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, YAML, Python, and tape examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces tutorial documentation, GIF recording guidance, validation steps, README demo sections, and optional scaffold structures.] <br>

## Skill Version(s): <br>
1.9.12 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
