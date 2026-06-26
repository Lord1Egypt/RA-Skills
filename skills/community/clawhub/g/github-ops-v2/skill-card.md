## Description: <br>
Automates GitHub repository creation, code pushes, README updates, and release management for an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create repositories, push code, update README files, and create GitHub Releases using git, curl, and a GitHub token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform GitHub write actions with stored credentials, including repository creation, code pushes, releases, and deployment-triggering pushes, without clear review gates. <br>
Mitigation: Use a narrowly scoped GitHub token and require explicit confirmation of the target repository, visibility, branch, files, and release metadata before any write action. <br>
Risk: Pushing workspace content may expose secrets or private files. <br>
Mitigation: Run it only in reviewed workspaces, scan staged changes, and exclude secret or private content before pushing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/github-ops-v2) <br>
- [Declared Homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and GitHub API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git, curl, and GITHUB_TOKEN; operations may create repositories, push code, and create releases.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
