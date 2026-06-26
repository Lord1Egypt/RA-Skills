## Description: <br>
This skill should be used when the user asks to "download files from GitHub", "fetch a folder from a repo", "grab code from GitHub", "download a GitHub repository", "get files from a GitHub URL", "clone just a folder", or needs to download specific files/folders from GitHub without cloning the entire repo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waldekmastykarz](https://clawhub.ai/user/waldekmastykarz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to download GitHub files, folders, or repositories with the gitload CLI without cloning full git history. It is useful for fetching targeted source files, template folders, ZIP archives, and private repository content when authentication is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may involve GitHub tokens or other sensitive credentials for private repositories and rate-limit handling. <br>
Mitigation: Prefer gh auth login or fine-grained read-only GitHub tokens, and avoid placing real tokens directly in commands that may be stored in shell history. <br>
Risk: The skill relies on the external gitload-cli npm package and may download code that could later be installed or executed. <br>
Mitigation: Install the package only when comfortable with that dependency, and inspect downloaded code before running npm install, build commands, or other execution steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/waldekmastykarz/gitload) <br>
- [Publisher profile](https://clawhub.ai/user/waldekmastykarz) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GitHub URLs, output paths, ZIP options, and authentication options for private repositories or rate limits.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
