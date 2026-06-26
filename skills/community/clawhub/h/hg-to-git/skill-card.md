## Description: <br>
Converts Mercurial repositories to Git while preserving history, branches, and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poeticflowerhome](https://clawhub.ai/user/poeticflowerhome) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when migrating legacy Mercurial repositories to Git, including extracting author mappings and running standard or large-repository conversion scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts can install or download executable conversion tooling into the local environment. <br>
Mitigation: Prefer installing hg-fast-export from a trusted source before use, and review the resolved executable before running repository conversions. <br>
Risk: Repository conversion modifies local files and one large-repository script can remove an existing target folder. <br>
Mitigation: Run conversions only on backed-up repositories and choose a destination path that does not already exist or contain data you care about. <br>


## Reference(s): <br>
- [Mercurial to Git Converter on ClawHub](https://clawhub.ai/poeticflowerhome/hg-to-git) <br>
- [hg-fast-export](https://github.com/frej/fast-export) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and generated author-map configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The conversion scripts can create a Git repository, write an authors.map file, and install or download hg-fast-export when it is missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
