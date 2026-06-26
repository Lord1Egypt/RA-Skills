## Description: <br>
Reads local RSS/XML files from the workspace, extracts title tags, and produces a concise list of news headlines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fedrov2025](https://clawhub.ai/user/fedrov2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users can use this skill to summarize a local RSS or XML file by listing the first ten title entries. It is suited for local feed inspection where the input file is already present in the workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs shell scripts over local RSS/XML files and may return misleading results for malformed feeds or feeds with complex XML structure. <br>
Mitigation: Use it on RSS/XML files you intend to inspect and review the resulting headline list before relying on it. <br>
Risk: summarize.sh calls the companion extract.sh script by relative path. <br>
Mitigation: Run the skill from the directory that contains the companion scripts, or update the script path before use in another workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fedrov2025/news-summary-local) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text headline list with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs up to 10 title entries from a provided RSS/XML file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
