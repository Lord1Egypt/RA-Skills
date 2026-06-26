## Description: <br>
Scans a user's logged-in social media accounts across Douyin, Xiaohongshu, Weibo, Douban, and Bilibili, compares public presentation with likes, favorites, saves, follows, comments, and history, and generates a humorous Mirror Report about gaps between public persona and observed preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophie-xin9](https://clawhub.ai/user/sophie-xin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this agent skill for self-analysis and entertainment by letting an agent collect data from their own logged-in social media accounts and generate a shareable Markdown Mirror Report. The skill is intended for voluntary personal insight, not assessment of other people. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect logged-in social account activity including likes, favorites, saves, follows, comments, and history. <br>
Mitigation: Use a separate browser profile and approve each platform and data category before collection. <br>
Risk: Collected raw data and Mirror Reports may remain on disk after use. <br>
Mitigation: Delete mirror-reports/ after use if the user does not want retained local data. <br>
Risk: The workflow may download an unpinned ManoBrowser dependency automatically when it is missing. <br>
Mitigation: Review and pin the dependency source before allowing automatic downloads in managed environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sophie-xin9/magic-mirror) <br>
- [Publisher Profile](https://clawhub.ai/user/sophie-xin9) <br>
- [Artifact README](artifact/README.md) <br>
- [Main Skill Definition](artifact/SKILL.md) <br>
- [ManoBrowser Dependency](https://github.com/ClawCap/ManoBrowser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with supporting JSON data files and browser automation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write raw collected data and generated reports under mirror-reports/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
