## Description: <br>
Collects data from a user's logged-in Douyin, Xiaohongshu, Weibo, Douban, and Bilibili accounts, cross-analyzes it, and generates USER.md and MEMORY.md profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophie-xin9](https://clawhub.ai/user/sophie-xin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill during onboarding or personalization setup to build a local user profile from the user's own logged-in social-platform activity. It is intended to help an agent understand user interests, history, and preferences before producing personalized assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read broad data from logged-in social accounts, including likes, favorites, follows, ratings, posts, uploads, and related third-party metadata. <br>
Mitigation: Use it only after explicit user consent, select platforms and data categories deliberately, and review the generated profile before relying on it. <br>
Risk: Generated raw JSON and profile files may contain sensitive personal information stored locally. <br>
Mitigation: Inspect know-your-owner-data and the generated USER.md and MEMORY.md files, keep them in a trusted local workspace, and delete them when no longer needed. <br>
Risk: The workflow may auto-download the ManoBrowser browser automation dependency. <br>
Mitigation: Review or pin the ManoBrowser dependency before use and confirm the browser extension and MCP configuration are expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sophie-xin9/know-your-owner) <br>
- [Publisher profile](https://clawhub.ai/user/sophie-xin9) <br>
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown profile files plus locally stored JSON data and progress guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces USER.md, MEMORY.md, and platform-specific raw data under know-your-owner-data when collection succeeds.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
