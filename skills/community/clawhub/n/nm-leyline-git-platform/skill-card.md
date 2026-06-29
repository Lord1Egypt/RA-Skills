## Description: <br>
Detects git forge (GitHub/GitLab/Bitbucket) and maps CLI commands cross-platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to identify whether a project is hosted on GitHub, GitLab, or Bitbucket and choose platform-appropriate commands for issues, pull requests or merge requests, discussions, and CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested gh, glab, curl, or API commands can mutate hosted repositories or public project content. <br>
Mitigation: Confirm the target repository, platform, authentication context, and intended action before running any generated command. <br>
Risk: Platform-specific command mappings may be inappropriate when the repository host is unknown or the expected CLI is unavailable. <br>
Mitigation: Check the git remote, platform markers, and CLI availability first, then fall back to the documented REST API or web interface path when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-git-platform) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Complete Command Mapping](modules/command-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and command mapping tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes platform-specific terminology and command equivalents for GitHub, GitLab, and Bitbucket.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
