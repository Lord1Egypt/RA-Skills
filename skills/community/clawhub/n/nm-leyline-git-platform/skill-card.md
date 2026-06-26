## Description: <br>
Detects git forge (GitHub/GitLab/Bitbucket) and maps CLI commands cross-platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to detect whether a repository is hosted on GitHub, GitLab, or Bitbucket and choose platform-appropriate CLI or API commands for issues, pull requests, merge requests, discussions, and CI configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced forge commands can create, close, merge, approve, or comment on remote issues, pull requests, merge requests, and discussions. <br>
Mitigation: Require explicit confirmation before running remote-changing examples, and verify both the target repository and the authenticated account. <br>
Risk: Using the wrong platform mapping can produce incorrect commands or terminology for GitHub, GitLab, or Bitbucket workflows. <br>
Mitigation: Confirm the detected git platform and available CLI before applying a mapped command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-git-platform) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Command mapping module](modules/command-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and API command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable files are included in the artifact; outputs are reference text for agent workflows.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
