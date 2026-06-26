## Description: <br>
Monitor web pages for content changes and get alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corbin-breton](https://clawhub.ai/user/corbin-breton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and automation users use this skill to watch user-chosen web pages for content changes, inspect diffs, and monitor specific sections with CSS selectors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches URLs supplied by the user and stores page text and diffs locally. <br>
Mitigation: Use workspace-specific WEB_MONITOR_DIR storage and avoid sensitive or authenticated pages unless local retention is intended. <br>
Risk: Removing a watch may not delete prior snapshot or diff files. <br>
Mitigation: Review and delete retained files from the configured monitor directory when removing sensitive watches. <br>
Risk: JavaScript-rendered page content may not be captured because the monitor fetches raw HTML. <br>
Mitigation: Use it for pages where the relevant content is present in fetched HTML, or confirm snapshots before relying on alerts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/corbin-breton/keats-web-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or read local watch configuration, snapshots, and diff files under WEB_MONITOR_DIR or the default local data directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
