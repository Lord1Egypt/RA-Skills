## Description: <br>
Use OpenCLI to fetch data from websites like Twitter, Reddit, Bilibili, Zhihu, Xiaohongshu, YouTube, and other social, video, and news sites without API keys by reusing Chrome login sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HelloTomBruce](https://clawhub.ai/user/HelloTomBruce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query social, video, finance, news, and desktop-app sources through OpenCLI commands. It is most useful when a task needs browser-backed access to public pages or logged-in account data without a site-specific API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenCLI can act through logged-in browser and desktop app sessions to post, message, delete, write, export private data, or change account state. <br>
Mitigation: Use a separate Chrome profile with limited accounts and require explicit user confirmation before commands that send, post, delete, follow, write, export private data, or change account state. <br>
Risk: The skill depends on a global npm package and Browser Bridge extension that can access active browser sessions. <br>
Mitigation: Review the npm package and browser extension before installation, keep them updated from trusted sources, and limit use to accounts and sessions intended for automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HelloTomBruce/opencli-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, Markdown, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with OpenCLI shell commands; command output may be table, JSON, YAML, Markdown, CSV, or downloaded files depending on the command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenCLI, the Browser Bridge extension, and an authenticated Chrome session for cookie or UI automation commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
